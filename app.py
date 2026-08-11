import streamlit as st
from supabase import create_client, Client
from datetime import date

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard KPI", layout="wide")
st.title("Índice Integral de Desempeño Profesional (IIDP)")

# 2. Conexión a Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"❌ Error al conectar con Supabase: {e}")
    st.stop() # Detiene la app si no hay conexión

# ==========================================
# FASE 3: FORMULARIO DE CAPTURA (SIDEBAR)
# ==========================================

with st.sidebar:
    st.header("📝 Nueva Actividad")
    
    # Usamos st.form para que la página no se recargue con cada tecla que presionas
    with st.form("registro_form", clear_on_submit=True):
        
        # Campos de entrada cualitativos
        fecha = st.date_input("Fecha", date.today())
        actividad = st.text_input("Actividad (Ej. Reunión cliente, Desarrollo...)")
        categoria = st.selectbox("Categoría", ["Producción", "Comercial", "Estrategia", "Administración"])
        proyecto = st.text_input("Proyecto / Cliente")
        
        # Campos de tiempo organizados en columnas
        col1, col2 = st.columns(2)
        with col1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        # Clasificaciones de valor
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", min_value=1, max_value=5, value=5)
        
        # Dato económico
        ingreso = st.number_input("Ingreso Generado ($)", min_value=0.0, value=0.0, step=100.0)
        
        # Botón de envío
        submit_button = st.form_submit_button("Registrar Actividad")
        
        if submit_button:
            # Validamos que no envíe actividades en blanco
            if actividad == "":
                st.warning("⚠️ Debes escribir el nombre de la actividad.")
            else:
                # Estructuramos los datos tal cual como los pide nuestra tabla SQL
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
                    # costo_hora tomará el valor por defecto (850) que definimos en la base de datos
                }
                
                # Insertamos a Supabase
                try:
                    supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success(f"✅ ¡'{actividad}' registrada con éxito!")
                except Exception as e:
                    st.error(f"❌ Error al guardar en base de datos: {e}")

# ==========================================
# ÁREA CENTRAL (Próximamente Dashboard)
# ==========================================
st.markdown("---")
st.info("👈 Utiliza la barra lateral para registrar tu primera actividad. El Dashboard se construirá aquí.")
