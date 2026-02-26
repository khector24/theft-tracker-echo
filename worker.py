import os
import requests
from datetime import datetime
from redis import Redis
from rq import Worker, Queue, Connection

from app import create_app
from models import db, Incident

def enrich_incident(incident_id: int):
    """
    Worker job:
    - calls external API (ipapi.co) using incident.ip
    - writes enrichment fields back to DB
    """
    app = create_app()
    with app.app_context():
        inc = Incident.query.get(incident_id)
        if not inc:
            return

        inc.status = "ENRICHING"
        db.session.commit()

        try:
            ip = inc.ip or ""
            # Free external API: https://ipapi.co/<ip>/json/
            data = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10).json()

            inc.city = data.get("city")
            inc.region = data.get("region")
            inc.country = data.get("country_name")
            inc.status = "ENRICHED"
            inc.enriched_at = datetime.utcnow()
            db.session.commit()
        except Exception:
            inc.status = "FAILED"
            db.session.commit()

if __name__ == "__main__":
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL not set.")

    redis_conn = Redis.from_url(redis_url)
    with Connection(redis_conn):
        worker = Worker([Queue("incident-jobs")])
        worker.work()