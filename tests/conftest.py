import sys
from pathlib import Path

# Always add the repo root to PYTHONPATH so `import app` works in CI
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))