#!/usr/bin/env python3
"""
Basic tests for Mermaid-Astar API.

Run from repo root:
    python -m tests.test_a_star
or:
    python tests/test_a_star.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_DIR = REPO_ROOT / "api"
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

# Import astar-api despite hyphen
import importlib.util
api_path = API_DIR / "astar-api.py"
spec = importlib.util.spec_from_file_location("astar_api", api_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load astar_api from {api_path}")
astar_api = importlib.util.module_from_spec(spec)
sys.modules["astar_api"] = astar_api
spec.loader.exec_module(astar_api)

_as = astar_api
identify_start = astar_api.identify_start
identify_goal = astar_api.identify_goal


def load_grid():
    grid_path = API_DIR / "grid.json"
    with open(grid_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_search_home():
    grid = load_grid()
    nodes, path = _as.search(grid, "HOME")
    assert nodes >= 0
    assert path is not None
    start = identify_start(grid)
    goal = identify_goal(grid, "HOME")
    assert start is not None and goal is not None


def test_search_food():
    grid = load_grid()
    nodes, path = _as.search(grid, "FOOD")
    assert nodes >= 0
    assert path is not None


if __name__ == "__main__":
    test_search_home()
    test_search_food()
    print("All A* tests passed.")
