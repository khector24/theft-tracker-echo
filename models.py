from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    category = db.Column(db.String(50), nullable=False)   # theft, suspicious, vandalism, etc.
    description = db.Column(db.Text, nullable=False)

    # enrichment fields (filled by worker)
    status = db.Column(db.String(20), default="NEW", nullable=False)  # NEW, ENRICHING, ENRICHED, FAILED
    ip = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    enriched_at = db.Column(db.DateTime, nullable=True)