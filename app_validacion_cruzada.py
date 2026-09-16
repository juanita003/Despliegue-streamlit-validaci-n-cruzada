import pickle
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Configuración general
# ---------------------------------------------------------
st.set_page_config(
    page_title="Predicción cardiovascular",
    page_icon="🫀",
    layout="wide"
)

# Estilo diferente al ejemplo de videojuegos
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    .main-title {
        font-size: 2.35rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #667085;
        margin-bottom: 1.6rem;
    }
    .result-card {
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-top: .8rem;
    }
    .small-note {
        font-size: .88rem;
        color: #667085;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Carga del modelo guardado en el notebook de validación
# ---------------------------------------------------------
@st.cache_resource
def cargar_modelo():
    with open("modelo-cla.pkl", "rb") as archivo:
        modelo, labelencoder, variables, min_max_scaler = pickle.load(archivo)
    return modelo, labelencoder, list(variables), min_max_scaler

try:
    modelo, labelencoder, variables, min_max_scaler = cargar_modelo()
except FileNotFoundError:
    st.error(
        "No se encontró 'modelo-cla.pkl'. Ejecuta primero el notebook de "
        "validación cruzada hasta la celda que guarda el modelo y coloca el "
        "archivo en la misma carpeta de esta aplicación."
    )
    st.stop()

# ---------------------------------------------------------
# Encabezado
# ---------------------------------------------------------
st.markdown('<div class="main-title">Predicción académica de evento cardiovascular</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Modelo KNN seleccionado mediante validación cruzada estratificada de 10 particiones.</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Sobre el modelo")
    st.write("**Modelo final:** K-Nearest Neighbors (KNN)")
    st.write("**Vecinos:** 7")
    st.write("**Métrica:** distancia euclidiana")
    st.write("**Validación:** Stratified K-Fold, 10 folds")
    st.divider()
    st.metric("Accuracy promedio", "87.34 %")
    st.metric("F1 macro promedio", "80.91 %")
    st.metric("Recall macro promedio", "82.02 %")
    st.caption("Métricas obtenidas en el notebook de validación cruzada.")
    st.warning("Uso exclusivamente académico. La salida del modelo no constituye un diagnóstico médico.")

tab_pred, tab_modelo = st.tabs(["Predicción", "Rendimiento del modelo"])

# ---------------------------------------------------------
# TAB 1: captura y predicción
# ---------------------------------------------------------
with tab_pred:
    st.subheader("Datos de entrada")
    st.write("Completa los datos y presiona **Realizar predicción**.")

    with st.form("formulario_prediccion"):
        col1, col2 = st.columns(2)

        with col1:
            edad = st.slider("Edad", min_value=1, max_value=82, value=45, step=1)
            glucosa = st.number_input(
                "Nivel promedio de glucosa",
                min_value=55.12,
                max_value=271.74,
                value=91.89,
                step=0.10,
                format="%.2f"
            )
            hipertension_ui = st.selectbox("¿Tiene hipertensión?", ["No", "Sí"])

        with col2:
            cardiopatia_ui = st.selectbox("¿Tiene enfermedad cardíaca?", ["No", "Sí"])
            casado_ui = st.selectbox("¿Alguna vez se ha casado?", ["No", "Sí"])
            fumador_ui = st.selectbox(
                "Estado de tabaquismo",
                ["Nunca ha fumado", "Fumó anteriormente", "Fuma actualmente", "Desconocido"]
            )

        enviar = st.form_submit_button("Realizar predicción", use_container_width=True)

    if enviar:
        # Traducción de etiquetas de la interfaz a los valores usados en entrenamiento
        mapa_si_no = {"No": "No", "Sí": "Yes"}
        mapa_fumador = {
            "Nunca ha fumado": "'never smoked'",
            "Fumó anteriormente": "'formerly smoked'",
            "Fuma actualmente": "smokes",
            "Desconocido": "Unknown"
        }

        datos = pd.DataFrame([{
            "age": edad,
            "hypertension": mapa_si_no[hipertension_ui],
            "heart_disease": mapa_si_no[cardiopatia_ui],
            "ever_married": mapa_si_no[casado_ui],
            "avg_glucose_level": glucosa,
            "smoking_status": mapa_fumador[fumador_ui]
        }])

        # Mismo preprocesamiento del notebook de entrenamiento
        data_preparada = datos.copy()

        data_preparada = pd.get_dummies(
            data_preparada,
            columns=["smoking_status"],
            drop_first=False,
            dtype=int
        )

        # En despliegue usamos drop_first=False porque normalmente se predice
        # un solo registro; luego reindex conserva únicamente las columnas
        # que existían durante el entrenamiento (por ejemplo, hypertension_Yes).
        data_preparada = pd.get_dummies(
            data_preparada,
            columns=["hypertension", "heart_disease", "ever_married"],
            drop_first=False,
            dtype=int
        )

        # Se crean las columnas faltantes y se respeta el mismo orden del entrenamiento
        data_preparada = data_preparada.reindex(columns=variables, fill_value=0)

        # El modelo KNN se entrenó con estas dos variables normalizadas
        data_preparada[["age", "avg_glucose_level"]] = min_max_scaler.transform(
            data_preparada[["age", "avg_glucose_level"]]
        )

        # Predicción
        prediccion_cod = int(modelo.predict(data_preparada)[0])
        prediccion = str(labelencoder.inverse_transform([prediccion_cod])[0])

        # Probabilidad estimada por el modelo para cada clase
        probabilidades = modelo.predict_proba(data_preparada)[0]
        etiquetas = labelencoder.inverse_transform(modelo.classes_.astype(int))
        tabla_prob = pd.DataFrame({
            "Clase": etiquetas,
            "Probabilidad": probabilidades
        })
        tabla_prob["Probabilidad (%)"] = (tabla_prob["Probabilidad"] * 100).round(2)

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("Resultado")

        if prediccion.strip().lower() in ["yes", "si", "sí", "1"]:
            st.error("El modelo clasificó el registro en la clase: **Sí**.")
        else:
            st.success("El modelo clasificó el registro en la clase: **No**.")

        c1, c2 = st.columns(2)
        with c1:
            st.write("**Probabilidad estimada por clase**")
            grafica = tabla_prob.set_index("Clase")[["Probabilidad (%)"]]
            st.bar_chart(grafica)

        with c2:
            st.write("**Resumen del caso ingresado**")
            resumen = pd.DataFrame({
                "Variable": [
                    "Edad", "Glucosa promedio", "Hipertensión",
                    "Enfermedad cardíaca", "Alguna vez casado", "Tabaquismo"
                ],
                "Valor": [
                    edad, f"{glucosa:.2f}", hipertension_ui,
                    cardiopatia_ui, casado_ui, fumador_ui
                ]
            })
            st.dataframe(resumen, hide_index=True, use_container_width=True)

        # Funcionalidad adicional: descargar el resultado
        resultado_descarga = datos.copy()
        resultado_descarga["prediccion_modelo"] = prediccion
        for _, fila in tabla_prob.iterrows():
            resultado_descarga[f"probabilidad_{fila['Clase']}"] = fila["Probabilidad"]

        st.download_button(
            "Descargar resultado en CSV",
            data=resultado_descarga.to_csv(index=False).encode("utf-8"),
            file_name="resultado_prediccion.csv",
            mime="text/csv",
            use_container_width=True
        )

        with st.expander("Ver datos preparados para el modelo"):
            st.dataframe(data_preparada, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(
            "La probabilidad mostrada corresponde al clasificador entrenado y no debe interpretarse "
            "como una probabilidad clínica individual."
        )

# ---------------------------------------------------------
# TAB 2: información adicional de la validación cruzada
# ---------------------------------------------------------
with tab_modelo:
    st.subheader("Resultados promedio de validación cruzada")
    metricas = pd.DataFrame({
        "Métrica": ["Accuracy", "F1 macro", "Precisión macro", "Recall macro"],
        "Valor": [0.873430, 0.809117, 0.800478, 0.820244]
    })
    metricas["Porcentaje"] = (metricas["Valor"] * 100).round(2)

    col_a, col_b = st.columns([1, 1.3])
    with col_a:
        st.dataframe(
            metricas[["Métrica", "Porcentaje"]].rename(columns={"Porcentaje": "Resultado (%)"}),
            hide_index=True,
            use_container_width=True
        )

    with col_b:
        st.bar_chart(metricas.set_index("Métrica")[["Porcentaje"]])

    st.info(
        "El KNN fue el modelo seleccionado en el notebook final. "
        "Las métricas aquí mostradas corresponden al promedio de las 10 particiones."
    )
