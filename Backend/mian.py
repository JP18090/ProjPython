from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import psycopg2
import uuid

app = Flask(__name__)
CORS(app)

# === Configuração da conexão Postgres (Supabase) ===
DB_URL = "postgresql://postgres:Pedrito18090@db.nwfuwlcfcckzckeikrxb.supabase.co:5432/postgres"

def get_conn():
    return psycopg2.connect(DB_URL)

# === Endpoints ===

@app.route("/api/tariffs", methods=["GET"])
def get_tariffs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT vehicle_type, base_rate, fixed_hours, additional_hour_rate FROM tariffs;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    tarifas = [
        {"vehicleType": r[0], "baseRate": float(r[1]), "fixedHours": float(r[2]), "additionalHourRate": float(r[3])}
        for r in rows
    ]
    return jsonify(tarifas)

@app.route("/api/tariffs/<tipo>", methods=["PUT"])
def update_tariff(tipo):
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE tariffs
        SET base_rate=%s, fixed_hours=%s, additional_hour_rate=%s
        WHERE vehicle_type=%s
    """, (data["baseRate"], data["fixedHours"], data["additionalHourRate"], tipo))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Tarifa atualizada"})

@app.route("/api/vehicles", methods=["POST"])
def registrar_entrada():
    data = request.json
    vid = str(uuid.uuid4())
    now = datetime.now().isoformat()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO vehicles (id, plate, brand, model, year, color, vehicle_type, entry_time, active)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
    """, (vid, data["plate"], data["brand"], data["model"], data["year"], data["color"], data["vehicleType"], now))
    conn.commit()
    cur.close(); conn.close()

    data.update({"id": vid, "entryTime": now, "active": True})
    return jsonify(data), 201

@app.route("/api/vehicles/active", methods=["GET"])
def listar_ativos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, plate, brand, model, year, color, vehicle_type, entry_time FROM vehicles WHERE active=TRUE;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    veiculos = [
        {"id": r[0], "plate": r[1], "brand": r[2], "model": r[3], "year": r[4],
         "color": r[5], "vehicleType": r[6], "entryTime": r[7]} for r in rows
    ]
    return jsonify(veiculos)

@app.route("/api/vehicles/plate/<placa>", methods=["GET"])
def buscar_por_placa(placa):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, plate, brand, model, year, color, vehicle_type, entry_time FROM vehicles WHERE plate=%s AND active=TRUE;", (placa,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if row:
        veiculo = {"id": row[0], "plate": row[1], "brand": row[2], "model": row[3], "year": row[4],
                   "color": row[5], "vehicleType": row[6], "entryTime": row[7]}
        return jsonify(veiculo)
    return jsonify({"error": "Veículo não encontrado"}), 404

@app.route("/api/vehicles/<vid>/exit", methods=["PUT"])
def registrar_saida(vid):
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE vehicles 
        SET exit_time=%s, active=FALSE, payment_method=%s, amount_paid=%s
        WHERE id=%s
    """, (data["exitTime"], data["paymentMethod"], data["amountPaid"], vid))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Saída registrada", "amountPaid": data["amountPaid"]})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*), COALESCE(SUM(amount_paid),0), COUNT(*) FILTER (WHERE active=TRUE) FROM vehicles;")
    total, revenue, ativos = cur.fetchone()

    cur.execute("SELECT vehicle_type, COUNT(*), COALESCE(SUM(amount_paid),0) FROM vehicles GROUP BY vehicle_type;")
    rows = cur.fetchall()

    cur.close(); conn.close()

    vehiclesByType = {r[0]: r[1] for r in rows}
    revenueByType = {r[0]: float(r[2]) for r in rows}

    stats = {
        "totalVehicles": total,
        "totalRevenue": float(revenue),
        "activeVehicles": ativos,
        "vehiclesByType": vehiclesByType,
        "revenueByType": revenueByType
    }
    return jsonify(stats)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)

# script.js
# const API_BASE = 'http://localhost:5000/api';
