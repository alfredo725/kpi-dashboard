import streamlit as st
from supabase import create_client, Client
from datetime import date
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CONFIGURACIÓN DEL ENTORNO
# ==========================================
st.set_page_config(page_title="Dashboard KPI", page_icon="📊", layout="wide")
st.title("Índice Integral de Desempeño Profesional (IIDP)")

# Conexión a Supabase (Con limpiador automático de URL)
@st.cache_resource
def init_connection():
    raw_url = st.secrets["SUPABASE_URL"]
    # Limpieza de URL para evitar el error PGRST125
    clean_url = raw_url.strip().rstrip('/').replace('/rest/v1', '')
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(clean_url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"❌ Error crítico de conexión. Verifica los Secretos. Detalle: {e}")
    st.stop()

# ==========================================
# 2. FORMULARIO DE CAPTURA (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("📝 Nueva Actividad")
    
    with st.form("registro_form", clear_on_submit=True):
        fecha = st.date_input("Fecha", date.today())
        actividad = st.text_input("Actividad (Ej. Reunión cliente)")
        categoria = st.selectbox("Categoría", ["Producción", "Comercial", "Estrategia", "Administración"])
        proyecto = st.text_input("Proyecto / Cliente")
        
        col1, col2 = st.columns(2)
        with col1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", min_value=1, max_value=5, value=5)
        
        # Campo de Ingreso Inteligente (Permite comas)
        ingreso_str = st.text_input("Ingreso Generado ($)", value="0.00", help="Puedes usar comas, ej: 4,500.00")
        
        submit_button = st.form_submit_button("Registrar Actividad")
        
        if submit_button:
            if actividad == "":
                st.warning("⚠️ Debes escribir el nombre de la actividad.")
            else:
                # Limpieza de la coma para convertirlo a número matemático
                try:
                    ingreso_limpio = float(ingreso_str.replace(",", ""))
                except ValueError:
                    st.error("⚠️ Formato de ingreso no válido. Usa solo números y punto decimal.")
                    ingreso_limpio = 0.0
                
                # Preparamos el diccionario de datos
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
                    "ingreso": ingreso_limpio
                }
                
                # Enviamos a Supabase
                try:
                    supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success("✅ ¡Actividad registrada con éxito!")
                except Exception as e:
                    st.error(f"❌ Error al guardar en base de datos: {e}")

# ==========================================
# 3. EXTRACCIÓN Y MOTOR KPI
# ==========================================

# Extraer datos (Incluye el 'id' para poder gestionar eliminaciones)
respuesta_db = supabase.table("registro_actividades").select("*").execute()
datos = respuesta_db.data

if not datos:
    st.info("📊 Utiliza el menú lateral para registrar tu primera actividad y generar el Dashboard.")
else:
    df = pd.DataFrame(datos)
    
    # Cálculos derivados fundamentales
    df['horas_reales'] = df['minutos_reales'] / 60
    df['costo_actividad'] = df['horas_reales'] * df['costo_hora']
    df['margen'] = df['ingreso'] - df['costo_actividad']
    
    # CREACIÓN DE PESTAÑAS (TABS)
    tab_dash, tab_gestion = st.tabs(["📊 Dashboard Visual", "🗄️ Gestión de Registros"])

    # ---------------------------------------------------------
    # PESTAÑA 1: DASHBOARD VISUAL
    # ---------------------------------------------------------
    with tab_dash:
        # Ecuaciones del IIDP
        horas_totales = df['horas_reales'].sum()
        ingresos_totales = df['ingreso'].sum()
        margen_total = df['margen'].sum()
        
        capacidad_mensual = 140
        P = min((horas_totales / capacidad_mensual) * 100, 100) 
        
        tareas_cumplidas = len(df[df['estado'] == 'Cumplido'])
        C = (tareas_cumplidas / len(df)) * 100 if len(df) > 0 else 0
        
        E = min((df['minutos_objetivo'].sum() / df['minutos_reales'].sum()) * 100, 100) if df['minutos_reales'].sum() > 0 else 0
        Q = (df['calidad'].mean() / 5) * 100
        R = (margen_total / ingresos_totales * 100) if ingresos_totales > 0 else 0
        
        horas_prioridad_alta = df[df['prioridad'] == 3]['horas_reales'].sum()
        EP = (horas_prioridad_alta / horas_totales) * 100 if horas_totales > 0 else 0
        
        # Fórmula Maestra
        IIDP = (0.25 * P) + (0.20 * C) + (0.15 * E) + (0.15 * Q) + (0.15 * R) + (0.10 * EP)

        # Panel de Tarjetas Superiores
        st.markdown("### Resumen Global")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("🏆 IIDP Global", f"{IIDP:.1f} / 100")
        kpi2.metric("⏱️ Productividad", f"{P:.1f}%")
        kpi3.metric("🎯 Cumplimiento", f"{C:.1f}%")
        kpi4.metric("⚡ Eficiencia", f"{E:.1f}%")
        
        st.divider()
        
        kpi5, kpi6, kpi7, kpi8 = st.columns(4)
        kpi5.metric("🌟 Calidad Promedio", f"{Q:.1f}%")
        kpi6.metric("📈 Rentabilidad (Margen)", f"{R:.1f}%")
        kpi7.metric("🔥 Enfoque (Alta Prioridad)", f"{EP:.1f}%")
        
        valor_hora = ingresos_totales / horas_totales if horas_totales > 0 else 0
        kpi8.metric("💰 Valor x Hora Generado", f"${valor_hora:,.2f}")

        # Panel de Gráficos (Plotly)
        st.markdown("### Análisis Gráfico")
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            df_cat = df.groupby("categoria")["horas_reales"].sum().reset_index()
            fig1 = px.pie(df_cat, values='horas_reales', names='categoria', 
                          title="Distribución del Tiempo", hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig1, use_container_width=True)

        with col_graf2:
            df_proj = df.groupby("proyecto")[["ingreso", "costo_actividad"]].sum().reset_index()
            df_proj = df_proj[df_proj['proyecto'] != ""] # Filtra si el proyecto está vacío
            fig2 = px.bar(df_proj, x="proyecto", y=["ingreso", "costo_actividad"], 
                          title="Ingresos vs Costo por Proyecto", barmode="group",
                          labels={"value": "Monto ($)", "variable": "Tipo", "proyecto": "Proyecto"})
            st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------------------
    # PESTAÑA 2: GESTIÓN DE DATOS (ELIMINAR REGISTROS)
    # ---------------------------------------------------------
    with tab_gestion:
        st.markdown("### Base de Datos Activa")
        st.info("Aquí puedes revisar el historial completo y eliminar registros si cometiste algún error en la captura.")
        
        # Formateamos los datos financieros para que se vean bien en la tabla
        df_vista = df.copy()
        df_vista['ingreso'] = df_vista['ingreso'].apply(lambda x: f"${x:,.2f}")
        df_vista['margen'] = df_vista['margen'].apply(lambda x: f"${x:,.2f}")
        df_vista['horas_reales'] = df_vista['horas_reales'].apply(lambda x: f"{x:.2f} h")
        
        # Mostramos la tabla ocultando columnas muy técnicas
        st.dataframe(df_vista.drop(columns=['costo_hora', 'created_at', 'costo_actividad']), use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🗑️ Eliminar Registro")
        
        # Selector para elegir qué registro eliminar (Muestra Fecha + Actividad, pero usa el ID por detrás)
        opciones_eliminar = dict(zip(df['id'], df['fecha'].astype(str) + " | " + df['actividad'] + " (" + df['proyecto'] + ")"))
        
        registro_a_eliminar = st.selectbox(
            "Selecciona la actividad que deseas eliminar:",
            options=list(opciones_eliminar.keys()),
            format_func=lambda x: opciones_eliminar[x]
        )
        
        if st.button("🚨 Eliminar Definitivamente", type="primary"):
            try:
                # Ordenamos a Supabase borrar el registro exacto
                supabase.table("registro_actividades").delete().eq("id", registro_a_eliminar).execute()
                st.success("✅ Registro eliminado correctamente. Actualizando...")
                st.rerun() # Recarga la aplicación para reflejar los cambios en las gráficas
            except Exception as e:
                st.error(f"❌ Error al eliminar el registro: {e}")
