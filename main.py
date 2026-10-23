import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def make_jobs(keyword, country_code):
    """Genera resultados de prueba dinámicos basados en la búsqueda."""
    now = datetime.now()
    return [
        {
            "title": f"{keyword.title()} Junior - Trabajo Remoto",
            "description": f"Empresa busca perfil de {keyword} con 1 año de experiencia mínimo. Excelente ambiente laboral y salario competitivo.",
            "location": f"Remoto — {country_code}",
            "url": "https://www.facebook.com/groups/empleos.tech/posts/1001",
            "source_group": "Empleos Tech Latinoamérica",
            "published_at": (now - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M")
        },
        {
            "title": f"{keyword.title()} Senior - Tiempo completo",
            "description": f"Startup fintech necesita {keyword} con experiencia en equipos ágiles. Trabajo híbrido disponible.",
            "location": f"Ciudad principal — {country_code}",
            "url": "https://www.facebook.com/groups/empleos.tech/posts/1002",
            "source_group": "Trabajo Remoto Hispano",
            "published_at": (now - timedelta(hours=10)).strftime("%d/%m/%Y %H:%M")
        },
        {
            "title": f"Freelance {keyword.title()} — Proyecto 3 meses",
            "description": f"Proyecto de corta duración para {keyword}. Pago por horas, totalmente online.",
            "location": f"Online — {country_code}",
            "url": "https://www.facebook.com/groups/freelance.hispano/posts/2001",
            "source_group": "Freelancers Hispanos",
            "published_at": (now - timedelta(days=3)).strftime("%d/%m/%Y %H:%M")
        },
        {
            "title": f"Prácticas / Pasantía — {keyword.title()}",
            "description": f"Empresa líder ofrece prácticas remuneradas para estudiantes de {keyword}. Posibilidad de contratación.",
            "location": f"{country_code}",
            "url": "https://www.facebook.com/groups/practicas.trabajo/posts/3001",
            "source_group": "Prácticas y Pasantías",
            "published_at": (now - timedelta(days=6)).strftime("%d/%m/%Y %H:%M")
        },
        {
            "title": f"Director de {keyword.title()} — Empresa consolidada",
            "description": f"Posición de liderazgo para experto en {keyword} con más de 5 años de experiencia.",
            "location": f"Presencial — {country_code}",
            "url": "https://www.facebook.com/groups/empleos.directivos/posts/4001",
            "source_group": "Empleos Directivos",
            "published_at": (now - timedelta(days=12)).strftime("%d/%m/%Y %H:%M")
        },
        {
            "title": f"Media jornada — {keyword.title()}",
            "description": f"ONG busca voluntario/colaborador part-time con conocimientos en {keyword}.",
            "location": f"Remoto — {country_code}",
            "url": "https://www.facebook.com/groups/empleos.sociales/posts/5001",
            "source_group": "Empleos Sociales",
            "published_at": (now - timedelta(days=25)).strftime("%d/%m/%Y %H:%M")
        },
    ]

def get_cutoff_date(date_filter: str):
    now = datetime.now()
    if date_filter == "today":
        return now - timedelta(days=1)
    elif date_filter == "week":
        return now - timedelta(weeks=1)
    elif date_filter == "month":
        return now - timedelta(days=30)
    return None  # "all"

@app.route('/')
def home():
    return jsonify({"status": "Backend Empleo FB activo ✅", "version": "3.0"})

@app.route('/search', methods=['POST'])
def search_jobs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400

    keyword      = data.get('keyword', '').strip()
    country_code = data.get('country_code', 'ES').strip().upper()
    date_filter  = data.get('date_filter', 'all').strip().lower()

    if not keyword:
        return jsonify({"error": "keyword es requerido"}), 400

    # Generar resultados dinámicos para la keyword buscada
    all_jobs = make_jobs(keyword, country_code)

    # Aplicar filtro de fecha
    cutoff = get_cutoff_date(date_filter)
    if cutoff is not None:
        filtered = []
        for job in all_jobs:
            try:
                job_date = datetime.strptime(job["published_at"], "%d/%m/%Y %H:%M")
                if job_date >= cutoff:
                    filtered.append(job)
            except ValueError:
                filtered.append(job)
        all_jobs = filtered

    return jsonify({
        "results": all_jobs,
        "total": len(all_jobs)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
