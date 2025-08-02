from numpy import full
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- Configuración ---
DB_PATH = "vacantes.db"

# --- Cargar datos ---
@st.cache_data(ttl=60)
def cargar_datos():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    vacantes = pd.read_sql_query("SELECT * FROM vacantes", conn)
    empresas = pd.read_sql_query("SELECT * FROM empresas", conn)
    conn.close()
    fulldf = pd.merge(vacantes, empresas, on="company", how="left")
    return vacantes, empresas, fulldf

def filtrar_con_keywords(df, columna, texto_raw):
    if not texto_raw:
        return df
    keywords = [kw.strip() for kw in texto_raw.split(',') if kw.strip()]
    patron = '|'.join(keywords)
    return df[df[columna].fillna('').str.lower().str.contains(patron)]



vacantes, empresas, fulldf = cargar_datos()

# --- Título principal ---
st.set_page_config(layout="wide")

st.title("📊 Visor de Vacantes Analizadas")

# --- Panel de resumen general ---
st.header("Resumen general")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vacantes totales", len(vacantes))

with col2:
    st.metric("Empresas únicas", empresas['company'].nunique())

with col3:
    missing_empresas = vacantes[~vacantes['company'].isin(empresas['company'])]['company'].nunique()
    st.metric("Empresas sin datos", missing_empresas)

# --- Filtros ---
st.sidebar.header("Filtros")
score_min = st.sidebar.slider("Score mínimo", min_value=0, max_value=120, value=85, step=5)
filtro_lugar = st.sidebar.text_input("📍 Filtrar por lugar (puedes usar múltiples, separados por coma)").strip().lower()
filtro_empresa = st.sidebar.text_input("🏢 Filtrar por empresa (puedes usar múltiples, separados por coma)").strip().lower()



# --- Aplicar filtros ---
df_filtrado = fulldf.copy()
df_filtrado = df_filtrado[df_filtrado['score_total'] >= score_min]
#df_filtrado = df_filtrado[df_filtrado['modalidad_trabajo'].isin(modalidad_filtro)]
df_filtrado = filtrar_con_keywords(df_filtrado, 'location', filtro_lugar)
df_filtrado = filtrar_con_keywords(df_filtrado, 'company', filtro_empresa)



def formatear_link(url):
    if not url:
        return ""
    return f"[🔗 Ver]({url})"

df_filtrado['link_click'] = df_filtrado['link'].apply(formatear_link)

# --- Tabla de resultados ---
st.subheader("Vacantes filtradas")
st.caption(f"Mostrando {len(df_filtrado)} vacantes con score >= {score_min}")

columnas_mostrar = ['score_total', 'categoria_fit', 'title', 'company','sector_empresa',  'location', 'presencia_mexico', 'es_procurement', 'es_fit_usuario', 'nivel_estimado','link']

st.markdown(
    df_filtrado[columnas_mostrar]
    .sort_values(by='score_total', ascending=False)
    .to_markdown(index=False),
    unsafe_allow_html=True

)

# --- Detalle expandible ---
st.subheader("Detalle por vacante")
for _, row in df_filtrado.iterrows():
    with st.expander(f"{row['title']} – {row['company']} [{row['score_total']}]"):
        st.markdown(f"**Ubicación:** {row['location']}")
        st.markdown(f"**Modalidad:** {row['modalidad_trabajo']}")
        st.markdown(f"**Nivel estimado:** {row['nivel_estimado']}")
        st.markdown(f"**Fit usuario:** {'✅' if row['es_fit_usuario'] else '❌'}")
        st.markdown(f"**Es procurement:** {'✅' if row['es_procurement'] else '❌'}")
        st.markdown("**Descripción completa:**")
        st.text(row['job_description'] or row.get('full_text', 'Sin descripción'))