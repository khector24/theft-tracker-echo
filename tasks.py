import os
from redis import Redis
from rq import Queue

def _queue():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL not set (needed for queue).")
    redis_conn = Redis.from_url(redis_url)
    return Queue("incident-jobs", connection=redis_conn)

def enqueue_enrichment(incident_id: int):
    q = _queue()
    q.enqueue("worker.enrich_incident", incident_id)