import os
import psycopg
from flask import Flask, request

app = Flask(__name__)

# Toute la connexion vient de variables d'environnement : aucune valeur en dur
def get_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "shopnow"),
        user=os.getenv("DB_USER", "shopnow"),
        password=os.getenv("DB_PASSWORD", ""),
    )

def init_db():
    with get_conn() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, product TEXT NOT NULL)")

# Le health check vérifie aussi la base : si elle est injoignable, on renvoie une erreur 503
@app.route("/health")
def health():
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "error", "db": str(e)}, 503

@app.route("/")
def home():
    return {"service": "shopnow-api", "env": os.getenv("APP_ENV", "dev")}

@app.route("/orders", methods=["GET"])
def list_orders():
    init_db()
    with get_conn() as conn:
        rows = conn.execute("SELECT id, product FROM orders ORDER BY id").fetchall()
    return {"orders": [{"id": r[0], "product": r[1]} for r in rows]}

@app.route("/orders", methods=["POST"])
def create_order():
    init_db()
    product = request.json.get("product")
    with get_conn() as conn:
        row = conn.execute("INSERT INTO orders (product) VALUES (%s) RETURNING id", (product,)).fetchone()
    return {"id": row[0], "product": product}, 201
