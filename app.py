import streamlit as st
from supabase import create_client, Client
from datetime import date
import pandas as pd
import plotly.express as px
import time  # <-- Importado para permitir que los mensajes de éxito sean leíbles

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
respuesta_db = supabase.table("registro_actividades").select("*").order("id", desc=True).execute()
datos = respuesta_db.data

if not datos:
    st.info("📊 Registra tu primera actividad para generar el Dashboard.")
else:
    df_completo = pd.DataFrame(datos)
    
    if 'area' not in df_completo.columns:
        df_completo['area'] = 'Lexicodex'
    df_completo['area'] = df_completo['area'].fillna('Lexicodex')
    
    tab_dash, tab_gestion = st.tabs(["📊 Dashboard Visual", "🗄️ Gestión de Registros"])

    # ---------------------------------------------------------
    # PESTAÑA 1: DASHBOARD
    # ---------------------------------------------------------
    with tab_dash:
        area_filtro = st.radio("Mostrar resultados para:", ["Todas las Áreas", "Lexicodex", "NewsLetter", "TikTok"], horizontal=True)
        
        df_dash = df_completo.copy()
        if area_filtro != "Todas las Áreas":
            df_dash = df_dash[df_dash['area'] == area_filtro]

        if df_dash.empty:
            st.warning(f"No hay datos registrados aún para el área: {area_filtro}")
        else:
            df_dash['horas_reales'] = df_dash['minutos_reales'] / 60
            df_dash['costo_actividad'] = df_dash['horas_reales'] * df_dash['costo_hora']
            df_dash['margen'] = df_dash['ingreso'] - df_dash['costo_actividad']
            
            horas_totales = df_dash['horas_reales'].sum()
            ingresos_totales = df_dash['ingreso'].sum()
            margen_total = df_dash['margen'].sum()
            
            capacidad_mensual = 140
            P = min((horas_totales / capacidad_mensual) * 100, 100) 
            
            tareas_cumplidas = len(df_dash[df_dash['estado'] == 'Cumplido'])
            C = (tareas_cumplidas / len(df_dash)) * 100 if len(df_dash) > 0 else 0
            
            E = min((df_dash['minutos_objetivo'].sum() / df_dash['minutos_reales'].sum()) * 100, 100) if df_dash['minutos_reales'].sum() > 0 else 0
            Q = (df_dash['calidad'].mean() / 5) * 100
            R = (margen_total / ingresos_totales * 100) if ingresos_totales > 0 else 0
            
            horas_prioridad_alta = df_dash[df_dash['prioridad'] == 3]['horas_reales'].sum()
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
                if area_filtro in ["NewsLetter", "TikTok"]:
                    df_pie = df_dash.groupby("estado")["horas_reales"].sum().reset_index()
                    titulo_pie = "Distribución por Estado"
                    nombres = "estado"
                else:
                    df_pie = df_dash.groupby("categoria")["horas_reales"].sum().reset_index()
                    titulo_pie = "Distribución del Tiempo"
                    nombres = "categoria"
                    
                fig1 = px.pie(df_pie, values='horas_reales', names=nombres, 
                              title=titulo_pie, hole=0.4,
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig1, use_container_width=True)

            with col_graf2:
                if area_filtro == "Lexicodex":
                    df_graf2 = df_dash.groupby("sub_categoria")[["costo_actividad"]].sum().reset_index()
                    fig2 = px.bar(df_graf2, x="sub_categoria", y="costo_actividad", 
                                  title="Costo Operativo por Sub Categoría",
                                  labels={"costo_actividad": "Costo ($)", "sub_categoria": "Sub Categoría"})
                elif area_filtro in ["NewsLetter", "TikTok"]:
                    df_graf2 = df_dash.groupby("tema")[["costo_actividad"]].sum().reset_index()
                    fig2 = px.bar(df_graf2, x="tema", y="costo_actividad", 
                                  title=f"Costo Operativo por Tema de {area_filtro}",
                                  labels={"costo_actividad": "Costo Operativo ($)", "tema": "Tema"})
                else:
                    df_graf2 = df_dash.groupby("proyecto")[["ingreso", "costo_actividad"]].sum().reset_index()
                    df_graf2 = df_graf2[df_graf2['proyecto'].astype(bool)]
                    fig2 = px.bar(df_graf2, x="proyecto", y=["ingreso", "costo_actividad"], 
                                  title="Ingresos vs Costo por Proyecto", barmode="group",
                                  labels={"value": "Monto ($)", "variable": "Tipo", "proyecto": "Proyecto"})
                st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------------------
    # PESTAÑA 2: GESTIÓN DE DATOS (BUSCADOR Y EDICIÓN)
    # ---------------------------------------------------------
    with tab_gestion:
        st.markdown("### 🔍 Buscador Inteligente y Filtros")
        
        col_b1, col_b2 = st.columns([1, 2])
        with col_b1:
            filtro_tabla_area = st.selectbox("Filtrar Tabla por Área:", ["Todas", "Lexicodex", "NewsLetter", "TikTok"])
        with col_b2:
            texto_busqueda = st.text_input("Buscar por palabra (Actividad, Tema, Categoría...)", placeholder="Ej. Finanzas, Video, Amparo...")

        df_tabla = df_completo.copy()
        
        if filtro_tabla_area != "Todas":
            df_tabla = df_tabla[df_tabla['area'] == filtro_tabla_area]
            
        if texto_busqueda:
            columnas_texto = ['actividad', 'tema', 'categoria', 'sub_categoria', 'sub_sub_categoria', 'proyecto']
            columnas_existentes = [col for col in columnas_texto if col in df_tabla.columns]
            filtro_texto = df_tabla[columnas_existentes].fillna('').astype(str).apply(lambda x: x.str.contains(texto_busqueda, case=False)).any(axis=1)
            df_tabla = df_tabla[filtro_texto]
        
        st.markdown(f"**Resultados encontrados:** {len(df_tabla)}")

        df_vista = df_tabla.copy()
        df_vista['horas_reales'] = (df_vista['minutos_reales'] / 60).apply(lambda x: f"{x:.2f} h")
        
        cols_posibles = ['area', 'fecha_inicio', 'fecha_termino', 'actividad', 'tema', 'categoria', 'sub_categoria', 'sub_sub_categoria', 'horas_reales', 'estado']
        cols_mostrar = [col for col in cols_posibles if col in df_vista.columns]
        
        st.dataframe(df_vista[cols_mostrar], use_container_width=True)
        
        st.markdown("---")
        st.markdown("### ⚙️ Modificar o Eliminar Registro")
        
        if df_tabla.empty:
            st.info("No hay registros que coincidan con tu búsqueda.")
        else:
            opciones_editar = dict(zip(df_tabla['id'], df_tabla['area'] + " | " + df_tabla['fecha'].astype(str) + " | " + df_tabla['actividad']))
            
            registro_seleccionado = st.selectbox(
                "Selecciona el registro que deseas gestionar:",
                options=list(opciones_editar.keys()),
                format_func=lambda x: opciones_editar[x]
            )
            
            if registro_seleccionado:
                accion = st.radio("¿Qué acción deseas realizar?", ["✏️ Editar Registro", "🗑️ Eliminar Registro"], horizontal=True)
                
                if accion == "🗑️ Eliminar Registro":
                    st.warning("⚠️ Esta acción no se puede deshacer.")
                    if st.button("🚨 Eliminar Definitivamente", type="primary"):
                        try:
                            supabase.table("registro_actividades").delete().eq("id", registro_seleccionado).execute()
                            st.success("✅ Registro eliminado correctamente. Actualizando...")
                            time.sleep(1.5) # Pausa para que el usuario pueda leer el mensaje
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al eliminar el registro: {e}")
                            
                elif accion == "✏️ Editar Registro":
                    st.info("Modifica los datos que necesites y presiona Guardar Cambios.")
                    
                    fila = df_tabla[df_tabla['id'] == registro_seleccionado].iloc[0]
                    area_edit = fila['area']
                    
                    with st.expander("Abir Formulario de Edición", expanded=True):
                        col_e1, col_e2 = st.columns(2)
                        with col_e1: 
                            f_inicio_e = st.date_input("Fecha Inicio", pd.to_datetime(fila.get('fecha_inicio', fila['fecha'])), key="ei")
                        with col_e2: 
                            f_termino_e = st.date_input("Fecha Término", pd.to_datetime(fila.get('fecha_termino', fila['fecha'])), key="et")
                        
                        datos_actualizados = {
                            "fecha_inicio": str(f_inicio_e),
                            "fecha_termino": str(f_termino_e),
                            "fecha": str(f_termino_e)
                        }

                        if area_edit == "Lexicodex":
                            cat_val = fila.get('categoria', 'Contaduría')
                            idx_cat = list(diccionario_lexicodex.keys()).index(cat_val) if cat_val in diccionario_lexicodex else 0
                            cat_e = st.selectbox("Categoría", list(diccionario_lexicodex.keys()), index=idx_cat, key="ecat")
                            
                            sub_cats = diccionario_lexicodex[cat_e]
                            sub_cat_val = fila.get('sub_categoria', '')
                            idx_sub = sub_cats.index(sub_cat_val) if sub_cat_val in sub_cats else 0
                            sub_cat_e = st.selectbox("Sub Categoría", sub_cats, index=idx_sub, key="esub")
                            
                            sub_sub_val = fila.get('sub_sub_categoria', '')
                            sub_sub_e = st.text_input("Sub sub categoría", str(sub_sub_val) if pd.notna(sub_sub_val) else "", key="esubsub")
                            
                            act_val = fila.get('actividad', 'Crucigrama')
                            idx_act = ["Crucigrama", "Autodefinido", "Busca Palabra"].index(act_val) if act_val in ["Crucigrama", "Autodefinido", "Busca Palabra"] else 0
                            act_e = st.selectbox("Actividad", ["Crucigrama", "Autodefinido", "Busca Palabra"], index=idx_act, key="eact")
                            
                            datos_actualizados.update({"categoria": cat_e, "sub_categoria": sub_cat_e, "sub_sub_categoria": sub_sub_e, "actividad": act_e})
                        
                        elif area_edit in ["NewsLetter", "TikTok"]:
                            tema_val = fila.get('tema', '')
                            tema_e = st.text_input("Tema", str(tema_val) if pd.notna(tema_val) else "", key="etema")
                            prefijo = "Redacción: " if area_edit == "NewsLetter" else "Video: "
                            datos_actualizados.update({"tema": tema_e, "actividad": f"{prefijo}{tema_e}"})

                        col_t1, col_t2 = st.columns(2)
                        with col_t1: 
                            min_r_val = int(fila['minutos_reales']) if pd.notna(fila.get('minutos_reales')) else 60
                            min_r_e = st.number_input("Min. Reales", min_value=1, value=min_r_val, key="emr")
                        with col_t2: 
                            min_o_val = int(fila['minutos_objetivo']) if pd.notna(fila.get('minutos_objetivo')) else 60
                            min_o_e = st.number_input("Min. Objetivo", min_value=1, value=min_o_val, key="emo")
                        
                        pri_val = int(fila['prioridad']) if pd.notna(fila.get('prioridad')) else 3
                        idx_pri = [3, 2, 1].index(pri_val) if pri_val in [3, 2, 1] else 0
                        pri_e = st.selectbox("Prioridad", [3, 2, 1], index=idx_pri, format_func=lambda x: f"{x} - {'Alta' if x==3 else 'Media' if x==2 else 'Baja'}", key="epri")
                        
                        est_val = fila.get('estado', 'Cumplido')
                        if pd.isna(est_val): est_val = 'Cumplido'
                        idx_est = ["Cumplido", "Parcial", "Pendiente"].index(est_val) if est_val in ["Cumplido", "Parcial", "Pendiente"] else 0
                        est_e = st.selectbox("Estado", ["Cumplido", "Parcial", "Pendiente"], index=idx_est, key="eest")
                        
                        cal_val = int(fila['calidad']) if pd.notna(fila.get('calidad')) else 5
                        cal_e = st.slider("Calidad del Entregable", 1, 5, cal_val, key="ecal")
                        
                        cost_val = float(fila['costo_hora']) if pd.notna(fila.get('costo_hora')) else 850.0
                        cost_e = st.number_input("Costo por Hora ($)", min_value=0.0, value=cost_val, step=50.0, key="ecost")
                        
                        datos_actualizados.update({"minutos_reales": min_r_e, "minutos_objetivo": min_o_e, "prioridad": pri_e, "estado": est_e, "calidad": cal_e, "costo_hora": cost_e})

                        if st.button("💾 Guardar Cambios", type="primary"):
                            try:
                                supabase.table("registro_actividades").update(datos_actualizados).eq("id", registro_seleccionado).execute()
                                st.success("✅ ¡Registro modificado con éxito! Actualizando tablero...")
                                time.sleep(1.5) # Pausa para que el usuario pueda leer el mensaje
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error al guardar los cambios: {e}")
