import streamlit as st
from supabase import create_client, Client
from datetime import date

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard KPI", layout="wide")
st.title("Índice Integral de Desempeño Profesional (IIDP)")

# 2. Conexión a Supabase (Con limpiador automático de URL)
@st.cache_resource
def init_connection():
    # Limpiamos espacios, diagonales finales y rutas extra que causan el error PGRST125
    raw_url = st.secrets["SUPABASE_URL"]
    clean_url = raw_url.strip().rstrip('/').replace('/rest/v1', '')
    key = st.secrets["SUPABASE_KEY"].strip()
    
    return create_client(clean_url, key), clean_url

try:
    supabase, url_limpia = init_connection()
    
    # --- MODO DIAGNÓSTICO ---
    st.info(f"🔍 URL procesada por el sistema: `{url_limpia}`")
    
    # Prueba de lectura para confirmar que encuentra la tabla
    test_lectura = supabase.table("registro_actividades").select("id").limit(1).execute()
    st.success("✅ Conexión establecida y tabla 'registro_actividades' encontrada perfectamente.")
    
except Exception as e:
    st.error(f"❌ Error crítico de conexión. Detalle: {e}")
    st.stop() # Detiene la ejecución si falla

# ==========================================
# FASE 3: FORMULARIO DE CAPTURA (SIDEBAR)
# ==========================================

with st.sidebar:
    st.header("📝 Nueva Actividad")
    
    with st.form("registro_form", clear_on_submit=True):
        
        # Campos cualitativos
        fecha = st.date_input("Fecha", date.today())
        actividad = st.text_input("Actividad (Ej. Reunión cliente)")
        categoria = st.selectbox("Categoría", ["Producción", "Comercial", "Estrategia", "Administración"])
        proyecto = st.text_input("Proyecto / Cliente")
        
        # Campos de tiempo
        col1, col2 = st.columns(2)
        with col1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        # Clasificaciones
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", min_value=1, max_value=5, value=5)
        
        # Dato económico
        ingreso = st.number_input("Ingreso Generado ($)", min_value=0.0, value=0.0, step=100.0)
        
        # Botón de envío
        submit_button = st.form_submit_button("Registrar Actividad")
        
        if submit_button:
            if actividad == "":
                st.warning("⚠️ Debes escribir el nombre de la actividad.")
            else:
                # Diccionario con los datos
                nuevo_registro = {
                    "fecha": str(fecha),
                    "actividad": actividad,
                    "categoria": categoria,
                    "proyecto": proyecto,
                    "minutos_reales": min_reales,
                    "minutos_objetivo": min_objetivo,
                    "prioridad": prioridad,
                    "estado": estado,
                    "calidad": calidad,
                    "ingreso": ingreso
                }
                
                # Inserción
                try:
                    respuesta = supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success(f"✅ ¡'{actividad}' registrada con éxito en Supabase!")
                except Exception as e:
                    st.error(f"❌ Error al guardar en base de datos: {e}")

# ==========================================
# ÁREA CENTRAL
# ==========================================
st.markdown("---")
st.info("👈 Intenta registrar el ejemplo comercial usando el formulario.")
