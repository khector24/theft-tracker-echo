from flask import Flask, request, jsonify
from models import db
import time

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ---- super-simple in-memory metrics ----
START_TIME = time.time()
TOTAL_REQUESTS = 0

@app.before_request
def count_requests():
    global TOTAL_REQUESTS
    TOTAL_REQUESTS += 1

# ----------------- required endpoints -----------------

@app.get("/health")
def health():
    # Just needs to return 200 OK
    return "ok", 200

@app.get("/metrics")
def metrics():
    # "requests per second" = total requests / uptime seconds
    uptime_seconds = max(time.time() - START_TIME, 0.000001)
    rps = TOTAL_REQUESTS / uptime_seconds

    return jsonify({
        "status": "ok",
        "uptime_seconds": round(uptime_seconds, 2),
        "total_requests": TOTAL_REQUESTS,
        "requests_per_second": round(rps, 4),
    }), 200

# ----------------- your existing routes -----------------

@app.get("/")
def home():
    return """
    <h2>Echo App</h2>
    <form method="POST" action="/echo">
      <label>Type something:</label><br/>
      <input name="message" placeholder="Hello world" style="width:320px;padding:8px;" />
      <button type="submit" style="padding:8px 12px;">Submit</button>
    </form>
    """

@app.post("/echo")
def echo():
    msg = request.form.get("message", "").strip()
    if not msg:
        msg = "(no input provided)"
    return f"""
    <h2>Echo Result</h2>
    <p><b>You typed:</b> {msg}</p>
    <a href="/">Back</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

