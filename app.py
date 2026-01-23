from flask import Flask, request

app = Flask(__name__)

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
