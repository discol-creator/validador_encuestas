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
    df_inicio = pd.read_excel(file_inicio) if file_inicio.name.endswith('xlsx') else pd.read_csv(file_inicio)
    df_final = pd.read_excel(file_final) if file_final.name.endswith('xlsx') else pd.read_csv(file_final)

    # --- CONFIGURACIÓN ---
    st.sidebar.header("Configuración de Columnas")
    id_inicio = st.sidebar.selectbox("ID (Email/Cédula) - Inicio", df_inicio.columns)
    id_final = st.sidebar.selectbox("ID (Email/Cédula) - Final", df_final.columns)
    
    score_inicio = st.sidebar.selectbox("Puntaje - Inicio", df_inicio.columns)
    score_final = st.sidebar.selectbox("Puntaje - Final", df_final.columns)

    # Limpieza
    df_inicio[id_inicio] = df_inicio[id_inicio].astype(str).str.strip().lower()
    df_final[id_final] = df_final[id_final].astype(str).str.strip().lower()

    # --- CRUCE DE DATOS ---
    # Realizamos un inner join para encontrar quiénes hicieron ambas
    ambas = pd.merge(df_inicio, df_final, left_on=id_inicio, right_on=id_final, suffixes=('_ini', '_fin'))
    
    # Cálculo de impacto: Diferencia = Puntaje Final - Puntaje Inicial
    ambas['Diferencia'] = ambas[score_final] - ambas[score_inicio]

    # --- VISUALIZACIÓN ---
    st.divider()
    st.subheader("📊 Resumen de Impacto")
    
    avg_diff = ambas['Diferencia'].mean()
    m1, m2 = st.columns(2)
    m1.metric("Participantes Completos", len(ambas))
    m2.metric("Mejora Promedio", f"{avg_diff:.2f} pts")

    # Gráfico de impacto
    fig = px.bar(ambas, x=id_inicio, y='Diferencia', 
                 title="Diferencia de Puntaje por Participante",
                 color='Diferencia', color_continuous_scale='RdYlGn',
                 labels={'Diferencia': 'Δ Puntaje'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("✅ Listado de Cumplimiento")
    st.dataframe(ambas[[id_inicio, score_inicio, score_final, 'Diferencia']])

    # Botón de descarga
    st.download_button("Descargar Reporte Completo (CSV)", ambas.to_csv(index=False), "reporte_impacto.csv")
else:
    st.info("💡 Esperando la carga de ambos archivos para procesar el impacto...")
