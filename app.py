from flask import Flask, request, jsonify
from models import db, Incident
from datetime import datetime
import os
import time

# ---- super-simple in-memory metrics ----
START_TIME = time.time()
TOTAL_REQUESTS = 0
INCIDENTS_CREATED = 0

def create_app():
    app = Flask(__name__)

    # SQLite local, Postgres on Render via DATABASE_URL
    db_url = os.getenv("DATABASE_URL", "sqlite:///incidents.sqlite3")

    # Render Postgres sometimes uses postgres:// (SQLAlchemy wants postgresql://)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_request
    def count_requests():
        global TOTAL_REQUESTS
        TOTAL_REQUESTS += 1

    # ---------- Monitoring ----------
    @app.get("/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return "ok", 200
        except Exception as e:
            return f"db_error: {e}", 500

    @app.get("/metrics")
    def metrics():
        uptime_seconds = max(time.time() - START_TIME, 0.000001)
        rps = TOTAL_REQUESTS / uptime_seconds
        return jsonify({
            "status": "ok",
            "uptime_seconds": round(uptime_seconds, 2),
            "total_requests": TOTAL_REQUESTS,
            "requests_per_second": round(rps, 4),
            "incidents_created": INCIDENTS_CREATED,
        }), 200

    # ---------- Web app ----------
    @app.get("/")
    def home():
        return """
        <h2>Incident Tracker</h2>
        <form method="POST" action="/incidents">
          <label>Category:</label><br/>
          <select name="category">
            <option value="theft">theft</option>
            <option value="suspicious">suspicious</option>
            <option value="vandalism">vandalism</option>
            <option value="other">other</option>
          </select><br/><br/>
          <label>Description:</label><br/>
          <textarea name="description" style="width:420px;height:100px;"></textarea><br/><br/>
          <button type="submit">Submit Incident</button>
        </form>
        <p><a href="/incidents">View Dashboard</a></p>
        """

    @app.get("/incidents")
    def list_incidents():
        incidents = Incident.query.order_by(Incident.created_at.desc()).limit(50).all()
        rows = []
        for i in incidents:
            rows.append(
                f"<li><a href='/incidents/{i.id}'>Incident #{i.id}</a> "
                f"[{i.category}] status={i.status} created={i.created_at}</li>"
            )
        return "<h2>Dashboard</h2><ul>" + "".join(rows) + "</ul><p><a href='/'>Back</a></p>"

    @app.get("/incidents/<int:incident_id>")
    def incident_detail(incident_id: int):
        i = Incident.query.get_or_404(incident_id)
        return f"""
        <h2>Incident #{i.id}</h2>
        <p><b>Category:</b> {i.category}</p>
        <p><b>Description:</b> {i.description}</p>
        <p><b>Status:</b> {i.status}</p>
        <p><b>IP:</b> {i.ip or ""}</p>
        <p><b>City/Region/Country:</b> {i.city or ""} {i.region or ""} {i.country or ""}</p>
        <p><b>Created:</b> {i.created_at}</p>
        <p><b>Enriched:</b> {i.enriched_at or ""}</p>
        <p><a href="/incidents">Back to Dashboard</a></p>
        """

    # ---------- REST collaboration + Event messaging (publish job) ----------
    @app.post("/incidents")
    def create_incident():
        global INCIDENTS_CREATED
        category = request.form.get("category", "other").strip()
        description = request.form.get("description", "").strip()
        if not description:
            return "Description required", 400

        # best-effort client IP
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()

        inc = Incident(category=category, description=description, ip=ip, status="NEW")
        db.session.add(inc)
        db.session.commit()

        INCIDENTS_CREATED += 1

        # publish enrichment job (if REDIS_URL is configured)
        try:
            from tasks import enqueue_enrichment
            enqueue_enrichment(inc.id)
        except Exception:
            # still fine locally without Redis
            pass

        return f"<p>✅ Created incident #{inc.id}</p><p><a href='/incidents/{inc.id}'>View</a></p><p><a href='/'>Back</a></p>", 201

    # ---------- Analyzer ----------
    @app.get("/analysis")
    def analysis():
        total = db.session.query(db.func.count(Incident.id)).scalar() or 0
        by_category = db.session.query(Incident.category, db.func.count(Incident.id)) \
            .group_by(Incident.category).all()

        return jsonify({
            "total_incidents": total,
            "by_category": {k: v for k, v in by_category},
        }), 200

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
