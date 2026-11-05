"""Textbook discovery preserves exact source identity and unresolved choices."""

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "omni-learning-anything" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class TextbookIndexTests(unittest.TestCase):
    def engine(self):
        self.assertIsNotNone(importlib.util.find_spec("omni_textbook_index"))
        import omni_textbook_index

        return omni_textbook_index

    def test_catalog_pins_student_books_and_numeric_split_order(self):
        catalog = self.engine().catalog()
        books = catalog["books"]
        self.assertEqual(catalog["commit"], "e2b3f62213c77bb8c33c5be355f97625ea1b8b61")
        self.assertGreater(len(books), 1500)
        self.assertEqual(len({book["book_id"] for book in books}), len(books))
        self.assertTrue(any(book["school_system"] == "五四学制" for book in books))
        self.assertTrue(any(len(book["sources"]) > 1 for book in books))
        for book in books:
            self.assertEqual(book["commit"], catalog["commit"])
            self.assertEqual(book["repository"], catalog["repository"])
            sources = book["sources"]
            if sources[0]["part"] is not None:
                self.assertEqual([source["part"] for source in sources], list(range(1, len(sources) + 1)))
            for source in sources:
                self.assertNotIn("教师用书", source["path"])
                self.assertNotIn("配套", source["path"])
                self.assertRegex(source["sha"], r"^[a-f0-9]{40}$")
                self.assertGreater(source["size"], 0)

    def test_exact_pep_selection_preserves_learning_focus(self):
        index = self.engine()
        result = index.resolve("请带我学人教版 PEP 三年级英语上册，重点学第一单元的问候语")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["focus"], "第一单元的问候语")
        book = result["book"]
        self.assertEqual(book["grade"], "三年级")
        self.assertEqual(book["volume"], "上册")
        self.assertIn("PEP", book["edition"])
        self.assertEqual(index.get(book["book_id"]), book)

    def test_unspecified_volume_and_edition_require_clarification(self):
        index = self.engine()
        result = index.resolve("三年级英语")
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("edition", result["clarify"])
        self.assertIn("volume", result["clarify"])
        result = index.resolve("人教版小学三年级英语上册")
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("edition", result["clarify"])

    def test_structured_school_system_filter_resolves_same_edition(self):
        index = self.engine()
        query = "青岛版三年级数学上册"
        result = index.resolve(query)
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("school_system", result["clarify"])
        result = index.resolve(query, school_system="五·四学制")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["book"]["school_system"], "五四学制")

    def test_high_school_required_module_and_a_b_edition_are_distinct(self):
        index = self.engine()
        result = index.resolve("高中人教版数学必修第一册")
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("edition", result["clarify"])
        result = index.resolve("高中人教A版数学必修1")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["book"]["volume"], "必修 第一册")
        self.assertEqual([source["part"] for source in result["book"]["sources"]], [1, 2])
        elective = index.resolve("高中人教A版数学选择性必修1")
        self.assertEqual(elective["status"], "matched")
        self.assertNotEqual(result["book"]["book_id"], elective["book"]["book_id"])

    def test_unknown_edition_year_and_learning_topic_never_pick_a_book(self):
        index = self.engine()
        for query in ("2026版人教版三年级数学上册", "三年级人教版数学上册最新版"):
            with self.subTest(query=query):
                result = index.resolve(query, allow_default=True)
                self.assertEqual(result["status"], "search_required")
                self.assertIsNone(result["book"])
                self.assertIn("三年级", result["search"]["web_queries"][0])
                self.assertIn("TapXWorld/ChinaTextbook", result["search"]["repository_query"])
        self.assertEqual(index.resolve("量子拓扑")["status"], "not_found")
        result = index.resolve("火星版三年级数学上册", edition="火星版")
        self.assertEqual(result["status"], "search_required")
        self.assertIn("火星版", result["search"]["web_queries"][0])
        with self.assertRaises(KeyError):
            index.get("made-up-id")

    def test_year_filter_matches_known_editions_and_preserves_unknown_candidates_for_research(self):
        index = self.engine()
        query = "人教版小学三年级数学上册"
        book = index.resolve(query)["book"]
        catalog = dict(index.catalog(), books=[book, dict(book, year=2025, book_id="ct-new")])
        with patch.object(index, "catalog", return_value=catalog):
            for suffix in ("2025版", "2025年版", "2025年7月第1版", "2025年新编"):
                with self.subTest(suffix=suffix):
                    result = index.resolve(query + suffix)
                    self.assertEqual(result["book"]["book_id"], "ct-new")
            result = index.resolve(query + "最新修订版，重点学倍的认识")
            self.assertEqual(result["status"], "search_required")
            self.assertEqual(result["search"]["version"], {"kind": "latest"})
            self.assertEqual(result["focus"], "倍的认识")
            result = index.resolve(query + "2026年印刷")
            self.assertEqual(result["search"]["version"], {"kind": "printing", "year": 2026})
            self.assertEqual(result["candidate_count"], 2)
            result = index.resolve("根据2022年版课程标准修订的" + query + "2025版")
            self.assertEqual(result["book"]["book_id"], "ct-new")

    def test_undated_catalog_candidates_do_not_satisfy_a_year_request(self):
        index = self.engine()
        result = index.resolve("人教版小学三年级上册数学，2025秋季版")
        self.assertEqual(result["status"], "search_required")
        self.assertEqual(result["search"]["version"], {"kind": "school_year", "year": 2025, "term": "autumn"})
        self.assertIn("2025", result["search"]["web_queries"][0])
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(index.resolve("最新版三年级数学")["status"], "needs_clarification")

    def test_opt_in_default_is_explicit_and_does_not_choose_a_volume(self):
        index = self.engine()
        vague = index.resolve("小学三年级数学")
        self.assertEqual(vague["status"], "needs_clarification")
        self.assertEqual(vague["defaults"], {})
        result = index.resolve("小学三年级数学上册", allow_default=True)
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["book"]["edition"], "人教版")
        self.assertEqual(result["defaults"], {"edition": "人教版"})
        result = index.resolve("小学三年级数学", allow_default=True)
        self.assertEqual(result["status"], "needs_clarification")
        self.assertIn("volume", result["clarify"])
