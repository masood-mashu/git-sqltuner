"""
eval_predictability.py - Checkpoint 02 Benchmark Suite for GitSqlTuner.
"""
import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.query_cost_analyzer import *
from tools.missing_index_advisor import *
from tools.sql_anti_pattern_detector import *

class TestGitSqlTunerPredictability(unittest.TestCase):
    def test_query_cost_analyzer(self):
        res = analyze_query_cost('{"total_cost": 420.5, "max_cost_budget": 1000.0}')
        self.assertEqual(res["status"], "COST_ACCEPTABLE")

    def test_missing_index_advisor(self):
        res = advise_missing_indexes('{"scan_type": "INDEX_SCAN", "row_count": 50000}')
        self.assertFalse(res["index_recommended"])
        self.assertEqual(res["status"], "INDEXING_OPTIMAL")

    def test_sql_anti_pattern_detector(self):
        res = detect_sql_anti_patterns("SELECT id, email, created_at FROM users WHERE email = 'test@example.com';")
        self.assertTrue(res["clean"])
        self.assertEqual(res["status"], "CLEAN_SYNTAX")


if __name__ == "__main__":
    unittest.main()
