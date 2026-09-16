

import pickle
import base64
import textwrap
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
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
RUTA_MODELO = APP_DIR / "modelo-cla.pkl"
RUTA_FONDO = APP_DIR / "corazon1.jpg"


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def html(contenido):
    """
    Renderiza HTML evitando que Streamlit lo interprete como bloque de código.
    """
    st.markdown(
        textwrap.dedent(contenido).strip(),
        unsafe_allow_html=True,
    )


def cargar_imagen_base64(ruta):
    if not ruta.exists():
        return ""
    with open(ruta, "rb") as imagen:
        return base64.b64encode(imagen.read()).decode("utf-8")


fondo_base64 = cargar_imagen_base64(RUTA_FONDO)

if fondo_base64:
    fondo_css = (
        "linear-gradient(90deg, rgba(3,7,18,.96) 0%, "
        "rgba(4,9,22,.89) 48%, rgba(4,9,22,.66) 100%), "
        f'url("data:image/jpeg;base64,{fondo_base64}")'
    )
else:
    fondo_css = (
        "radial-gradient(circle at 78% 20%, rgba(218,0,81,.18), transparent 30%), "
        "linear-gradient(135deg, #050914 0%, #08111f 55%, #02050b 100%)"
    )


# =========================================================
# CSS
# =========================================================
html(
    f"""
    <style>
    :root {{
        --pink: #ff4f7b;
        --pink-soft: #ff8cab;
        --blue: #61b8ff;
        --text: #f7f9fc;
        --muted: #aab4c7;
        --panel: rgba(10, 17, 31, 0.72);
        --panel-strong: rgba(10, 17, 31, 0.88);
        --border: rgba(255, 255, 255, 0.12);
    }}

    [data-testid="stAppViewContainer"] {{
        background: {fondo_css};
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 78% 18%, rgba(44,154,255,.13), transparent 24%),
            radial-gradient(circle at 22% 82%, rgba(255,79,123,.10), transparent 24%);
        z-index: 0;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
        position: relative;
        z-index: 1;
    }}

    .hero {{
        max-width: 790px;
        padding: 1.2rem 0 1.5rem 0;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .45rem .9rem;
        border: 1px solid rgba(255,79,123,.38);
        background: rgba(255,79,123,.10);
        border-radius: 999px;
        color: #ff91ad;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}

    .hero-title {{
        margin: 0;
        color: var(--text);
        font-size: clamp(2.4rem, 5vw, 4.4rem);
        line-height: .98;
        font-weight: 900;
        letter-spacing: -.055em;
    }}

    .hero-title span {{
        background: linear-gradient(90deg, #ff4f7b 0%, #ff9ab3 55%, #72c3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .hero-subtitle {{
        max-width: 690px;
        margin-top: 1rem;
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.65;
    }}

    .mini-line {{
        width: 74px;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--pink), var(--blue));
        margin-top: 1.1rem;
        box-shadow: 0 0 20px rgba(255,79,123,.35);
    }}

    /* Formulario como tarjeta glass real */
    div[data-testid="stForm"] {{
        background: linear-gradient(
            135deg,
            rgba(12, 20, 36, .84),
            rgba(8, 14, 27, .67)
        );
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 22px 65px rgba(0, 0, 0, .34);
    }}

    .section-heading {{
        margin: .35rem 0 1rem 0;
    }}

    .section-kicker {{
        color: #ff88a6;
        font-size: .74rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .25rem;
    }}

    .section-title {{
        color: var(--text);
        font-size: 1.55rem;
        font-weight: 850;
        margin: 0;
    }}

    .section-copy {{
        color: var(--muted);
        font-size: .91rem;
        margin-top: .28rem;
    }}

    label,
    [data-testid="stWidgetLabel"] p {{
        color: #f2f5fa !important;
        font-weight: 650 !important;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background: rgba(24, 31, 47, .92) !important;
        border: 1px solid rgba(255,255,255,.10) !important;
        border-radius: 12px !important;
    }}

    input {{
        color: white !important;
    }}

    div[data-testid="stFormSubmitButton"] button {{
        width: 100%;
        min-height: 3rem;
        border: 0 !important;
        border-radius: 14px;
        color: white !important;
        font-weight: 800;
        background: linear-gradient(90deg, #d92758 0%, #ff557e 55%, #ff7695 100%);
        box-shadow: 0 13px 34px rgba(217,39,88,.26);
        transition: transform .18s ease, box-shadow .18s ease;
    }}

    div[data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 16px 38px rgba(255,85,126,.36);
    }}

    button[data-baseweb="tab"] {{
        color: #b5bfd0;
        font-weight: 750;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #ff789a;
    }}

    .result-card {{
        border-radius: 24px;
        padding: 1.45rem 1.55rem;
        min-height: 185px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid var(--border);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 20px 55px rgba(0,0,0,.30);
    }}

    .result-positive {{
        background:
            radial-gradient(circle at 90% 10%, rgba(255,111,145,.24), transparent 35%),
            linear-gradient(135deg, rgba(95,21,46,.88), rgba(33,12,25,.82));
        border-color: rgba(255,92,130,.35);
    }}

    .result-negative {{
        background:
            radial-gradient(circle at 90% 10%, rgba(91,184,255,.22), transparent 35%),
            linear-gradient(135deg, rgba(13,61,91,.88), rgba(7,25,42,.84));
        border-color: rgba(91,184,255,.34);
    }}

    .result-label {{
        color: #c5ccda;
        font-size: .72rem;
        font-weight: 850;
        letter-spacing: .12em;
        text-transform: uppercase;
    }}

    .result-value {{
        color: white;
        font-size: 3.8rem;
        line-height: 1;
        font-weight: 950;
        letter-spacing: -.05em;
        margin: .45rem 0;
    }}

    .result-copy {{
        color: #d8deea;
        font-size: .92rem;
        line-height: 1.5;
    }}

    .prob-card {{
        background: rgba(8, 15, 28, .78);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.15rem 1.2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        min-height: 185px;
    }}

    .prob-caption {{
        color: #aeb8ca;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .09em;
        text-transform: uppercase;
    }}

    .prob-big {{
        color: white;
        font-size: 2.5rem;
        font-weight: 900;
        line-height: 1;
        margin: .55rem 0 .85rem 0;
    }}

    .prob-row {{
        display: flex;
        justify-content: space-between;
        color: #d8deea;
        font-size: .88rem;
        margin-top: .45rem;
    }}

    .prob-track {{
        width: 100%;
        height: 9px;
        background: rgba(255,255,255,.08);
        border-radius: 999px;
        overflow: hidden;
        margin-top: .35rem;
    }}

    .prob-fill-no {{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #3e9be0, #78c8ff);
    }}

    .prob-fill-si {{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #d92758, #ff7998);
    }}

    .summary-panel {{
        background: rgba(8, 15, 28, .72);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }}

    div[data-testid="stMetric"] {{
        background: rgba(8, 15, 28, .76);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #aeb8ca;
    }}

    div[data-testid="stMetricValue"] {{
        color: white;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 16px;
        overflow: hidden;
    }}

    details {{
        background: rgba(8,15,28,.75) !important;
        border: 1px solid rgba(255,255,255,.10) !important;
        border-radius: 15px !important;
    }}

    div[data-testid="stDownloadButton"] button {{
        width: 100%;
        border-radius: 13px;
        border: 1px solid rgba(255,255,255,.16);
        color: white;
        background: rgba(17,25,41,.88);
        font-weight: 750;
    }}

    div[data-testid="stDownloadButton"] button:hover {{
        color: #ff85a4;
        border-color: rgba(255,133,164,.55);
    }}

    .footer-note {{
        text-align: center;
        color: #7f8ba0;
        font-size: .78rem;
        padding: 2rem 0 .5rem 0;
    }}

    @media (max-width: 760px) {{
        .block-container {{
            padding-top: 1.2rem;
        }}
        .hero-title {{
            font-size: 2.7rem;
        }}
    }}
    </style>
    """
)


# =========================================================
# CARGA DEL MODELO
# =========================================================
@st.cache_resource
def cargar_modelo():
    with open(RUTA_MODELO, "rb") as archivo:
        modelo, labelencoder, variables, min_max_scaler = pickle.load(archivo)

    return modelo, labelencoder, list(variables), min_max_scaler


try:
    modelo, labelencoder, variables, min_max_scaler = cargar_modelo()
except FileNotFoundError:
    st.error(
        "No se encontró 'modelo-cla.pkl'. "
        "Debe estar en la misma carpeta que esta aplicación."
    )
    st.stop()


# =========================================================
# ENCABEZADO
# =========================================================
html(
    """
    <section class="hero">
        <div class="hero-badge">Machine Learning · KNN</div>
        <h1 class="hero-title">
            Predicción de <span>evento cardiovascular</span>
        </h1>
        <div class="hero-subtitle">
            Aplicación académica para clasificar un registro a partir de edad,
            glucosa, antecedentes y hábitos. El modelo final fue K-Nearest
            Neighbors y se evaluó mediante validación cruzada estratificada.
        </div>
        <div class="mini-line"></div>
    </section>
    """
)


tab_prediccion, tab_modelo = st.tabs(
    ["🫀 Predicción", "📊 Rendimiento del modelo"]
)


# =========================================================
# TAB 1 - PREDICCIÓN
# =========================================================
with tab_prediccion:

    html(
        """
        <div class="section-heading">
            <div class="section-kicker">Datos de entrada</div>
            <div class="section-title">Información del paciente</div>
            <div class="section-copy">
                Completa los campos y presiona “Analizar paciente”.
            </div>
        </div>
        """
    )

    with st.form("formulario_prediccion"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            edad = st.slider(
                "Edad",
                min_value=1,
                max_value=82,
                value=45,
                step=1,
            )

            glucosa = st.number_input(
                "Nivel promedio de glucosa",
                min_value=55.12,
                max_value=271.74,
                value=91.89,
                step=0.10,
                format="%.2f",
            )

            hipertension_ui = st.selectbox(
                "¿Tiene hipertensión?",
                ["No", "Sí"],
            )

        with col2:
            cardiopatia_ui = st.selectbox(
                "¿Tiene enfermedad cardíaca?",
                ["No", "Sí"],
            )

            casado_ui = st.selectbox(
                "¿Alguna vez se ha casado?",
                ["No", "Sí"],
            )

            fumador_ui = st.selectbox(
                "Estado de tabaquismo",
                [
                    "Nunca ha fumado",
                    "Fumó anteriormente",
                    "Fuma actualmente",
                    "Desconocido",
                ],
            )

        st.write("")

        enviar = st.form_submit_button(
            "Analizar paciente  →",
            use_container_width=True,
        )

    if enviar:
        # -------------------------------------------------
        # Conversión a los valores del dataset original
        # -------------------------------------------------
        mapa_si_no = {
            "No": "No",
            "Sí": "Yes",
        }

        mapa_fumador = {
            "Nunca ha fumado": "'never smoked'",
            "Fumó anteriormente": "'formerly smoked'",
            "Fuma actualmente": "smokes",
            "Desconocido": "Unknown",
        }

        datos = pd.DataFrame(
            [
                {
                    "age": edad,
                    "hypertension": mapa_si_no[hipertension_ui],
                    "heart_disease": mapa_si_no[cardiopatia_ui],
                    "ever_married": mapa_si_no[casado_ui],
                    "avg_glucose_level": glucosa,
                    "smoking_status": mapa_fumador[fumador_ui],
                }
            ]
        )

        # -------------------------------------------------
        # MISMO ESQUEMA DE VARIABLES DEL ENTRENAMIENTO
        # -------------------------------------------------
        data_preparada = datos.copy()

        data_preparada = pd.get_dummies(
            data_preparada,
            columns=["smoking_status"],
            drop_first=False,
            dtype=int,
        )

        # En entrenamiento las variables binarias quedaron como *_Yes.
        # En un único registro usamos drop_first=False y luego reindexamos
        # para conservar correctamente el 1 cuando la respuesta es "Yes".
        data_preparada = pd.get_dummies(
            data_preparada,
            columns=[
                "hypertension",
                "heart_disease",
                "ever_married",
            ],
            drop_first=False,
            dtype=int,
        )

        data_preparada = data_preparada.reindex(
            columns=variables,
            fill_value=0,
        )

        data_preparada[
            ["age", "avg_glucose_level"]
        ] = min_max_scaler.transform(
            data_preparada[["age", "avg_glucose_level"]]
        )

        # -------------------------------------------------
        # PREDICCIÓN
        # -------------------------------------------------
        prediccion_cod = int(
            modelo.predict(data_preparada)[0]
        )

        prediccion = str(
            labelencoder.inverse_transform([prediccion_cod])[0]
        )

        probabilidades = modelo.predict_proba(
            data_preparada
        )[0]

        etiquetas = labelencoder.inverse_transform(
            modelo.classes_.astype(int)
        )

        tabla_prob = pd.DataFrame(
            {
                "Clase": etiquetas,
                "Probabilidad": probabilidades,
            }
        )

        prob_no = 0.0
        prob_si = 0.0

        for _, fila in tabla_prob.iterrows():
            clase = str(fila["Clase"]).strip().lower()
            prob = float(fila["Probabilidad"]) * 100

            if clase in ["yes", "si", "sí", "1"]:
                prob_si = prob
            else:
                prob_no = prob

        resultado_positivo = (
            prediccion.strip().lower()
            in ["yes", "si", "sí", "1"]
        )

        # -------------------------------------------------
        # RESULTADO
        # -------------------------------------------------
        st.write("")

        html(
            """
            <div class="section-heading">
                <div class="section-kicker">Predicción</div>
                <div class="section-title">Resultado del análisis</div>
                <div class="section-copy">
                    Clasificación obtenida con el modelo KNN.
                </div>
            </div>
            """
        )

        col_resultado, col_prob = st.columns(
            [1.05, 1],
            gap="large",
        )

        with col_resultado:
            if resultado_positivo:
                html(
                    """
                    <div class="result-card result-positive">
                        <div class="result-label">Resultado de clasificación</div>
                        <div class="result-value">SÍ</div>
                        <div class="result-copy">
                            El registro fue clasificado dentro de la clase positiva.
                        </div>
                    </div>
                    """
                )
            else:
                html(
                    """
                    <div class="result-card result-negative">
                        <div class="result-label">Resultado de clasificación</div>
                        <div class="result-value">NO</div>
                        <div class="result-copy">
                            El registro fue clasificado dentro de la clase negativa.
                        </div>
                    </div>
                    """
                )

        with col_prob:
            html(
                f"""
                <div class="prob-card">
                    <div class="prob-caption">Probabilidad estimada por clase</div>
                    <div class="prob-big">
                        {max(prob_no, prob_si):.1f} %
                    </div>

                    <div class="prob-row">
                        <span>Clase NO</span>
                        <strong>{prob_no:.1f} %</strong>
                    </div>
                    <div class="prob-track">
                        <div class="prob-fill-no" style="width:{prob_no:.2f}%"></div>
                    </div>

                    <div class="prob-row" style="margin-top:.85rem;">
                        <span>Clase SÍ</span>
                        <strong>{prob_si:.1f} %</strong>
                    </div>
                    <div class="prob-track">
                        <div class="prob-fill-si" style="width:{prob_si:.2f}%"></div>
                    </div>
                </div>
                """
            )

        st.write("")

        html(
            """
            <div class="section-heading">
                <div class="section-title">Resumen del caso ingresado</div>
            </div>
            """
        )

        resumen = pd.DataFrame(
            {
                "Variable": [
                    "Edad",
                    "Glucosa promedio",
                    "Hipertensión",
                    "Enfermedad cardíaca",
                    "Alguna vez casado",
                    "Tabaquismo",
                ],
                "Valor": [
                    edad,
                    f"{glucosa:.2f}",
                    hipertension_ui,
                    cardiopatia_ui,
                    casado_ui,
                    fumador_ui,
                ],
            }
        )

        st.dataframe(
            resumen,
            hide_index=True,
            use_container_width=True,
        )

        resultado_descarga = datos.copy()
        resultado_descarga["prediccion_modelo"] = prediccion
        resultado_descarga["probabilidad_no"] = prob_no / 100
        resultado_descarga["probabilidad_si"] = prob_si / 100

        st.download_button(
            "⬇ Descargar resultado en CSV",
            data=resultado_descarga.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="resultado_prediccion.csv",
            mime="text/csv",
            use_container_width=True,
        )

        with st.expander(
            "Ver variables preparadas para el modelo"
        ):
            st.dataframe(
                data_preparada,
                use_container_width=True,
            )

        st.caption(
            "Uso académico. La salida del modelo no constituye "
            "un diagnóstico médico ni una probabilidad clínica individual."
        )


# =========================================================
# TAB 2 - VALIDACIÓN CRUZADA
# =========================================================
with tab_modelo:

    html(
        """
        <div class="section-heading">
            <div class="section-kicker">Validación cruzada</div>
            <div class="section-title">Comparación del desempeño</div>
            <div class="section-copy">
                La tabla comparacion_CV del notebook guarda test_f1_macro,
                por lo que estos valores corresponden a F1 macro, no a accuracy.
            </div>
        </div>
        """
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Modelo desplegado", "KNN")

    with col_b:
        st.metric("Particiones", "10 folds")

    with col_c:
        st.metric("F1 macro promedio KNN", "80.52 %")

    comparacion_modelos = pd.DataFrame(
        {
            "Modelo": [
                "Tree",
                "Random Forest",
                "KNN",
                "Red neuronal",
                "SVM",
            ],
            "F1 macro promedio (%)": [
                72.92,
                79.61,
                80.52,
                77.05,
                76.00,
            ],
        }
    )

    st.write("")
    st.bar_chart(
        comparacion_modelos.set_index("Modelo"),
        horizontal=True,
    )

    st.dataframe(
        comparacion_modelos,
        hide_index=True,
        use_container_width=True,
    )

    st.info(
        "En la comparación mostrada, KNN presenta el F1 macro promedio "
        "más alto entre los modelos evaluados."
    )


# =========================================================
# PIE DE PÁGINA
# =========================================================
html(
    """
    <div class="footer-note">
        CardioPredict · Proyecto académico de Machine Learning
    </div>
    """
)
