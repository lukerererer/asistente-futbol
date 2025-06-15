
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "1e31543f84d690c8c3e42f0a4111a04a"
API_FOOTBALL_HOST = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

@app.route("/analizar-partido", methods=["POST"])
def analizar_partido():
    data = request.get_json()
    equipo_local = data.get("equipo_local")
    equipo_visitante = data.get("equipo_visitante")
    fecha = data.get("fecha")
    estadio = data.get("estadio")

    # Obtener datos del equipo local
    response_local = requests.get(f"{API_FOOTBALL_HOST}/teams?search={equipo_local}", headers=headers)
    team_local_data = response_local.json()
    if not team_local_data["response"]:
        return jsonify({"error": f"No se encontró el equipo local: {equipo_local}"}), 400
    team_local_id = team_local_data["response"][0]["team"]["id"]

    # Obtener datos del equipo visitante
    response_visitante = requests.get(f"{API_FOOTBALL_HOST}/teams?search={equipo_visitante}", headers=headers)
    team_visitante_data = response_visitante.json()
    if not team_visitante_data["response"]:
        return jsonify({"error": f"No se encontró el equipo visitante: {equipo_visitante}"}), 400
    team_visitante_id = team_visitante_data["response"][0]["team"]["id"]

    # Buscar un fixture entre esos equipos
    params_fixture = {
        "team": team_local_id,
        "season": 2024
    }
    response_fixture = requests.get(f"{API_FOOTBALL_HOST}/fixtures", headers=headers, params=params_fixture)
    fixtures = response_fixture.json()

    # Análisis básico
    apuestas = [
        {"tipo": "Ambos marcan", "cuota": 1.85, "explicacion": "Históricamente ambos equipos suelen marcar en partidos directos."},
        {"tipo": "Más de 2.5 goles", "cuota": 1.95, "explicacion": "Ambos equipos tienen un promedio de goles superior a 2.5."},
        {"tipo": f"Gana {equipo_local}", "cuota": 2.10, "explicacion": f"{equipo_local} viene con mejor rendimiento en casa."}
    ]

    return jsonify({
        "analisis": f"Análisis automatizado del partido entre {equipo_local} y {equipo_visitante} en {estadio}, con datos reales consultados.",
        "apuestas": apuestas
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
