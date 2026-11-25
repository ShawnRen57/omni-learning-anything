"""Refresh the source tables in every README. Use --check to detect drift."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'skills/omni-learning-anything/references/course-catalog.json'
LABELS = ROOT / 'tools/content/readme_catalog_labels.csv'
START = '<!-- catalog:start -->'
END = '<!-- catalog:end -->'

# Keep a school and its imprints in one row. Retain the named publishing
# unit alongside the relevant group when a school provides different sources.
PROVIDERS = {
    'Harvard University (HarvardX)': ('Harvard University', ''),
    '清华大学计算机系人工智能通识教育研究中心': ('清华大学', ''),
    'MIT Press': ('Massachusetts Institute of Technology', 'MIT Press'),
    'MIT Press / authors': ('Massachusetts Institute of Technology', 'MIT Press'),
    'Stanford University / authors': ('Stanford University', ''),
    'Stanford Encyclopedia of Philosophy': ('Stanford University', 'Stanford Encyclopedia of Philosophy'),
    'O’Reilly / authors': ('O’Reilly', ''),
}
KINDS = ('course', 'reference', 'textbook', 'academic_book', 'article', 'lecture_series', 'talk')
FIRST = ('清华大学', '北京大学', '复旦大学', '上海交通大学', '浙江大学', '北京师范大学',
         'Harvard University', 'Yale University', 'Massachusetts Institute of Technology', 'Stanford University')


def grouped_sources(catalog):
    grouped = defaultdict(lambda: defaultdict(list))
    for course in catalog['courses']:
        provider, imprint = PROVIDERS.get(course['institution'], (course['institution'], ''))
        kind = course.get('pathway_type', 'course')
        grouped[provider][(kind, imprint)].append((course['title'], '', course['sources'][0]['url']))
    for resource in catalog['resources']:
        provider, imprint = PROVIDERS.get(resource['provider'], (resource['provider'], ''))
        grouped[provider][(resource['kind'], imprint)].append(
            (resource['title'], resource['zh_title'], resource['url']))
    return grouped


def source_link(title, zh_title, url, language):
    label = zh_title if language == 'zh' and zh_title else title
    label = label.replace('\\', '\\\\').replace('[', r'\[').replace(']', r'\]').replace('|', r'\|')
    # Markdown titles preserve the original spelling for translated catalogue entries.
    tooltip = ''
    if language == 'zh' and zh_title and zh_title != title:
        tooltip = ' "' + title.replace('"', '&quot;').replace('|', '&#124;') + '"'
    href = quote(url, safe=":/?#[]@!$&'*+,;=%~-._")
    return f'[{label}]({href}{tooltip})'


def table(grouped, language, labels):
    total = sum(len(links) for by_type in grouped.values() for links in by_type.values())
    heading = f"| {labels['provider_header']} | {labels['links_header']} ({total}) |"
    lines = [heading, '| --- | --- |']
    providers = [p for p in FIRST if p in grouped] + [p for p in grouped if p not in FIRST]
    for provider in providers:
        groups = []
        for (kind, imprint), records in sorted(grouped[provider].items(), key=lambda item: KINDS.index(item[0][0])):
            category = labels[kind] + (' · ' + imprint if imprint else '')
            links = [source_link(*record, language) for record in records]
            groups.append('**' + category + '** ' + ' · '.join(links))
        lines.append('| ' + labels.get(provider, provider) + ' | ' + '<br>'.join(groups) + ' |')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    groups = grouped_sources(json.loads(CATALOG.read_text(encoding='utf-8')))
    with LABELS.open(encoding='utf-8', newline='') as source:
        rows = list(csv.DictReader(source))
    stale = []
    for lang in rows[0]:
        if lang == 'key':
            continue
        labels = {row['key']: row[lang] for row in rows}
        path = ROOT / ('README.md' if lang == 'en' else f'docs/readme/README_{lang}.md')
        old = path.read_text(encoding='utf-8')
        if old.count(START) != 1 or old.count(END) != 1:
            raise ValueError(f'Missing or duplicate catalogue markers in {path}')
        before, current = old.split(START)
        _, after = current.split(END)
        updated = before + START + '\n\n' + table(groups, lang, labels) + '\n\n' + END + after
        if old != updated:
            stale.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(updated, encoding='utf-8')
    if args.check and stale:
        raise SystemExit('Outdated source tables: ' + ', '.join(stale))


if __name__ == '__main__':
    main()
