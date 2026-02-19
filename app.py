import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Validador & Analista de Impacto", layout="wide")

st.title("🚀 Analista de Impacto: Inicio vs. Final")
st.markdown("Valida la participación y mide la evolución de tus proyectos de movilidad e inclusión.")

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
    
    score_inicio_col = st.sidebar.selectbox("Puntaje - Inicio", df_inicio.columns)
    score_final_col = st.sidebar.selectbox("Puntaje - Final", df_final.columns)

    # LIMPIEZA DE IDs
    df_inicio[id_inicio] = df_inicio[id_inicio].astype(str).str.strip().str.lower()
    df_final[id_final] = df_final[id_final].astype(str).str.strip().str.lower()

    # --- RENOMBRADO ESTRATÉGICO PARA EVITAR EL KEYERROR ---
    # Creamos copias con nombres fijos para el cálculo
    df_ini_clean = df_inicio.rename(columns={score_inicio_col: 'SCORE_INI_TEMP'})
    df_fin_clean = df_final.rename(columns={score_final_col: 'SCORE_FIN_TEMP'})

    # --- CRUCE DE DATOS ---
    # Unimos usando los IDs. Los nombres de columnas duplicados se manejarán con sufijos
    ambas = pd.merge(
        df_ini_clean, 
        df_fin_clean, 
        left_on=id_inicio, 
        right_on=id_final, 
        suffixes=('_hoja1', '_hoja2')
    )
    
    if not ambas.empty:
        # Ahora el cálculo es 100% seguro porque usamos los nombres fijos
        # Calculamos el impacto: Δ = Final - Inicial
        ambas['Diferencia'] = ambas['SCORE_FIN_TEMP'] - ambas['SCORE_INI_TEMP']

        # --- VISUALIZACIÓN ---
        st.divider()
        st.subheader("📊 Resumen de Impacto")
        
        avg_diff = ambas['Diferencia'].mean()
        m1, m2, m3 = st.columns(3)
        m1.metric("Participantes Completos", len(ambas))
        m2.metric("Mejora Promedio", f"{avg_diff:.2f} pts")
        m3.metric("Tasa de Retención", f"{(len(ambas)/len(df_inicio))*100:.1f}%")

        # Gráfico interactivo
        fig = px.bar(ambas, x=id_inicio, y='Diferencia', 
                     title="Evolución Individual de Puntajes",
                     color='Diferencia', color_continuous_scale='RdYlGn',
                     labels={'Diferencia': 'Cambio en Puntaje', id_inicio: 'Identificador'})
        st.plotly_chart(fig, use_container_width=True)

        # Mostrar tabla con nombres originales para claridad del usuario
        st.subheader("✅ Listado de Cumplimiento")
        # Mostramos los IDs y la diferencia calculada
        st.dataframe(ambas[[id_inicio, 'SCORE_INI_TEMP', 'SCORE_FIN_TEMP', 'Diferencia']]
                     .rename(columns={'SCORE_INI_TEMP': 'Puntaje Inicial', 'SCORE_FIN_TEMP': 'Puntaje Final'}))

        st.download_button("📥 Descargar Reporte Final",
