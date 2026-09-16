
import pickle
import base64
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="CardioPredict",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# FONDO
# =========================================================
def cargar_imagen_base64(ruta):
    with open(ruta, "rb") as imagen:
        return base64.b64encode(imagen.read()).decode()


# La imagen debe estar en la misma carpeta que app_validacion_cruzada.py
RUTA_FONDO = "corazon1.jpg"

try:
    fondo_base64 = cargar_imagen_base64(RUTA_FONDO)
except FileNotFoundError:
    fondo_base64 = ""


# =========================================================
# CSS PERSONALIZADO
# =========================================================
st.markdown(
    f"""
    <style>

    /* -----------------------------------------------------
       FONDO GENERAL
    ----------------------------------------------------- */
    .stApp {{
        background:
            linear-gradient(
                90deg,
                rgba(4, 8, 18, 0.97) 0%,
                rgba(4, 8, 18, 0.91) 45%,
                rgba(4, 8, 18, 0.72) 100%
            ),
            url("data:image/jpg;base64,{fondo_base64}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* -----------------------------------------------------
       CONTENEDOR PRINCIPAL
    ----------------------------------------------------- */
    .block-container {{
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    /* -----------------------------------------------------
       OCULTAR ELEMENTOS DE STREAMLIT
    ----------------------------------------------------- */
    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        background: transparent !important;
    }}


    /* -----------------------------------------------------
       ENCABEZADO
    ----------------------------------------------------- */
    .hero {{
        padding: 1.5rem 0 2rem 0;
    }}

    .badge {{
        display: inline-block;
        padding: 7px 16px;
        border-radius: 50px;
        background: rgba(255, 58, 105, 0.13);
        border: 1px solid rgba(255, 74, 114, 0.45);
        color: #ff7899;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 15px;
    }}

    .main-title {{
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -1.5px;
        color: white;
        margin-bottom: 12px;
    }}

    .main-title span {{
        background: linear-gradient(
            90deg,
            #ff4b72,
            #ff87a6
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .subtitle {{
        color: #b7bfd0;
        max-width: 680px;
        font-size: 1.03rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }}


    /* -----------------------------------------------------
       TARJETAS DE VIDRIO
    ----------------------------------------------------- */
    .glass-card {{
        background: rgba(13, 20, 34, 0.68);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 25px;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0px 18px 50px rgba(0, 0, 0, 0.35);
        margin-bottom: 20px;
    }}

    .section-title {{
        font-size: 1.35rem;
        font-weight: 800;
        color: white;
        margin-bottom: 4px;
    }}

    .section-description {{
        color: #929aad;
        font-size: 0.92rem;
        margin-bottom: 15px;
    }}


    /* -----------------------------------------------------
       CAMPOS DE ENTRADA
    ----------------------------------------------------- */
    label {{
        color: #f1f4f8 !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: rgba(24, 31, 48, 0.90) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
    }}

    div[data-baseweb="input"] > div {{
        background-color: rgba(24, 31, 48, 0.90) !important;
        border-radius: 12px !important;
    }}

    input {{
        color: white !important;
    }}


    /* -----------------------------------------------------
       SLIDER
    ----------------------------------------------------- */
    div[data-baseweb="slider"] > div > div {{
        background-color: #ff4b72 !important;
    }}


    /* -----------------------------------------------------
       BOTÓN PRINCIPAL
    ----------------------------------------------------- */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {{
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 0.75rem 1rem;
        font-weight: 800;
        font-size: 1rem;
        color: white;

        background: linear-gradient(
            90deg,
            #e8325e,
            #ff597e
        );

        box-shadow: 0px 10px 30px rgba(232, 50, 94, 0.25);
        transition: 0.25s;
    }}

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {{
        transform: translateY(-2px);
        border: none;
        color: white;
        box-shadow: 0px 12px 35px rgba(255, 75, 114, 0.38);
    }}


    /* -----------------------------------------------------
       RESULTADO POSITIVO
    ----------------------------------------------------- */
    .resultado-si {{
        padding: 28px;
        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(131, 24, 51, 0.78),
                rgba(58, 16, 30, 0.70)
            );

        border: 1px solid rgba(255, 77, 114, 0.45);
        box-shadow: 0 15px 45px rgba(255, 50, 95, 0.18);
    }}

    .resultado-no {{
        padding: 28px;
        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(19, 73, 104, 0.78),
                rgba(9, 37, 62, 0.72)
            );

        border: 1px solid rgba(87, 183, 255, 0.42);
        box-shadow: 0 15px 45px rgba(38, 149, 255, 0.15);
    }}

    .resultado-label {{
        color: #b9c0ce;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.72rem;
        font-weight: 800;
    }}

    .resultado-grande {{
        font-size: 3.3rem;
        color: white;
        font-weight: 900;
        line-height: 1;
        margin-top: 7px;
        margin-bottom: 7px;
    }}

    .resultado-texto {{
        color: #dce1ea;
        font-size: 0.92rem;
    }}


    /* -----------------------------------------------------
       PROBABILIDADES
    ----------------------------------------------------- */
    .prob-card {{
        background: rgba(12, 18, 31, 0.72);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 20px;
        border-radius: 18px;
        margin-top: 12px;
    }}

    .prob-title {{
        color: white;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .prob-number {{
        font-size: 1.7rem;
        font-weight: 900;
        color: white;
    }}


    /* -----------------------------------------------------
       MÉTRICAS
    ----------------------------------------------------- */
    div[data-testid="stMetric"] {{
        background: rgba(13, 20, 34, 0.72);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 17px;
        border-radius: 18px;
        backdrop-filter: blur(12px);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #aab3c4;
    }}

    div[data-testid="stMetricValue"] {{
        color: white;
    }}


    /* -----------------------------------------------------
       DATAFRAME
    ----------------------------------------------------- */
    div[data-testid="stDataFrame"] {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.10);
    }}


    /* -----------------------------------------------------
       TABS
    ----------------------------------------------------- */
    button[data-baseweb="tab"] {{
        color: #aab3c4;
        font-weight: 700;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #ff668a;
    }}


    /* -----------------------------------------------------
       EXPANDER
    ----------------------------------------------------- */
    details {{
        background-color: rgba(13,20,34,0.70) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}


    /* -----------------------------------------------------
       DOWNLOAD BUTTON
    ----------------------------------------------------- */
    div[data-testid="stDownloadButton"] button {{
        width: 100%;
        border-radius: 13px;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        background: rgba(20, 27, 43, 0.85);
        font-weight: 700;
    }}

    div[data-testid="stDownloadButton"] button:hover {{
        border: 1px solid #ff668a;
        color: #ff668a;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CARGA DEL MODELO
# =========================================================
@st.cache_resource
def cargar_modelo():

    with open("modelo-cla.pkl", "rb") as archivo:

        modelo, labelencoder, variables, min_max_scaler = pickle.load(
            archivo
        )

    return (
        modelo,
        labelencoder,
        list(variables),
        min_max_scaler
    )


try:

    modelo, labelencoder, variables, min_max_scaler = cargar_modelo()

except FileNotFoundError:

    st.error(
        "No se encontró el archivo modelo-cla.pkl. "
        "Ejecuta primero el entrenamiento y guarda el modelo."
    )

    st.stop()


# =========================================================
# ENCABEZADO
# =========================================================
st.markdown(
    """
    <div class="hero">

        <div class="badge">
            ◉ MACHINE LEARNING · KNN
        </div>

        <div class="main-title">
            Predicción de <span>evento cardiovascular</span>
        </div>

        <div class="subtitle">
            Sistema académico de clasificación basado en Machine Learning.
            Ingresa la información del paciente para estimar la clase
            predicha por el modelo K-Nearest Neighbors.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================
tab_prediccion, tab_modelo = st.tabs(
    [
        "🫀 Predicción",
        "📊 Rendimiento del modelo"
    ]
)


# =========================================================
# TAB 1 - PREDICCIÓN
# =========================================================
with tab_prediccion:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                Información del paciente
            </div>

            <div class="section-description">
                Completa los siguientes datos para realizar la predicción.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    with st.form("formulario_prediccion"):

        col1, col2 = st.columns(
            2,
            gap="large"
        )


        # -------------------------------------------------
        # COLUMNA IZQUIERDA
        # -------------------------------------------------
        with col1:

            edad = st.slider(
                "Edad",
                min_value=1,
                max_value=82,
                value=45,
                step=1
            )

            glucosa = st.number_input(
                "Nivel promedio de glucosa",
                min_value=55.12,
                max_value=271.74,
                value=91.89,
                step=0.10,
                format="%.2f"
            )

            hipertension_ui = st.selectbox(
                "¿Tiene hipertensión?",
                ["No", "Sí"]
            )


        # -------------------------------------------------
        # COLUMNA DERECHA
        # -------------------------------------------------
        with col2:

            cardiopatia_ui = st.selectbox(
                "¿Tiene enfermedad cardíaca?",
                ["No", "Sí"]
            )

            casado_ui = st.selectbox(
                "¿Alguna vez se ha casado?",
                ["No", "Sí"]
            )

            fumador_ui = st.selectbox(
                "Estado de tabaquismo",
                [
                    "Nunca ha fumado",
                    "Fumó anteriormente",
                    "Fuma actualmente",
                    "Desconocido"
                ]
            )


        st.write("")

        enviar = st.form_submit_button(
            "Analizar paciente →",
            use_container_width=True
        )


    # =====================================================
    # REALIZAR PREDICCIÓN
    # =====================================================
    if enviar:

        mapa_si_no = {
            "No": "No",
            "Sí": "Yes"
        }


        mapa_fumador = {

            "Nunca ha fumado":
                "'never smoked'",

            "Fumó anteriormente":
                "'formerly smoked'",

            "Fuma actualmente":
                "smokes",

            "Desconocido":
                "Unknown"
        }


        datos = pd.DataFrame(
            [
                {
                    "age": edad,

                    "hypertension":
                        mapa_si_no[
                            hipertension_ui
                        ],

                    "heart_disease":
                        mapa_si_no[
                            cardiopatia_ui
                        ],

                    "ever_married":
                        mapa_si_no[
                            casado_ui
                        ],

                    "avg_glucose_level":
                        glucosa,

                    "smoking_status":
                        mapa_fumador[
                            fumador_ui
                        ]
                }
            ]
        )


        # =================================================
        # PREPROCESAMIENTO
        # =================================================
        data_preparada = datos.copy()


        data_preparada = pd.get_dummies(

            data_preparada,

            columns=[
                "smoking_status"
            ],

            drop_first=False,

            dtype=int
        )


        data_preparada = pd.get_dummies(

            data_preparada,

            columns=[
                "hypertension",
                "heart_disease",
                "ever_married"
            ],

            drop_first=False,

            dtype=int
        )


        data_preparada = data_preparada.reindex(

            columns=variables,

            fill_value=0
        )


        data_preparada[
            [
                "age",
                "avg_glucose_level"
            ]
        ] = min_max_scaler.transform(

            data_preparada[
                [
                    "age",
                    "avg_glucose_level"
                ]
            ]
        )


        # =================================================
        # PREDICCIÓN
        # =================================================
        prediccion_cod = int(
            modelo.predict(
                data_preparada
            )[0]
        )


        prediccion = str(

            labelencoder.inverse_transform(
                [
                    prediccion_cod
                ]
            )[0]
        )


        probabilidades = modelo.predict_proba(
            data_preparada
        )[0]


        etiquetas = labelencoder.inverse_transform(

            modelo.classes_.astype(
                int
            )
        )


        tabla_prob = pd.DataFrame(
            {
                "Clase":
                    etiquetas,

                "Probabilidad":
                    probabilidades
            }
        )


        tabla_prob[
            "Probabilidad (%)"
        ] = (

            tabla_prob[
                "Probabilidad"
            ]

            * 100

        ).round(2)


        # =================================================
        # TRADUCIR PROBABILIDADES
        # =================================================
        prob_no = 0
        prob_si = 0


        for _, fila in tabla_prob.iterrows():

            clase = str(
                fila["Clase"]
            ).strip().lower()

            probabilidad = float(
                fila["Probabilidad (%)"]
            )


            if clase in [
                "yes",
                "si",
                "sí",
                "1"
            ]:

                prob_si = probabilidad

            else:

                prob_no = probabilidad


        # =================================================
        # RESULTADO PRINCIPAL
        # =================================================
        st.write("")

        st.markdown(
            """
            <div class="section-title">
                Resultado del análisis
            </div>

            <div class="section-description">
                Clasificación generada por el modelo KNN.
            </div>
            """,
            unsafe_allow_html=True
        )


        resultado_positivo = (

            prediccion
            .strip()
            .lower()

            in [
                "yes",
                "si",
                "sí",
                "1"
            ]
        )


        if resultado_positivo:

            st.markdown(
                """
                <div class="resultado-si">

                    <div class="resultado-label">
                        Resultado de clasificación
                    </div>

                    <div class="resultado-grande">
                        SÍ
                    </div>

                    <div class="resultado-texto">
                        El modelo clasificó este registro
                        dentro de la clase positiva.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="resultado-no">

                    <div class="resultado-label">
                        Resultado de clasificación
                    </div>

                    <div class="resultado-grande">
                        NO
                    </div>

                    <div class="resultado-texto">
                        El modelo clasificó este registro
                        dentro de la clase negativa.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # PROBABILIDADES
        # =================================================
        st.write("")

        st.markdown(
            """
            <div class="section-title">
                Probabilidad estimada por clase
            </div>
            """,
            unsafe_allow_html=True
        )


        col_prob1, col_prob2 = st.columns(2)


        with col_prob1:

            st.markdown(
                f"""
                <div class="prob-card">

                    <div class="prob-title">
                        Clase NO
                    </div>

                    <div class="prob-number">
                        {prob_no:.1f} %
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                int(prob_no)
            )


        with col_prob2:

            st.markdown(
                f"""
                <div class="prob-card">

                    <div class="prob-title">
                        Clase SÍ
                    </div>

                    <div class="prob-number">
                        {prob_si:.1f} %
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                int(prob_si)
            )


        # =================================================
        # DATOS DEL PACIENTE
        # =================================================
        st.write("")

        st.markdown(
            """
            <div class="section-title">
                Resumen del paciente
            </div>
            """,
            unsafe_allow_html=True
        )


        resumen = pd.DataFrame(
            {
                "Variable": [

                    "Edad",

                    "Glucosa promedio",

                    "Hipertensión",

                    "Enfermedad cardíaca",

                    "Alguna vez casado",

                    "Tabaquismo"
                ],

                "Valor": [

                    edad,

                    f"{glucosa:.2f}",

                    hipertension_ui,

                    cardiopatia_ui,

                    casado_ui,

                    fumador_ui
                ]
            }
        )


        st.dataframe(

            resumen,

            hide_index=True,

            use_container_width=True
        )


        # =================================================
        # DESCARGAR RESULTADO
        # =================================================
        resultado_descarga = datos.copy()


        resultado_descarga[
            "prediccion_modelo"
        ] = prediccion


        resultado_descarga[
            "probabilidad_no"
        ] = prob_no / 100


        resultado_descarga[
            "probabilidad_si"
        ] = prob_si / 100


        st.download_button(

            "⬇ Descargar resultado",

            data=resultado_descarga
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                ),

            file_name=
                "resultado_prediccion.csv",

            mime=
                "text/csv",

            use_container_width=True
        )


        with st.expander(
            "Ver variables preparadas para el modelo"
        ):

            st.dataframe(

                data_preparada,

                use_container_width=True
            )


        st.caption(
            "Este sistema fue desarrollado con fines académicos. "
            "La clasificación del modelo no representa un diagnóstico médico."
        )


# =========================================================
# TAB 2 - RENDIMIENTO
# =========================================================
with tab_modelo:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                Rendimiento del modelo
            </div>

            <div class="section-description">
                Información obtenida durante el proceso
                de validación cruzada.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Accuracy promedio observado en la comparación
    # de validación cruzada que mostraste.
    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Modelo",
            "KNN"
        )


    with col2:

        st.metric(
            "Validación",
            "10 folds"
        )


    with col3:

        st.metric(
            "Accuracy promedio CV",
            "80.52 %"
        )


    st.write("")


    comparacion_modelos = pd.DataFrame(
        {
            "Modelo": [
                "Tree",
                "Random Forest",
                "KNN",
                "Red neuronal",
                "SVM"
            ],

            "Accuracy promedio (%)": [
                72.93,
                79.61,
                80.52,
                77.05,
                76.00
            ]
        }
    )


    st.markdown(
        """
        <div class="section-title">
            Comparación de modelos
        </div>

        <div class="section-description">
            Promedio obtenido en las 10 particiones
            de validación cruzada.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.bar_chart(

        comparacion_modelos.set_index(
            "Modelo"
        )
    )


    st.dataframe(

        comparacion_modelos,

        hide_index=True,

        use_container_width=True
    )


    st.info(
        "KNN obtuvo el mayor accuracy promedio "
        "entre los modelos evaluados en la validación cruzada."
    )


# =========================================================
# PIE DE PÁGINA
# =========================================================
st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7f8899;
        font-size:0.78rem;
        padding-top:30px;
    ">

        CardioPredict · Proyecto académico de Machine Learning

    </div>
    """,
    unsafe_allow_html=True
)
