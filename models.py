from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherSample(db.Model):
    __tablename__ = "weather_samples"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    location = db.Column(db.String(100), nullable=False)
    temperature_c = db.Column(db.Float, nullable=False)
    wind_speed_kmh = db.Column(db.Float, nullable=True)
