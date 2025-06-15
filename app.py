
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("API_FOOTBALL_KEY")
HEADERS = {
    "x-apisports-key": API_KEY
}
BASE_URL = "https://v3.football.api-sports.io"

def buscar_equipo_id(nombre):
    response = requests.get(f"{BASE_URL}/teams?search={nombre}", headers=HEADERS)
    data = response.json()
    if data["response"]:
        return data["response"][0]["team"]["id"]
    return None

def obtener_ultimos_partidos(equipo_id):
    response = requests.get(f"{BASE_URL}/teams/statistics?team={equipo_id}&season=2023&league=2", headers=HEADERS)
    return response.json()

@app.route("/analizar-partido", methods=["POST"])
def analizar_partido():
    datos = request.get_json()
    local = datos.get("local")
    visitante = datos.get("visitante")
    fecha = datos.get("fecha")
    estadio = datos.get("estadio")

    id_local = buscar_equipo_id(local)
    id_visitante = buscar_equipo_id(visitante)

    if not id_local or not id_visitante:
        return jsonify({"error": "No se encontraron los equipos"}), 400

    analisis = f"{local} y {visitante} se enfrentan en el estadio {estadio} el {fecha}. "
    analisis += f"{local} viene con motivación tras sus últimos partidos, mientras que {visitante} busca consolidarse defensivamente."

    factores_clave = [
        "Motivación y estado de forma reciente",
        "Historial de enfrentamientos previos",
        "Estilo de juego y efectividad ofensiva",
        "Defensas y goles recibidos",
    ]

    apuestas = [
        {
            "tipo": "PSG gana o empata (Doble oportunidad)",
            "cuota": 1.40,
            "explicacion": "El PSG tiene una ofensiva fuerte y podría al menos empatar este partido."
        },
        {
            "tipo": "Ambos equipos marcan (BTTS)",
            "cuota": 1.75,
            "explicacion": "Ambos equipos tienen capacidad goleadora y antecedentes de marcar en partidos importantes."
        },
        {
            "tipo": "Más de 2.5 goles",
            "cuota": 1.65,
            "explicacion": "Historial ofensivo sugiere un partido con varios goles."
        },
    ]

    noticias = [
        {"titulo": "Mbappé listo para liderar al PSG", "fuente": "Lequipe"},
        {"titulo": "Atlético confía en Griezmann y Morata", "fuente": "Marca"},
        {"titulo": "Rose Bowl será testigo de un gran duelo", "fuente": "ESPN"},
    ]

    return jsonify({
        "analisis": analisis,
        "factores": factores_clave,
        "apuestas": apuestas,
        "noticias": noticias
    })

if __name__ == "__main__":
    app.run(debug=True)
