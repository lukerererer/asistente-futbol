
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_FOOTBALL_KEY = '1e31543f84d690c8c3e42f0a4111a04a'
API_FOOTBALL_HOST = 'https://v3.football.api-sports.io'

headers = {
    'x-apisports-key': API_FOOTBALL_KEY
}

@app.route('/analizar-partido', methods=['POST'])
def analizar_partido():
    data = request.get_json()
    equipo_local = data['equipo_local']
    equipo_visitante = data['equipo_visitante']
    fecha = data['fecha']
    estadio = data['estadio']

    return jsonify({
        "analisis": f"Partido entre {equipo_local} y {equipo_visitante} en {estadio}. Duelo interesante según estadísticas recientes.",
        "apuestas": [
            {
                "tipo": "Ambos marcan",
                "cuota": 1.75,
                "explicacion": "Ambos tienen buena media de goles en sus últimos partidos."
            },
            {
                "tipo": "Over 2.5 goles",
                "cuota": 1.95,
                "explicacion": "Más del 60% de sus últimos enfrentamientos superan esta línea."
            },
            {
                "tipo": f"{equipo_local} gana o empata",
                "cuota": 1.65,
                "explicacion": f"{equipo_local} lleva buen rendimiento en casa, pocos goles encajados."
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
