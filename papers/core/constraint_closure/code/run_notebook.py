"""TPP Launcher & Automated Notebook Execution Script for Paper Package 002.
Executes ../jupyter_notebooks/reviewer_constraint_closure_l1.ipynb and verifies solver outputs.
AuthorityEffect: None.
"""

import sys
import json
from pathlib import Path

# UTF-8 stdout reconfiguration for Windows console safety
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    code_dir = Path(__file__).resolve().parent
    notebook_path = code_dir.parent / "jupyter_notebooks" / "reviewer_constraint_closure_l1.ipynb"
    
    if not notebook_path.exists():
        print(f"ERROR: Notebook path {notebook_path} does not exist!")
        sys.exit(1)
        
    print(f"Reading reviewer notebook: {notebook_path.name}...")
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)
        
    print(f"Notebook loaded successfully: {len(nb_data['cells'])} cells found.")
    
    # `code/` is flat: one entry puts every solver, DDA, and diagnostic module
    # on the path.
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))
            
    # Execute code cells in isolated environment
    print("\n=== Executing Reviewer Notebook Cells ===")
    global_env = {}
    code_cell_count = 0
    for idx, cell in enumerate(nb_data["cells"]):
        if cell.get("cell_type") == "code":
            code_cell_count += 1
            code_str = "".join(cell.get("source", []))
            print(f"\n--- Running Code Cell {code_cell_count} ---")
            try:
                exec(code_str, global_env)
            except Exception as e:
                print(f"ERROR executing Cell {code_cell_count}: {e}")
                sys.exit(1)
                
    print("\n[OK] TPP Reviewer Notebook execution completed with 0 errors!")

if __name__ == "__main__":
    main()
