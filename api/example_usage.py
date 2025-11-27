import json
import sys
from pathlib import Path
import importlib.util

# Ensure local api modules resolve when run from repo root or api/
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

# Import astar-api.py despite hyphen
api_path = THIS_DIR / "astar-api.py"
spec = importlib.util.spec_from_file_location("astar_api", api_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load astar_api from {api_path}")
astar_api = importlib.util.module_from_spec(spec)
sys.modules["astar_api"] = astar_api
spec.loader.exec_module(astar_api)

search = astar_api.search
draw_grid = astar_api.draw_grid
identify_start = astar_api.identify_start
identify_goal = astar_api.identify_goal
next_action_from_path = astar_api.next_action_from_path
encode_action_ascii = astar_api.encode_action_ascii

def main():
    # ---- 1. Load grid.json ----
    grid_path = THIS_DIR / "grid.json"
    with open(grid_path, "r", encoding="utf-8") as f:
        grid = json.load(f)

    print("Loaded grid.json\n")
    # ---- 2. Choose which goal you want to search for ----
    # Options: "FOOD" or "HOME"
    GOAL_TYPE = "HOME"

    # ---- 4. Run A* ----
    nodes, path = _as.search(grid, GOAL_TYPE)
    print(f"Nodes expanded: {nodes}")

     # ---- 5. For Visualisation A* ----
    start = identify_start(grid)
    print(f"Start position (Crab): {start}")
    goal = identify_goal(grid, goal_type="HOME")
    print(f"Goal position: {goal}\n")

    if path:
        print("Path found!\n")
        draw_grid(grid, path, start, goal)
    else:
        print("No path found.")
        draw_grid(grid, path, start, goal)
        exit()

    # ---- EXTRA 6. Calculate next action based on path ----
    init_heading = 'N'  # Initial heading

    action, init_heading = next_action_from_path(
        path,
        init_heading=init_heading,
        allow_back=False
    )

    print("Next action:", action)

    # ---- 7. Convert to ASCII command ----
    tx = encode_action_ascii(action)
    print("TX string:", tx)


if __name__ == "__main__":
    main()
