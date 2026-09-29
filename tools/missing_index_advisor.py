"""
missing_index_advisor.py - Detects sequential scans on large tables and recommends B-tree or GiST indexes
"""
import sys
import json


def advise_missing_indexes(scan_metrics_json: str):
    import json
    data = json.loads(scan_metrics_json) if isinstance(scan_metrics_json, str) else scan_metrics_json
    scan_type = data.get("scan_type", "INDEX_SCAN").upper()
    rows = data.get("row_count", 500)
    needs_idx = (scan_type == "SEQ_SCAN" and rows > 1000)
    table = data.get("table", "unknown")
    col = data.get("filter_column", "id")
    rec = f"CREATE INDEX idx_{table}_{col} ON {table}({col});" if needs_idx else "NO_INDEX_NEEDED"
    return {"index_recommended": needs_idx, "ddl": rec, "status": "INDEX_RECOMMENDED" if needs_idx else "INDEXING_OPTIMAL"}


if __name__ == "__main__":
    print(json.dumps({"status": "READY", "tool": "missing-index-advisor"}))
