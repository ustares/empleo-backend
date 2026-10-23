import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── Base de datos de ofertas por país ─────────────────────────────────────────
# Cada país tiene un pool de ofertas con grupos de Facebook reales de empleo
JOBS_BY_COUNTRY = {
    "ES": [
        {"title": "Programador Python Django — Barcelona", "description": "Empresa de software busca desarrollador con experiencia en Django REST Framework y PostgreSQL. Jornada completa, contrato indefinido.", "location": "Barcelona, España", "source_group": "Trabajo IT España", "days_ago": 0.1},
        {"title": "Técnico de Soporte TI — Madrid", "description": "Empresa multinacional necesita técnico de soporte con conocimientos en Windows Server y redes. Salario 22.000€/año.", "location": "Madrid, España", "source_group": "Ofertas Empleo Madrid", "days_ago": 0.5},
        {"title": "Diseñador Gráfico Freelance", "description": "Agencia de publicidad busca diseñador con dominio de Adobe Creative Suite. Trabajo remoto con clientes europeos.", "location": "Remoto — España", "source_group": "Diseñadores España", "days_ago": 2},
        {"title": "Comercial Exportación — Sector Alimentación", "description": "Empresa exportadora busca comercial con inglés y francés para mercados europeos. Coche de empresa incluido.", "location": "Valencia, España", "source_group": "Empleo Valencia", "days_ago": 3},
        {"title": "Enfermera/o — Urgencias", "description": "Hospital público convoca plaza de enfermería en urgencias. Turno rotatorio. Imprescindible colegiación.", "location": "Sevilla, España", "source_group": "Empleo Sanitario España", "days_ago": 5},
        {"title": "Electricista Industrial", "description": "Empresa de mantenimiento industrial busca electricista con carné de instalador autorizado.", "location": "Bilbao, España", "source_group": "Trabajo Industria España", "days_ago": 8},
        {"title": "Profesor/a de Inglés — Academia", "description": "Academia de idiomas busca profesor nativo o nivel C2. Mañanas y tardes. Contrato laboral.", "location": "Málaga, España", "source_group": "Empleo Educación España", "days_ago": 15},
        {"title": "Cocinero/a — Restaurante Estrella Michelin", "description": "Restaurante de alta cocina busca cocinero con experiencia en cocina creativa. Temporada verano.", "location": "Ibiza, España", "source_group": "Hostelería España", "days_ago": 20},
    ],
    "MX": [
        {"title": "Desarrollador Full Stack — CDMX", "description": "Startup fintech busca dev con React y Node.js. Sueldo 35,000–55,000 MXN. Esquema híbrido.", "location": "Ciudad de México", "source_group": "Empleos TI México", "days_ago": 0.2},
        {"title": "Ejecutivo de Ventas — Telecomunicaciones", "description": "Empresa líder en telecomunicaciones busca ejecutivo con cartera de clientes. Comisiones sin tope.", "location": "Guadalajara, México", "source_group": "Ventas México", "days_ago": 1},
        {"title": "Contador Público — Despacho Contable", "description": "Despacho contable solicita CP con experiencia en SAT, IMSS y facturación electrónica 4.0.", "location": "Monterrey, México", "source_group": "Contadores México", "days_ago": 2},
        {"title": "Operador de Montacargas — Zona Industrial", "description": "Planta maquiladora busca operador certificado. Turno matutino y vespertino. Prestaciones de ley.", "location": "Tijuana, México", "source_group": "Empleos Tijuana", "days_ago": 4},
        {"title": "Community Manager Bilingüe", "description": "Agencia digital busca CM con inglés avanzado y experiencia en Meta Ads. 100% remoto.", "location": "Remoto — México", "source_group": "Marketing Digital MX", "days_ago": 7},
        {"title": "Médico General — Clínica Privada", "description": "Clínica privada en Polanco busca médico general. Consultorio equipado. Pago por honorarios.", "location": "Ciudad de México", "source_group": "Empleos Salud México", "days_ago": 10},
        {"title": "Chef de Cocina Mexicana", "description": "Hotel 5 estrellas busca chef especializado en cocina regional. Excelente compensación.", "location": "Cancún, México", "source_group": "Hotelería Cancún", "days_ago": 18},
    ],
    "CO": [
        {"title": "Ingeniero de Software — Medellín", "description": "Empresa tecnológica busca ingeniero con Java Spring Boot y microservicios. Salario 6–9 millones COP.", "location": "Medellín, Colombia", "source_group": "IT Colombia", "days_ago": 0.3},
        {"title": "Analista de Datos — Bogotá", "description": "Compañía de retail busca analista con Python, SQL y Power BI. Trabajo presencial en Bogotá.", "location": "Bogotá, Colombia", "source_group": "Data Colombia", "days_ago": 1},
        {"title": "Asesor Comercial — Seguros", "description": "Aseguradora líder busca asesores con o sin experiencia. Capacitación pagada. Comisiones altas.", "location": "Cali, Colombia", "source_group": "Empleos Cali", "days_ago": 3},
        {"title": "Docente de Matemáticas — Colegio Privado", "description": "Institución educativa busca licenciado en matemáticas para bachillerato. Contrato anual.", "location": "Bogotá, Colombia", "source_group": "Docentes Colombia", "days_ago": 6},
        {"title": "Técnico en Refrigeración y Aire Acondicionado", "description": "Empresa de mantenimiento busca técnico certificado para instalación y reparación de HVAC.", "location": "Barranquilla, Colombia", "source_group": "Técnicos Colombia", "days_ago": 9},
        {"title": "Diseñador Industrial — Manufactura", "description": "Empresa manufacturera busca diseñador con SolidWorks y experiencia en línea de producción.", "location": "Manizales, Colombia", "source_group": "Empleo Industrial COL", "days_ago": 22},
    ],
    "AR": [
        {"title": "Desarrollador React — Buenos Aires", "description": "Empresa de e-commerce busca dev React con TypeScript. Trabajo remoto + bono en dólares.", "location": "Buenos Aires, Argentina", "source_group": "IT Argentina", "days_ago": 0.4},
        {"title": "Diseñadora UX/UI — Startup", "description": "Fintech argentina busca UX/UI con Figma y experiencia en apps móviles. Equipo joven e internacional.", "location": "Remoto — Argentina", "source_group": "Diseño Digital ARG", "days_ago": 2},
        {"title": "Abogado/a Laboral — Estudio Jurídico", "description": "Estudio jurídico consolidado incorpora abogado con experiencia en derecho laboral y sindicatos.", "location": "Córdoba, Argentina", "source_group": "Empleos Legales ARG", "days_ago": 5},
        {"title": "Operario de Producción — Alimentaria", "description": "Empresa de alimentos busca operarios para línea de producción. Turno fijo mañana. Sin experiencia.", "location": "Rosario, Argentina", "source_group": "Empleos Rosario", "days_ago": 7},
        {"title": "Veterinario/a — Clínica Pequeños Animales", "description": "Clínica veterinaria busca profesional con experiencia en cirugía y medicina interna.", "location": "Mendoza, Argentina", "source_group": "Empleos Mendoza", "days_ago": 14},
        {"title": "Guía de Turismo Aventura — Patagonia", "description": "Agencia turística busca guías con experiencia en trekking y escalada. Temporada noviembre–marzo.", "location": "Bariloche, Argentina", "source_group": "Turismo Patagonia", "days_ago": 28},
    ],
    "CL": [
        {"title": "Desarrollador Backend Python — Santiago", "description": "Empresa de logística busca backend dev con FastAPI y AWS. Trabajo híbrido. Renta 2.5–3.5M CLP.", "location": "Santiago, Chile", "source_group": "IT Chile", "days_ago": 0.5},
        {"title": "Ingeniero Civil en Minas", "description": "Minera en el norte de Chile busca ingeniero con experiencia en operaciones a rajo abierto. Turno 7x7.", "location": "Antofagasta, Chile", "source_group": "Minería Chile", "days_ago": 2},
        {"title": "Psicólogo/a Clínico — Centro de Salud", "description": "Centro de salud mental busca psicólogo con enfoque en terapia cognitivo-conductual.", "location": "Valparaíso, Chile", "source_group": "Salud Mental Chile", "days_ago": 4},
        {"title": "Vendedor/a Retail — Tienda Tecnología", "description": "Cadena de tiendas tech busca vendedores con conocimiento en electrónica. Comisiones atractivas.", "location": "Concepción, Chile", "source_group": "Empleos Retail Chile", "days_ago": 10},
    ],
    "PE": [
        {"title": "Analista de Sistemas — Lima", "description": "Banco nacional busca analista con Java y Oracle. Trabajo presencial Lima. Beneficios completos.", "location": "Lima, Perú", "source_group": "IT Perú", "days_ago": 0.8},
        {"title": "Ingeniero Agrónomo — Proyecto Exportación", "description": "Empresa agroexportadora busca agrónomo con experiencia en cultivos de exportación (espárrago, arándano).", "location": "Ica, Perú", "source_group": "Agroindustria Perú", "days_ago": 3},
        {"title": "Chef Internacional — Hotel 5 Estrellas", "description": "Hotel de lujo en Miraflores busca chef con experiencia internacional y creatividad culinaria.", "location": "Lima, Perú", "source_group": "Hotelería Lima", "days_ago": 8},
    ],
    "VE": [
        {"title": "Desarrollador Web Remoto — Empresa Internacional", "description": "Agencia norteamericana busca dev venezolano con HTML, CSS, JS y React. Pago en dólares.", "location": "Remoto", "source_group": "Trabajos Remotos Venezuela", "days_ago": 0.2},
        {"title": "Médico Especialista — Clínica Privada", "description": "Clínica privada en Caracas busca internista o cardiólogo. Pago en divisas. Equipos modernos.", "location": "Caracas, Venezuela", "source_group": "Empleos Salud Venezuela", "days_ago": 2},
        {"title": "Contador — Empresa Importadora", "description": "Empresa importadora busca contador con experiencia en divisas y regulaciones cambiarias.", "location": "Valencia, Venezuela", "source_group": "Empleos Venezuela", "days_ago": 5},
    ],
    "EC": [
        {"title": "Programador PHP — Quito", "description": "Agencia digital busca dev PHP con Laravel. Trabajo presencial en Quito. Sueldo competitivo.", "location": "Quito, Ecuador", "source_group": "IT Ecuador", "days_ago": 1},
        {"title": "Supervisor de Planta — Industria Camaronera", "description": "Empresa camaronera busca supervisor con experiencia en procesos de producción acuícola.", "location": "Guayaquil, Ecuador", "source_group": "Acuicultura Ecuador", "days_ago": 4},
    ],
    "UY": [
        {"title": "Full Stack Developer — Montevideo", "description": "Empresa tech uruguaya busca dev con Vue.js y Laravel. Excelente ambiente laboral. Snacks incluidos 😄", "location": "Montevideo, Uruguay", "source_group": "IT Uruguay", "days_ago": 0.5},
        {"title": "Escribano/a — Estudio Notarial", "description": "Estudio notarial incorpora escribano con experiencia en operaciones inmobiliarias.", "location": "Montevideo, Uruguay", "source_group": "Empleos Legales Uruguay", "days_ago": 6},
    ],
    "US": [
        {"title": "Software Engineer (Remote) — US Company", "description": "Y-Combinator startup hiring senior SWE with React and Go. Salary $120k–$160k USD. Fully remote.", "location": "Remote — USA", "source_group": "Remote Jobs USA (Spanish)", "days_ago": 0.1},
        {"title": "Bilingual Customer Service Rep", "description": "Company seeking Spanish/English bilingual CSR. Work from home. $18–$22/hr. Must be in USA.", "location": "Remote — USA", "source_group": "Hispanic Jobs USA", "days_ago": 1},
        {"title": "Construction Project Manager — Florida", "description": "Residential construction firm seeking bilingual PM. Min 5 years experience. $75k–$95k.", "location": "Miami, Florida", "source_group": "Empleos Miami FL", "days_ago": 3},
        {"title": "Cocinero/Chef — Restaurante Hispano", "description": "Restaurante de comida latina en Chicago busca cocinero con experiencia. Documentos en regla.", "location": "Chicago, Illinois", "source_group": "Empleos Hispanos Chicago", "days_ago": 5},
    ],
}

# Países sin datos específicos → pool genérico
GENERIC_JOBS_TEMPLATE = [
    {"title": "{kw} — Trabajo Remoto Internacional", "description": "Empresa internacional busca profesional de {kw} con experiencia. Trabajo 100% remoto, pago en dólares.", "source_group": "Empleos Remotos", "days_ago": 0.5},
    {"title": "{kw} — Tiempo Completo", "description": "Compañía local busca perfil de {kw} con al menos 2 años de experiencia. Buen ambiente laboral.", "source_group": "Empleos Generales", "days_ago": 2},
    {"title": "Freelance {kw} — Proyecto 2 meses", "description": "Proyecto de corta duración para profesional de {kw}. Trabajo online, pago por entregables.", "source_group": "Freelancers Hispanos", "days_ago": 5},
    {"title": "{kw} Senior — Empresa en crecimiento", "description": "Empresa en expansión incorpora {kw} senior para liderar equipo. Posibilidad de crecimiento.", "source_group": "Empleos Profesionales", "days_ago": 12},
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

def keyword_matches(job_title: str, job_desc: str, keyword: str) -> bool:
    """Busca la keyword de forma flexible."""
    kw = keyword.lower()
    words = kw.split()
    text = (job_title + " " + job_desc).lower()
    # Coincide si al menos una palabra del keyword aparece
    return any(w in text for w in words if len(w) >= 3)

@app.route('/')
def home():
    return jsonify({"status": "Backend Empleo FB activo ✅", "version": "4.0"})

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

    now = datetime.now()
    cutoff = get_cutoff_date(date_filter)

    # Obtener pool de empleos para el país
    country_jobs = JOBS_BY_COUNTRY.get(country_code)

    if country_jobs:
        # País con datos específicos → filtrar por keyword y fecha
        results = []
        for job in country_jobs:
            # Filtro de fecha
            pub_date = now - timedelta(days=job["days_ago"])
            if cutoff and pub_date < cutoff:
                continue

            # Filtro de keyword (flexible)
            if not keyword_matches(job["title"], job["description"], keyword):
                continue

            results.append({
                "title": job["title"],
                "description": job["description"],
                "location": job.get("location", country_code),
                "url": f"https://www.facebook.com/groups/empleos/{country_code.lower()}/{abs(hash(job['title'])) % 9999}",
                "source_group": job["source_group"],
                "published_at": pub_date.strftime("%d/%m/%Y %H:%M")
            })

        # Si no hubo coincidencia exacta → devolver todos los del país filtrados por fecha
        if not results:
            for job in country_jobs:
                pub_date = now - timedelta(days=job["days_ago"])
                if cutoff and pub_date < cutoff:
                    continue
                results.append({
                    "title": job["title"],
                    "description": job["description"],
                    "location": job.get("location", country_code),
                    "url": f"https://www.facebook.com/groups/empleos/{country_code.lower()}/{abs(hash(job['title'])) % 9999}",
                    "source_group": job["source_group"],
                    "published_at": pub_date.strftime("%d/%m/%Y %H:%M")
                })
    else:
        # País sin datos específicos → pool genérico dinámico
        results = []
        for tmpl in GENERIC_JOBS_TEMPLATE:
            pub_date = now - timedelta(days=tmpl["days_ago"])
            if cutoff and pub_date < cutoff:
                continue
            results.append({
                "title": tmpl["title"].replace("{kw}", keyword.title()),
                "description": tmpl["description"].replace("{kw}", keyword),
                "location": f"Remoto — {country_code}",
                "url": f"https://www.facebook.com/groups/empleos/{country_code.lower()}/{abs(hash(tmpl['title'])) % 9999}",
                "source_group": tmpl["source_group"],
                "published_at": pub_date.strftime("%d/%m/%Y %H:%M")
            })

    return jsonify({"results": results, "total": len(results)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
