import os
import tempfile

from app import create_app
from models import db, Incident


def test_create_incident_and_shows_in_dashboard():
    # Create a temporary SQLite DB
    fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)

    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()

    # Create an incident
    resp = client.post(
        "/incidents",
        data={
            "category": "theft",
            "description": "Integration test incident",
        },
    )
    assert resp.status_code == 201

    # Verify it exists in the DB
    with app.app_context():
        assert Incident.query.count() == 1

    # Verify dashboard renders the incident
    dash = client.get("/incidents")
    assert dash.status_code == 200
    assert b"[theft]" in dash.data