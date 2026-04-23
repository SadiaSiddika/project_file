from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- MYSQL CONFIG ----------------
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "thyroscan.db"   # FIXED (removed .db)

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# ---------------- SAVE HISTORY ----------------
@app.route("/save_history", methods=["POST"])
def save_history():
    data = request.get_json()

    patient_name = data.get("patient_name", "Unknown")
    timestamp = data.get("timestamp")
    prediction = data.get("prediction")
    probability = data.get("probability")

    if not timestamp:
        return jsonify({"status": "error", "message": "Missing timestamp"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO diagnosis_history 
            (patient_name, timestamp, prediction, probability)
            VALUES (%s, %s, %s, %s)
        """, (patient_name, timestamp, prediction, probability))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- GET HISTORY ----------------
@app.route("/get_history", methods=["GET"])
def get_history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT patient_name, timestamp, prediction, probability
        FROM diagnosis_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)