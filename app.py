{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import plotly.express as px\
\
st.set_page_config(page_title="Validador & Analista de Impacto", layout="wide")\
\
st.title("\uc0\u55357 \u56960  Analista de Impacto: Inicio vs. Final")\
\
col1, col2 = st.columns(2)\
with col1:\
    file_inicio = st.file_uploader("Encuesta INICIAL", type=['xlsx', 'csv'])\
with col2:\
    file_final = st.file_uploader("Encuesta FINAL", type=['xlsx', 'csv'])\
\
if file_inicio and file_final:\
    df_inicio = pd.read_excel(file_inicio) if file_inicio.name.endswith('xlsx') else pd.read_csv(file_inicio)\
    df_final = pd.read_excel(file_final) if file_final.name.endswith('xlsx') else pd.read_csv(file_final)\
\
    # --- CONFIGURACI\'d3N ---\
    st.sidebar.header("Configuraci\'f3n de Columnas")\
    id_inicio = st.sidebar.selectbox("ID (Email/C\'e9dula) - Inicio", df_inicio.columns)\
    id_final = st.sidebar.selectbox("ID (Email/C\'e9dula) - Final", df_final.columns)\
    \
    # Columnas de Puntaje para el c\'e1lculo de impacto\
    score_inicio = st.sidebar.selectbox("Columna de Puntaje - Inicio", df_inicio.columns)\
    score_final = st.sidebar.selectbox("Columna de Puntaje - Final", df_final.columns)\
\
    # Limpieza\
    df_inicio[id_inicio] = df_inicio[id_inicio].astype(str).str.strip().lower()\
    df_final[id_final] = df_final[id_final].astype(str).str.strip().lower()\
\
    # --- CRUCE DE DATOS ---\
    ambas = pd.merge(df_inicio, df_final, left_on=id_inicio, right_on=id_final, suffixes=('_ini', '_fin'))\
    \
    # C\'e1lculo de impacto\
    ambas['Diferencia'] = ambas[score_final] - ambas[score_inicio]\
\
    # --- VISUALIZACI\'d3N ---\
    st.subheader("\uc0\u55357 \u56522  Resumen de Impacto")\
    avg_diff = ambas['Diferencia'].mean()\
    st.metric("Mejora Promedio", f"\{avg_diff:.2f\} pts", delta=f"\{avg_diff:.2f\}")\
\
    fig = px.bar(ambas, x=id_inicio, y='Diferencia', \
                 title="Diferencia de Puntaje por Participante",\
                 color='Diferencia', color_continuous_scale='RdYlGn')\
    st.plotly_chart(fig, use_container_width=True)\
\
    st.subheader("\uc0\u9989  Listado de Cumplimiento")\
    st.dataframe(ambas[[id_inicio, score_inicio, score_final, 'Diferencia']])\
\
    # Bot\'f3n de descarga\
    st.download_button("Descargar Reporte Completo", ambas.to_csv(index=False), "reporte_impacto.csv")}