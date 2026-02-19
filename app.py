import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Validador & Analista de Impacto", layout="wide")

st.title("🚀 Analista de Impacto: Inicio vs. Final")
st.markdown("Carga tus archivos para validar la participación y medir la evolución.")

col1, col2 = st.columns(2)
with col1:
    file_inicio = st.file_uploader("Encuesta INICIAL", type=['xlsx', 'csv'])
with col2:
    file_final = st.file_uploader("Encuesta FINAL", type=['xlsx', 'csv'])

if file_inicio and file_final:
    # Cargar datos
    df_inicio = pd.read_excel(file_inicio) if file_inicio.name.endswith('xlsx') else pd.read_csv(file_inicio)
    df_final = pd.read_excel(file_final) if file_final.name.endswith('xlsx') else pd.read_csv(file_final)

    # --- CONFIGURACIÓN EN BARRA LATERAL ---
    st.sidebar.header("⚙️ Configuración")
    id_inicio = st.sidebar.selectbox("ID (Email/Cédula) - Inicio", df_inicio.columns)
    id_final = st.sidebar.selectbox("ID (Email/Cédula) - Final", df_final.columns)
    
    score_inicio = st.sidebar.selectbox("Puntaje - Inicio", df_inicio.columns)
    score_final = st.sidebar.selectbox("Puntaje - Final", df_final.columns)

    # LIMPIEZA DE DATOS (Aquí estaba el error corregido)
    df_inicio[id_inicio] = df_inicio[id_inicio].astype(str).str.strip().str.lower()
    df_final[id_final] = df_final[id_final].astype(str).str.strip().str.lower()

    # --- CRUCE DE DATOS ---
    ambas = pd.merge(df_inicio, df_final, left_on=id_inicio, right_on=id_final, suffixes=('_ini', '_fin'))
    
    if not ambas.empty:
        # Cálculo de impacto
        ambas['Diferencia'] = ambas[score_final] - ambas[score_inicio]

        # --- VISUALIZACIÓN ---
        st.divider()
        st.subheader("📊 Resumen de Impacto")
        
        avg_diff = ambas['Diferencia'].mean()
        m1, m2, m3 = st.columns(3)
        m1.metric("Participantes Completos", len(ambas))
        m2.metric("Mejora Promedio", f"{avg_diff:.2f} pts")
        m3.metric("Tasa de Retención", f"{(len(ambas)/len(df_inicio))*100:.1f}%")

        # Gráfico
        fig = px.bar(ambas, x=id_inicio, y='Diferencia', 
                     title="Evolución Individual de Puntajes",
                     color='Diferencia', color_continuous_scale='RdYlGn',
                     labels={'Diferencia': 'Cambio en Puntaje', id_inicio: 'Identificador'})
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("✅ Listado de Cumplimiento")
        st.dataframe(ambas[[id_inicio, score_inicio, score_final, 'Diferencia']])

        st.download_button("📥 Descargar Reporte Final", ambas.to_csv(index=False), "reporte_impacto.csv")
    else:
        st.warning("⚠️ No se encontraron coincidencias entre ambos archivos. Revisa si la columna de ID es la correcta en ambos.")
else:
    st.info("👋 ¡Hola Francisco! Sube las dos encuestas para empezar el análisis de impacto.")
