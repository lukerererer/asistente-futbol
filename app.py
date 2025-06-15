from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/analizar-partido', methods=['POST'])
def analizar_partido():
    datos = request.get_json()
    local = datos.get('local')
    visitante = datos.get('visitante')
    fecha = datos.get('fecha')
    estadio = datos.get('estadio')

    analisis = f"{local} y {visitante} se enfrentan el {fecha} en el estadio {estadio}. Ambos equipos buscarán imponer su estilo."
    apuestas = [
        {
            "tipo": "Doble oportunidad",
            "cuota": 1.35,
            "explicacion": f"{local} o {visitante} tienen alta probabilidad de no perder, basados en sus últimos resultados."
        },
        {
            "tipo": "Ambos marcan",
            "cuota": 1.72,
            "explicacion": "Ambos equipos suelen anotar con regularidad. Esta apuesta es sólida por los antecedentes ofensivos."
        },
        {
            "tipo": "Más de 2.5 goles",
            "cuota": 1.90,
            "explicacion": "Los partidos recientes entre equipos similares superaron los 2.5 goles. Buen valor en esta cuota."
        }
    ]

    return jsonify({
        "analisis": analisis,
        "apuestas": apuestas
    })

@app.route('/openapi.yaml', methods=['GET'])
def serve_openapi_yaml():
    return send_from_directory(directory=os.getcwd(), path='openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
