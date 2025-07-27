import sqlite3
from collections import Counter
from tabulate import tabulate

DB_PATH = 'vacantes.db'

def reporte_clasificacion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ✅ Necesario para acceder por nombre
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            es_procurement, 
            es_fit_usuario, 
            nivel_estimado 
        FROM vacantes
    """)
    filas = cur.fetchall()
    conn.close()

    if not filas:
        print("⚠️ No hay vacantes clasificadas aún.")
        return

    total = len(filas)
    resumen = Counter()

    for row in filas:
        es_proc = row["es_procurement"]
        es_fit = row["es_fit_usuario"]
        nivel = row["nivel_estimado"]

        key = (
            '✅' if es_proc else '❌' if es_proc == 0 else '⏳',
            '✅' if es_fit else '❌' if es_fit == 0 else '⏳',
            nivel if nivel else '⏳'
        )
        resumen[key] += 1

    tabla = []
    for (es_proc, es_fit, nivel), count in sorted(resumen.items(), key=lambda x: (-x[1])):
        tabla.append([es_proc, es_fit, nivel, count])

    print(tabulate(tabla, headers=["es_procurement", "es_fit_usuario", "nivel_estimado", "n"]))
    print(f"\nTotal vacantes: {total}")
