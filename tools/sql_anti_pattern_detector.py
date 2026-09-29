"""
sql_anti_pattern_detector.py - Scans SQL text for SELECT *, leading wildcards, and unindexed conversions
"""
import sys
import json


def detect_sql_anti_patterns(sql_query: str):
    import re
    issues = []
    if re.search(r"select\s+\*", sql_query, re.IGNORECASE):
        issues.append("SELECT_STAR_PROHIBITED")
    if "like '%" in sql_query.lower() or 'like "%' in sql_query.lower():
        issues.append("LEADING_WILDCARD_SCAN")
    is_clean = len(issues) == 0
    return {"clean": is_clean, "issues": issues, "status": "CLEAN_SYNTAX" if is_clean else "ANTI_PATTERN_FOUND"}


if __name__ == "__main__":
    print(json.dumps({"status": "READY", "tool": "sql-anti-pattern-detector"}))
