def test_health_endpoint_ok():
    # Import your Flask app object
    from app import app

    client = app.test_client()
    resp = client.get("/health")

    assert resp.status_code == 200
    assert resp.get_data(as_text=True).strip() == "ok"