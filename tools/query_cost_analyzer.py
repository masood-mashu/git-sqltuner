"""
query_cost_analyzer.py - Parses execution plan total cost and validates against organizational SLA threshold
"""
import sys
import json


def analyze_query_cost(plan_json: str):
    import json
    data = json.loads(plan_json) if isinstance(plan_json, str) else plan_json
    cost = data.get("total_cost", 150.0)
    limit = data.get("max_cost_budget", 1000.0)
    is_acceptable = cost <= limit
    return {"total_cost": cost, "budget": limit, "status": "COST_ACCEPTABLE" if is_acceptable else "HIGH_COST_PLAN"}


if __name__ == "__main__":
    print(json.dumps({"status": "READY", "tool": "query-cost-analyzer"}))
