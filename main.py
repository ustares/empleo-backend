from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "Backend Empleo FB activo ✅"})

@app.route('/search', methods=['POST'])
def search_jobs():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400

    keyword = data.get('keyword', '').strip()
    country_code = data.get('country_code', '').strip()

    if not keyword:
        return jsonify({"error": "keyword es requerido"}), 400

    # ── Aquí irá tu lógica real (Apify, scraping, DB, etc.) ──
    # Por ahora devuelve datos de ejemplo
    results = [
        {
            "title": f"Desarrollador {keyword} - Remoto",
            "description": f"Buscamos profesional de {keyword} con experiencia mínima de 2 años.",
            "location": f"{country_code}",
            "url": "https://www.facebook.com/groups/empleos.tech",
            "source_group": "Empleos Tech Latinoamérica"
        },
        {
            "title": f"{keyword} Senior - Trabajo desde casa",
            "description": "Excelente oportunidad para trabajar en equipo internacional.",
            "location": f"Remoto - {country_code}",
            "url": "https://www.facebook.com/groups/trabajoremoto",
            "source_group": "Trabajo Remoto Hispano"
        }
    ]

    return jsonify({"results": results, "total": len(results)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)