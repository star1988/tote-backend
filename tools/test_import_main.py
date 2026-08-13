import importlib
import sys
from pathlib import Path

# Ensure project root is on sys.path so `main` is importable
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

try:
    m = importlib.import_module("main")
    print(m.__file__, hasattr(m, "app"))
except Exception as e:
    print("IMPORT_ERROR:", e)
    sys.exit(1)
