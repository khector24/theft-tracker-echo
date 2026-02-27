from unittest.mock import patch
from app import app


def test_analysis_with_mocked_db():
    client = app.test_client()

    # Patch the db query chain used inside /analysis
    with patch("app.db.session.query") as mock_query:
        # First query: total count
        mock_query.return_value.scalar.return_value = 5

        # Second query: group_by(...).all()
        mock_query.return_value.group_by.return_value.all.return_value = [
            ("theft", 3),
            ("other", 2),
        ]

        resp = client.get("/analysis")
        assert resp.status_code == 200

        data = resp.get_json()
        assert data["total_incidents"] == 5
        assert data["by_category"]["theft"] == 3
        assert data["by_category"]["other"] == 2