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

@st.cache_resource
def init_connection():
    raw_url = st.secrets["SUPABASE_URL"]
    clean_url = raw_url.strip().rstrip('/').replace('/rest/v1', '')
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(clean_url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"❌ Error crítico de conexión. Detalle: {e}")
    st.stop()

# ==========================================
# 2. DICCIONARIOS DE DATOS
# ==========================================
diccionario_lexicodex = {
    "Contaduría": ["Contabilidad", "Fiscal", "Normas de Información", "Instituciones", "Finanzas"],
    "Administración": ["Gestión", "Economía", "Capital Humano", "Mercadotecnia", "Tecnologías de la Información"],
    "Derecho": ["Derechos humanos", "Ordenamiento Jurídico", "Amparo", "Jurisprudencia", "Doctrina"],
    "Ludo": ["Aprendizaje", "Artes", "Ciencias", "Cognición", "Democracia", "Deportes", "Ejercicio Físico", "Ejercicio Mental", "Eminentes", "Expresiones", "Filosofía", "Geopolítica", "Gobierno", "Historia", "Humanidades", "Instituciones", "Léxico", "Lógica", "Matemáticas", "Mindfulness", "Motivación", "Neurociencia", "Países", "Pensamiento", "Política", "Procrastinación", "Profesiones", "Psicología", "Salud", "Santiago Ixcuintla", "Sociedad", "Varios Temas"],
    "Sudokus": ["Por Actualizar"]
}

# ==========================================
# 3. FORMULARIO DINÁMICO DE CAPTURA
# ==========================================
with st.sidebar:
    st.header("📝 Nueva Actividad")
    
    area_seleccionada = st.selectbox(
        "Selecciona el Área de Trabajo:", 
        ["Lexicodex", "NewsLetter", "TikTok"]
    )
    
    st.markdown("---")
    
    # 🟢 FORMULARIO: LEXICODEX
    if area_seleccionada == "Lexicodex":
        st.subheader("Datos Lexicodex")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_inicio = st.date_input("Fecha Inicio", date.today())
        with col_f2:
            f_termino = st.date_input("Fecha Término", date.today())
        
        cat_lex = st.selectbox("Categoría", list(diccionario_lexicodex.keys()))
        sub_cat_lex = st.selectbox("Sub Categoría", diccionario_lexicodex[cat_lex])
        sub_sub_cat = st.text_input("Sub sub categoría (Especificar)")
        
        actividad_lex = st.selectbox("Actividad", ["Crucigrama", "Autodefinido", "Busca Palabra"])
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col_t2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", 1, 5, 5)
        costo_hora = st.number_input("Costo por Hora ($)", min_value=0.0, value=850.0, step=50.0)
        
        if st.button("💾 Registrar en Lexicodex", type="primary"):
            if sub_sub_cat == "":
                st.warning("⚠️ El campo de Sub sub categoría no puede estar vacío.")
            else:
                nuevo_registro = {
                    "area": "Lexicodex",
                    "fecha_inicio": str(f_inicio),
                    "fecha_termino": str(f_termino),
                    "fecha": str(f_termino),
                    "categoria": cat_lex,
                    "sub_categoria": sub_cat_lex,
                    "sub_sub_categoria": sub_sub_cat,
                    "actividad": actividad_lex,
                    "minutos_reales": min_reales,
                    "minutos_objetivo": min_objetivo,
                    "prioridad": prioridad,
                    "estado": estado,
                    "calidad": calidad,
                    "costo_hora": costo_hora,
                    "proyecto": "Lexicodex",
                    "ingreso": 0.0 
                }
                
                try:
                    supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success("✅ ¡Actividad de Lexicodex registrada!")
                except Exception as e:
                    st.error(f"❌ Error en BD: {e}")

    # 🟡 FORMULARIO: NEWSLETTER
    elif area_seleccionada == "NewsLetter":
        st.subheader("Datos NewsLetter")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_inicio = st.date_input("Fecha Inicio", date.today())
        with col_f2:
            f_termino = st.date_input("Fecha Término", date.today())
            
        tema_nl = st.text_input("Tema NewsLetter")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col_t2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", 1, 5, 5)
        costo_hora = st.number_input("Costo por Hora ($)", min_value=0.0, value=850.0, step=50.0)
        
        if st.button("💾 Registrar en NewsLetter", type="primary"):
            if tema_nl == "":
                st.warning("⚠️ El campo 'Tema' no puede estar vacío.")
            else:
                nuevo_registro = {
                    "area": "NewsLetter",
                    "fecha_inicio": str(f_inicio),
                    "fecha_termino": str(f_termino),
                    "fecha": str(f_termino), 
                    "tema": tema_nl,
                    "actividad": f"Redacción: {tema_nl}", 
                    "categoria": "NewsLetter", 
                    "proyecto": "NewsLetter", 
                    "minutos_reales": min_reales,
                    "minutos_objetivo": min_objetivo,
                    "prioridad": prioridad,
                    "estado": estado,
                    "calidad": calidad,
                    "costo_hora": costo_hora,
                    "ingreso": 0.0 
                }
                
                try:
                    supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success("✅ ¡NewsLetter registrada exitosamente!")
                except Exception as e:
                    st.error(f"❌ Error en BD: {e}")

    # 🟣 FORMULARIO: TIKTOK
    elif area_seleccionada == "TikTok":
        st.subheader("Datos TikTok")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_inicio = st.date_input("Fecha Inicio", date.today())
        with col_f2:
            f_termino = st.date_input("Fecha Término", date.today())
            
        tema_tk = st.text_input("Tema TikTok")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            min_reales = st.number_input("Min. Reales", min_value=1, value=60)
        with col_t2:
            min_objetivo = st.number_input("Min. Objetivo", min_value=1, value=60)
            
        prioridad = st.selectbox("Prioridad", [3, 2, 1], format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}")
        estado = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"])
        calidad = st.slider("Calidad del Entregable", 1, 5, 5)
        costo_hora = st.number_input("Costo por Hora ($)", min_value=0.0, value=850.0, step=50.0)
        
        if st.button("💾 Registrar en TikTok", type="primary"):
            if tema_tk == "":
                st.warning("⚠️ El campo 'Tema' no puede estar vacío.")
            else:
                nuevo_registro = {
                    "area": "TikTok",
                    "fecha_inicio": str(f_inicio),
                    "fecha_termino": str(f_termino),
                    "fecha": str(f_termino), 
                    "tema": tema_tk,
                    "actividad": f"Video: {tema_tk}", 
                    "categoria": "TikTok", 
                    "proyecto": "TikTok", 
                    "minutos_reales": min_reales,
                    "minutos_objetivo": min_objetivo,
                    "prioridad": prioridad,
                    "estado": estado,
                    "calidad": calidad,
                    "costo_hora": costo_hora,
                    "ingreso": 0.0 
                }
                
                try:
                    supabase.table("registro_actividades").insert(nuevo_registro).execute()
                    st.success("✅ ¡TikTok registrado exitosamente!")
                except Exception as e:
                    st.error(f"❌ Error en BD: {e}")

# ==========================================
# 4. EXTRACCIÓN Y MOTOR KPI
# ==========================================
respuesta_db = supabase.table("registro_actividades").select("*").execute()
datos = respuesta_db.data

if not datos:
    st.info("📊 Registra tu primera actividad para generar el Dashboard.")
else:
    df = pd.DataFrame(datos)
    
    if 'area' not in df.columns:
        df['area'] = 'Lexicodex'
    df['area'] = df['area'].fillna('Lexicodex')
    
    area_filtro = st.radio("Mostrar resultados para:", ["Todas las Áreas", "Lexicodex", "NewsLetter", "TikTok"], horizontal=True)
    
    if area_filtro != "Todas las Áreas":
        df = df[df['area'] == area_filtro]

    if df.empty:
        st.warning(f"No hay datos registrados aún para el área: {area_filtro}")
    else:
        df['horas_reales'] = df['minutos_reales'] / 60
        df['costo_actividad'] = df['horas_reales'] * df['costo_hora']
        df['margen'] = df['ingreso'] - df['costo_actividad']
        
        tab_dash, tab_gestion = st.tabs(["📊 Dashboard Visual", "🗄️ Gestión de Registros"])

        with tab_dash:
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
            
            IIDP = (0.25 * P) + (0.20 * C) + (0.15 * E) + (0.15 * Q) + (0.15 * R) + (0.10 * EP)

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

            st.markdown("### Análisis Gráfico")
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                # La dona agrupa TikTok y NewsLetter por Estado (al no tener categorías como Lexicodex)
                if area_filtro in ["NewsLetter", "TikTok"]:
                    df_pie = df.groupby("estado")["horas_reales"].sum().reset_index()
                    titulo_pie = "Distribución por Estado"
                    nombres = "estado"
                else:
                    df_pie = df.groupby("categoria")["horas_reales"].sum().reset_index()
                    titulo_pie = "Distribución del Tiempo"
                    nombres = "categoria"
                    
                fig1 = px.pie(df_pie, values='horas_reales', names=nombres, 
                              title=titulo_pie, hole=0.4,
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig1, use_container_width=True)

            with col_graf2:
                # El gráfico de barras se adapta según el área seleccionada
                if area_filtro == "Lexicodex":
                    df_graf2 = df.groupby("sub_categoria")[["costo_actividad"]].sum().reset_index()
                    fig2 = px.bar(df_graf2, x="sub_categoria", y="costo_actividad", 
                                  title="Costo Operativo por Sub Categoría",
                                  labels={"costo_actividad": "Costo ($)", "sub_categoria": "Sub Categoría"})
                elif area_filtro in ["NewsLetter", "TikTok"]:
                    df_graf2 = df.groupby("tema")[["costo_actividad"]].sum().reset_index()
                    fig2 = px.bar(df_graf2, x="tema", y="costo_actividad", 
                                  title=f"Costo Operativo por Tema de {area_filtro}",
                                  labels={"costo_actividad": "Costo Operativo ($)", "tema": "Tema"})
                else:
                    df_graf2 = df.groupby("proyecto")[["ingreso", "costo_actividad"]].sum().reset_index()
                    df_graf2 = df_graf2[df_graf2['proyecto'].astype(bool)]
                    fig2 = px.bar(df_graf2, x="proyecto", y=["ingreso", "costo_actividad"], 
                                  title="Ingresos vs Costo por Proyecto", barmode="group",
                                  labels={"value": "Monto ($)", "variable": "Tipo", "proyecto": "Proyecto"})
                st.plotly_chart(fig2, use_container_width=True)

        # PESTAÑA 2: GESTIÓN DE DATOS
        with tab_gestion:
            st.markdown("### Base de Datos Activa")
            df_vista = df.copy()
            df_vista['ingreso'] = df_vista['ingreso'].apply(lambda x: f"${x:,.2f}")
            df_vista['margen'] = df_vista['margen'].apply(lambda x: f"${x:,.2f}")
            df_vista['horas_reales'] = df_vista['horas_reales'].apply(lambda x: f"{x:.2f} h")
            
            cols_posibles = ['area', 'fecha_inicio', 'fecha_termino', 'actividad', 'tema', 'categoria', 'sub_categoria', 'sub_sub_categoria', 'horas_reales', 'margen', 'estado']
            cols_mostrar = [col for col in cols_posibles if col in df_vista.columns]
            
            st.dataframe(df_vista[cols_mostrar], use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🗑️ Eliminar Registro")
            
            opciones_eliminar = dict(zip(df['id'], df['area'] + " | " + df['fecha'].astype(str) + " | " + df['actividad']))
            
            registro_a_eliminar = st.selectbox(
                "Selecciona la actividad que deseas eliminar:",
                options=list(opciones_eliminar.keys()),
                format_func=lambda x: opciones_eliminar[x]
            )
            
            if st.button("🚨 Eliminar Definitivamente", type="primary"):
                try:
                    supabase.table("registro_actividades").delete().eq("id", registro_a_eliminar).execute()
                    st.success("✅ Registro eliminado correctamente. Actualizando...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al eliminar el registro: {e}")
