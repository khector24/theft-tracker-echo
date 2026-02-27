import importlib.util
from pathlib import Path

def load_flask_app():
    # Load app.py from repo root (works in CI + locally)
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    spec = importlib.util.spec_from_file_location("app_module", app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app

def test_health_endpoint_ok():
    app = load_flask_app()
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200