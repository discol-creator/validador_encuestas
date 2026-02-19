import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="Validador de Impacto", layout="wide")

st.title("🚀 Analista de Impacto: Inicio vs. Final")
st.markdown("Herramienta interactiva para validar la participación y evolución de usuarios.")

# 1. Carga de archivos
col1, col2 = st.columns(2)
with col1:
    file_inicio = st.file_uploader("Encuesta INICIAL", type=['xlsx', 'csv'])
with col2:
    file_final = st.file_uploader("Encuesta FINAL", type=['xlsx', 'csv'])

if file_inicio and file_final:
    # Leer datos
    if file_inicio.name.endswith('xlsx'):
        df_inicio = pd.read_excel(file_inicio)
    else:
        df_inicio = pd.read_csv(file_inicio)
        
    if file_final.name.endswith('xlsx'):
        df_final = pd.read_excel(file_final)
    else:
        df_final = pd.read_csv(file_final)

    # 2. Configuración en la barra lateral
    st.sidebar.header("⚙️ Configuración")
    id_ini_col = st.sidebar.selectbox("ID (Email/Cédula) - Inicio", df_inicio.columns)
    id_fin_col = st.sidebar.selectbox("ID (Email/Cédula) - Final", df_final.columns)
    
    score_ini_col = st.sidebar.selectbox("Puntaje - Inicio", df_inicio.columns)
    score_fin_col = st.sidebar.selectbox("Puntaje - Final", df_final.columns)

    # 3. Limpieza de identificadores
    df_inicio[id_ini_col] = df_inicio[id_ini_col].astype(str).str.strip().str.lower()
    df_final[id_fin_col] = df_final[id_fin_col].astype(str).str.strip().str.lower()

    # 4. Renombrado para evitar conflictos
    df_ini_ready = df_inicio.rename(columns={score_ini_col: 'PUNTO_INICIAL'})
    df_fin_ready = df_final.rename(columns={score_fin_col: 'PUNTO_FINAL'})

    # 5. Cruce de datos (Merge)
    ambas = pd.merge(
        df_ini_ready, 
        df_fin_ready, 
        left_on=id_ini_col, 
        right_on=id_fin_col, 
        suffixes=('_ini', '_fin')
    )

    # 6. Procesamiento si hay datos comunes
    if not ambas.empty:
        # Cálculo de Impacto
        ambas['Diferencia'] = ambas['PUNTO_FINAL'] - ambas['PUNTO_INICIAL']
        
        st.divider()
        
        # Métricas principales
        avg_diff = ambas['Diferencia'].mean()
        m1, m2, m3 = st.columns(3)
        m1.metric("Participantes Totales", len(ambas))
        m2.metric("Impacto Promedio", f"{avg_diff:.2f} pts")
        
        retencion = (len(ambas) / len(df_inicio)) * 100
        m3.metric("Tasa de Retención", f"{retencion:.1f}%")

        # Gráfico de evolución
        fig = px.bar(
            ambas, 
            x=id_ini_col, 
            y='Diferencia',
            title="Diferencia de Puntaje (Post - Pre)",
            color='Diferencia',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tabla de resultados
        st.subheader("✅ Listado de Cumplimiento")
        columnas_ver = [id_ini_col, 'PUNTO_INICIAL', 'PUNTO_FINAL', 'Diferencia']
        st.dataframe(ambas[columnas_ver])

        # Botón de descarga
        csv = ambas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte Final",
            data=csv,
            file_name="analisis_impacto.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ No se encontraron coincidencias. Asegúrate de que los IDs (correos o cédulas) sean los mismos en ambos archivos.")
else:
    st.info("Esperando archivos... Sube los documentos para generar el análisis.")
