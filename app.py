from flask import Flask
import os
app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/")
def home():
    return {"service": "shopnow-api-v2", "env": os.getenv("APP_ENV", "dev")}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
