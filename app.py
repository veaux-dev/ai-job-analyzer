import streamlit as st
import sqlite3
from datetime import datetime
from modules.run_scraper import run_scraper
from modules.empresa_info import llenar_tabla_empresas
from modules.classifier import clasificar_empresas

DB_PATH = "vacantes.db"

st.set_page_config(page_title="AI Job Analyzer", layout="wide")

st.title("📊 AI Job Analyzer – Dashboard Local")

# Ejecutar el scraper
if st.button("🔍 Ejecutar Scraper (LinkedIn)"):
    run_scraper()
    st.success("✅ Scraping completado.")# Ejecutar el scraper

# Extrae las expresas de las vacantes (unicas)
if st.button("🔍 Extraer Empresas de Vacantes"):
    llenar_tabla_empresas()
    st.success("✅ Extraccion completado.")

if st.button("🏢 Clasificar todas las empresas"):
    progress = st.progress(0)
    status = st.empty()

    with st.spinner("⏳ Clasificando empresas desde vacantes..."):
        clasificar_empresas(report_callback={"progress": progress, "status": status})

    st.success("🎉 Clasificación completada.")

# Leer la base de datos
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Conteo total
c.execute("SELECT COUNT(*) FROM vacantes")
total = c.fetchone()[0]

# Nuevas hoy
today = datetime.today().strftime("%Y-%m-%d")
c.execute("SELECT COUNT(*) FROM vacantes WHERE date = ?", (today,))
nuevas = c.fetchone()[0]

st.markdown(f"**🧮 Total de vacantes:** {total}")
st.markdown(f"**🆕 Nuevas hoy:** {nuevas}")

# Últimas 10 vacantes
c.execute("""
    SELECT title, company, date, modalidad_trabajo
    FROM vacantes
    ORDER BY date DESC
    LIMIT 10
""")
rows = c.fetchall()

if rows:
    st.markdown("### 🧾 Últimas vacantes registradas")
    st.table(rows)
else:
    st.info("No hay vacantes aún en la base.")

conn.close()
