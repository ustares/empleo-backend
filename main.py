import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── Base de datos de prueba con fechas reales ─────────────────────────────────
# (Aquí irán tus resultados reales de Facebook/Apify más adelante)
MOCK_JOBS = [
    {
        "title": "Desarrollador Python - Remoto",
        "description": "Buscamos dev Python con experiencia en Flask y APIs REST.",
        "location": "Remoto",
        "url": "https://www.facebook.com/groups/empleos1/posts/1",
        "source_group": "Empleos Tech",
        "published_at": (datetime.now() - timedelta(hours=2)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Diseñador UX/UI Senior",
        "description": "Empresa internacional busca diseñador con experiencia en Figma.",
        "location": "Ciudad de México",
        "url": "https://www.facebook.com/groups/empleos1/posts/2",
        "source_group": "Diseño y Creatividad",
        "published_at": (datetime.now() - timedelta(hours=5)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Community Manager - Media Jornada",
        "description": "Se busca CM con experiencia en redes sociales y creación de contenido.",
        "location": "España",
        "url": "https://www.facebook.com/groups/empleos1/posts/3",
        "source_group": "Empleos Marketing",
        "published_at": (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Analista de Datos - Excel avanzado",
        "description": "Empresa de retail necesita analista con Python y Power BI.",
        "location": "Colombia",
        "url": "https://www.facebook.com/groups/empleos1/posts/4",
        "source_group": "Empleos Data",
        "published_at": (datetime.now() - timedelta(days=4)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Desarrollador Android Kotlin",
        "description": "Startup fintech busca dev Android con Jetpack Compose.",
        "location": "Argentina",
        "url": "https://www.facebook.com/groups/empleos1/posts/5",
        "source_group": "Empleos Tech",
        "published_at": (datetime.now() - timedelta(days=8)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Contador / Administrador",
        "description": "PYME busca contador con experiencia en facturación electrónica.",
        "location": "Chile",
        "url": "https://www.facebook.com/groups/empleos1/posts/6",
        "source_group": "Empleos Finanzas",
        "published_at": (datetime.now() - timedelta(days=20)).strftime("%d/%m/%Y %H:%M")
    },
    {
        "title": "Instructor de Idiomas Online",
        "description": "Academia busca profesores de inglés y francés para clases virtuales.",
        "location": "Remoto",
        "url": "https://www.facebook.com/groups/empleos1/posts/7",
        "source_group": "Empleos Educación",
        "published_at": (datetime.now() - timedelta(days=35)).strftime("%d/%m/%Y %H:%M")
    },
]

def get_cutoff_date(date_filter: str):
    """Retorna la fecha mínima según el filtro seleccionado."""
    now = datetime.now()
    if date_filter == "today":
        return now - timedelta(days=1)
    elif date_filter == "week":
        return now - timedelta(weeks=1)
    elif date_filter == "month":
        return now - timedelta(days=30)
    else:
        return None  # "all" — sin límite

@app.route('/')
def home():
    return jsonify({"status": "Backend Empleo FB activo ✅", "version": "2.0"})

@app.route('/search', methods=['POST'])
def search_jobs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400

    keyword     = data.get('keyword', '').strip().lower()
    country_code = data.get('country_code', '').strip().upper()
    date_filter = data.get('date_filter', 'all').strip().lower()

    if not keyword:
        return jsonify({"error": "keyword es requerido"}), 400

    cutoff = get_cutoff_date(date_filter)

    results = []
    for job in MOCK_JOBS:
        # ── Filtro por fecha ───────────────────────────────────────────────────
        if cutoff is not None:
            try:
                job_date = datetime.strptime(job["published_at"], "%d/%m/%Y %H:%M")
                if job_date < cutoff:
                    continue  # Oferta demasiado antigua, la omitimos
            except ValueError:
                pass  # Si el formato de fecha falla, incluimos la oferta

        # ── Filtro por keyword (título o descripción) ──────────────────────────
        title_match = keyword in job["title"].lower()
        desc_match  = keyword in job["description"].lower()
        group_match = keyword in job["source_group"].lower()

        if not (title_match or desc_match or group_match):
            continue

        results.append(job)

    return jsonify({
        "results": results,
        "total": len(results),
        "filters_applied": {
            "keyword": keyword,
            "country_code": country_code,
            "date_filter": date_filter
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
