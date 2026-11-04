"""Build the metadata-only K12 index from a pinned GitHub recursive tree."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

REPOSITORY = "TapXWorld/ChinaTextbook"
COMMIT = "e2b3f62213c77bb8c33c5be355f97625ea1b8b61"
OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "skills/omni-learning-anything/references/textbook-index.json"
)
ROOTS = {
    "小学": ("小学", "六三学制"),
    "初中": ("初中", "六三学制"),
    "高中": ("高中", None),
    "小学（五•四学制）": ("小学", "五四学制"),
    "初中（五•四学制）": ("初中", "五四学制"),
}
PDF = re.compile(r"(.+\.pdf)(?:\.(\d+))?")
AUXILIARY = re.compile(r"教师(?:教学)?用书|教学用书|教参|练习册|习题集|活动册|答案|学具")
YEAR = re.compile(r"(?<!\d)((?:19|20)\d{2})\s*年?版")
GRADE = re.compile(r"([一二三四五六七八九])年级(?!起点)")
GRADE_RANGE = re.compile(r"([1-9])至([1-9])年级")
DIGITS = "〇一二三四五六七八九"
VOLUME = re.compile(r"全一册|[上中下]册|第[一二三四五六七八九十\d]+册")
TRACK = re.compile(r"(?P<track>选择性必修|必修|选修)\s*(?P<number>[0-9]+|第[一二三四五六七八九十]+册|全一册|[上中下]册)?")


def book_metadata(path):
    root, subject, edition_dir, *rest = PurePosixPath(path).parts
    title = rest[-1].removesuffix(".pdf")
    stage, school_system = ROOTS[root]
    edition, _, publisher = edition_dir.partition("-")
    edition_family = re.split(r"（|[一三]年级起点", edition, maxsplit=1)[0]
    grades = []
    if len(rest) > 1 and GRADE.fullmatch(rest[0]):
        grades = [rest[0]]
    elif grade_range := GRADE_RANGE.search(title):
        low, high = map(int, grade_range.groups())
        grades = [f"{DIGITS[number]}年级" for number in range(low, high + 1)]
    elif grade := GRADE.search(title):
        grades = [grade[0]]

    track = TRACK.search(title) if stage == "高中" else None
    if track:
        suffix = title[track.end():].strip()
        volume = track["track"]
        if track["number"]:
            joiner = "" if track["number"].isdigit() else " "
            volume += joiner + track["number"]
        elif suffix:
            volume += " " + suffix
    else:
        suffix = ""
        match = VOLUME.search(title)
        volume = match[0] if match else None

    year = YEAR.search(f"{edition} {title}")
    kind = "student_reader" if "学生读本" in title else "student_textbook"
    return {
        "book_id": "ct-" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:20],
        "title": title,
        "stage": stage,
        "grade": "至".join(grades) if len(grades) <= 1 else grades[0] + "至" + grades[-1],
        "grade_levels": grades,
        "subject": subject,
        "edition": edition,
        "edition_family": edition_family,
        "publisher": publisher or None,
        "volume": volume,
        "module_title": suffix or None,
        "school_system": school_system,
        "year": int(year[1]) if year else None,
        "material_type": kind,
        "repository": REPOSITORY,
        "commit": COMMIT,
    }


def build(tree):
    expected_url = f"https://api.github.com/repos/{REPOSITORY}/git/trees/{COMMIT}"
    if tree.get("sha") != COMMIT or tree.get("url") != expected_url or tree.get("truncated") is not False:
        raise ValueError("Expected the complete, pinned ChinaTextbook Git tree.")
    audit = Counter()
    groups = defaultdict(list)
    for entry in tree["tree"]:
        if entry["type"] != "blob":
            continue
        audit["tree_blobs"] += 1
        path = entry["path"]
        root, *folders, filename = PurePosixPath(path).parts if "/" in path else (path, path)
        if root not in ROOTS:
            audit["excluded_non_k12_blobs"] += 1
            continue
        audit["k12_blobs"] += 1
        match = PDF.fullmatch(filename)
        if not match:
            audit["excluded_k12_non_pdf_blobs"] += 1
            continue
        if AUXILIARY.search(filename):
            audit["excluded_teacher_or_workbook_blobs"] += 1
            continue
        if folders[1].startswith("配套"):
            audit["excluded_companion_blobs"] += 1
            continue
        stem, part = match.groups()
        if folders[-1] == stem + "_merge_folder":
            folders.pop()
        logical_path = "/".join((root, *folders, stem))
        groups[logical_path].append({
            "path": path, "size": entry["size"], "sha": entry["sha"],
            "part": int(part) if part else None,
        })

    books = []
    for path, alternatives in sorted(groups.items()):
        whole = [source for source in alternatives if source["part"] is None]
        if whole:
            sources = whole
            audit["superseded_split_blobs"] += len(alternatives) - len(whole)
        else:
            sources = sorted(alternatives, key=lambda source: source["part"])
            if [source["part"] for source in sources] != list(range(1, len(sources) + 1)):
                raise ValueError(f"Missing or duplicate split pieces for {path}")
            audit["split_books"] += 1
        book = book_metadata(path)
        book["grade"] = book["grade"] or None
        book["sources"] = sources
        books.append(book)
        audit["catalog_source_blobs"] += len(sources)
        audit["catalog_student_readers"] += book["material_type"] == "student_reader"
    audit["catalog_books"] = len(books)
    audit["catalog_student_textbooks"] = len(books) - audit["catalog_student_readers"]
    return {
        "schema_version": 1,
        "repository": REPOSITORY,
        "commit": COMMIT,
        "evidence": "repository_tree_metadata",
        "audit": dict(sorted(audit.items())),
        "stage_counts": dict(sorted(Counter(book["stage"] for book in books).items())),
        "books": books,
    }


def serialize(index):
    """Keep generated book records on separate lines for reviewable changes."""
    metadata = {key: value for key, value in index.items() if key != "books"}
    header = json.dumps(metadata, ensure_ascii=False, indent=2).removesuffix("\n}")
    records = ",\n".join(
        "    " + json.dumps(book, ensure_ascii=False, separators=(",", ":"))
        for book in index["books"]
    )
    return header + ',\n  "books": [\n' + records + "\n  ]\n}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tree", type=Path, help="Saved pinned recursive Git tree JSON")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    index = build(json.loads(args.tree.read_text(encoding="utf-8")))
    args.output.write_text(serialize(index), encoding="utf-8")
    print(json.dumps(index["audit"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
