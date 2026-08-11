import streamlit as st
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(page_title="Dashboard KPI", layout="wide")
st.title("Índice Integral de Desempeño Profesional (IIDP)")

# Función para conectar a Supabase de forma segura
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Prueba de conexión
try:
    supabase = init_connection()
    st.success("✅ Conexión a Supabase establecida correctamente. ¡El entorno está listo!")
except Exception as e:
    st.error(f"❌ Error al conectar con Supabase. Verifica tus secretos. Detalles: {e}")
