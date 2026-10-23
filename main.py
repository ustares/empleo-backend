from datetime import datetime, timedelta

@app.route('/search', methods=['POST'])
def search_jobs():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    country_code = data.get('country_code', '').strip()
    date_filter = data.get('date_filter', 'all')  # ← NUEVO

    # Lógica de filtro por fecha
    now = datetime.now()
    if date_filter == 'today':
        since = now - timedelta(days=1)
    elif date_filter == 'week':
        since = now - timedelta(weeks=1)
    elif date_filter == 'month':
        since = now - timedelta(days=30)
    else:
        since = None  # "all" = sin filtro

    # Aquí aplicas el filtro a tu fuente de datos
    # Cada resultado debe incluir "published_at": "hace 2 horas"
    results = [...]

    return jsonify({"results": results, "total": len(results)})
