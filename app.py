import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validador de Participación", layout="wide")

st.title("✅ Validador de Encuestas: Inicio vs. Final")
st.markdown("Carga las listas para identificar quiénes completaron el ciclo completo.")

# 1. Carga de archivos
col1, col2 = st.columns(2)
with col1:
    file_inicio = st.file_uploader("Lista de Inicio (Excel/CSV)", type=['xlsx', 'csv'])
with col2:
    file_final = st.file_uploader("Lista Final (Excel/CSV)", type=['xlsx', 'csv'])

if file_inicio and file_final:
    # Leer datos
    df_inicio = pd.read_excel(file_inicio) if file_inicio.name.endswith('xlsx') else pd.read_csv(file_inicio)
    df_final = pd.read_excel(file_final) if file_final.name.endswith('xlsx') else pd.read_csv(file_final)

    # 2. Configuración de ID
    st.sidebar.header("⚙️ Configuración")
    id_ini = st.sidebar.selectbox("Columna Identificadora - Inicio", df_inicio.columns)
    id_fin = st.sidebar.selectbox("Columna Identificadora - Final", df_final.columns)

    # Limpieza básica de texto
    df_inicio[id_ini] = df_inicio[id_ini].astype(str).str.strip().str.lower()
    df_final[id_fin] = df_final[id_fin].astype(str).str.strip().str.lower()

    # 3. Lógica de Cruce
    # Participantes que hicieron AMBAS
    ambos = pd.merge(df_inicio, df_final, left_on=id_ini, right_on=id_fin, how='inner')
    
    # Participantes que solo hicieron la inicial (Pendientes)
    pendientes = df_inicio[~df_inicio[id_ini].isin(df_final[id_fin])]

    # 4. Visualización de Resultados
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Iniciaron", len(df_inicio))
    m2.metric("Total Finalizaron", len(df_final))
    m3.metric("Completaron Ciclo", len(ambos))

    tab1, tab2 = st.tabs(["🎯 Completaron Ambas", "⏳ Pendientes de Final"])

    with tab1:
        st.subheader(f"Se encontraron {len(ambos)} coincidencias")
        st.dataframe(ambos, use_container_width=True)
        # Botón para descargar solo los que cumplieron
        csv_ambos = ambos.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Lista de Cumplimiento", data=csv_ambos, file_name="completaron_proceso.csv")

    with tab2:
        st.subheader(f"Hay {len(pendientes)} personas que no terminaron")
        st.dataframe(pendientes, use_container_width=True)
        # Botón para descargar los que faltan (útil para enviar recordatorios)
        csv_pend = pendientes.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Lista de Pendientes", data=csv_pend, file_name="pendientes_por_finalizar.csv")

else:
    st.info("👋 Sube los dos archivos para validar quiénes completaron el proceso.")
