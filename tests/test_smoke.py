import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH so `import app` and `import models` work in CI
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

def test_health_endpoint_ok():
    from app import app  # now works in CI
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200