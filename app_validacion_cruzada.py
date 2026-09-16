
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
RUTA_ICONO = APP_DIR / "corazon_icono.png"


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def html(contenido):
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
icono_base64 = cargar_imagen_base64(RUTA_ICONO)

if fondo_base64:
    fondo_css = (
        "linear-gradient(90deg, rgba(3,7,18,.96) 0%, "
        "rgba(4,9,22,.88) 48%, rgba(4,9,22,.68) 100%), "
        f'url("data:image/jpeg;base64,{fondo_base64}")'
    )
else:
    fondo_css = (
        "radial-gradient(circle at 80% 20%, rgba(255, 79, 123, .16), transparent 30%), "
        "radial-gradient(circle at 20% 85%, rgba(97, 184, 255, .14), transparent 30%), "
        "linear-gradient(135deg, #050914 0%, #08111f 55%, #02050b 100%)"
    )


# =========================================================
# CSS PRINCIPAL
# =========================================================
html(
    f"""
    <style>
    :root {{
        --pink: #ff4f7b;
        --pink-soft: #ff90ac;
        --blue: #71c1ff;
        --text: #f7f9fc;
        --muted: #aab4c7;
        --panel: rgba(10, 17, 31, 0.72);
        --panel-strong: rgba(10, 17, 31, 0.88);
        --border: rgba(255, 255, 255, 0.12);
    }}

    /* Fondo general */
    [data-testid="stAppViewContainer"] {{
        background: {fondo_css};
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        overflow: hidden;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background:
            radial-gradient(circle at 78% 18%, rgba(44,154,255,.10), transparent 24%),
            radial-gradient(circle at 24% 82%, rgba(255,79,123,.10), transparent 24%);
        animation: glowMove 14s ease-in-out infinite alternate;
    }}

    @keyframes glowMove {{
        0% {{
            transform: translate(0px, 0px) scale(1);
        }}
        100% {{
            transform: translate(-10px, 10px) scale(1.04);
        }}
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        position: relative;
        z-index: 2;
    }}

    /* Corazones flotantes */
    .hearts-layer {{
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }}

    .heart-float {{
        position: absolute;
        background-image: url("data:image/png;base64,{icono_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.14;
        filter: drop-shadow(0 0 16px rgba(255, 79, 123, 0.20));
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
    }}

    .heart-1 {{
        width: 95px; height: 95px;
        top: 6%; left: 3%;
        animation: float1 8s infinite;
    }}

    .heart-2 {{
        width: 75px; height: 75px;
        top: 14%; right: 6%;
        animation: float2 10s infinite;
    }}

    .heart-3 {{
        width: 105px; height: 105px;
        top: 38%; left: 1%;
        animation: float3 9s infinite;
    }}

    .heart-4 {{
        width: 85px; height: 85px;
        top: 52%; right: 3%;
        animation: float4 11s infinite;
    }}

    .heart-5 {{
        width: 110px; height: 110px;
        bottom: 10%; left: 6%;
        animation: float5 9s infinite;
    }}

    .heart-6 {{
        width: 72px; height: 72px;
        bottom: 7%; right: 9%;
        animation: float6 8s infinite;
    }}

    .heart-7 {{
        width: 68px; height: 68px;
        top: 74%; left: 37%;
        animation: float7 12s infinite;
    }}

    .heart-8 {{
        width: 60px; height: 60px;
        top: 28%; right: 29%;
        animation: float8 9.5s infinite;
    }}

    @keyframes float1 {{
        0%, 100% {{ transform: translateY(0px) rotate(-8deg) scale(1); }}
        50% {{ transform: translateY(-18px) rotate(6deg) scale(1.04); }}
    }}

    @keyframes float2 {{
        0%, 100% {{ transform: translateY(0px) translateX(0px) rotate(8deg); }}
        50% {{ transform: translateY(-14px) translateX(-8px) rotate(-8deg); }}
    }}

    @keyframes float3 {{
        0%, 100% {{ transform: translateY(0px) rotate(-10deg); }}
        50% {{ transform: translateY(-20px) rotate(10deg); }}
    }}

    @keyframes float4 {{
        0%, 100% {{ transform: translateY(0px) translateX(0px) rotate(12deg); }}
        50% {{ transform: translateY(-16px) translateX(7px) rotate(-4deg); }}
    }}

    @keyframes float5 {{
        0%, 100% {{ transform: translateY(0px) rotate(-6deg) scale(1); }}
        50% {{ transform: translateY(-18px) rotate(8deg) scale(1.05); }}
    }}

    @keyframes float6 {{
        0%, 100% {{ transform: translateY(0px) translateX(0px) rotate(10deg); }}
        50% {{ transform: translateY(-12px) translateX(-8px) rotate(-6deg); }}
    }}

    @keyframes float7 {{
        0%, 100% {{ transform: translateY(0px) rotate(-14deg); }}
        50% {{ transform: translateY(-10px) rotate(7deg); }}
    }}

    @keyframes float8 {{
        0%, 100% {{ transform: translateY(0px) rotate(6deg); }}
        50% {{ transform: translateY(-15px) rotate(-7deg); }}
    }}

    /* Encabezado */
    .hero {{
        max-width: 800px;
        padding: 1.2rem 0 1.4rem 0;
        position: relative;
        z-index: 2;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .45rem .9rem;
        border: 1px solid rgba(255,79,123,.40);
        background: rgba(255,79,123,.10);
        border-radius: 999px;
        color: #ff9ab3;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
        animation: pulseBadge 2.2s infinite;
    }}

    @keyframes pulseBadge {{
        0%, 100% {{
            box-shadow: 0 0 0 rgba(255,79,123,0);
        }}
        50% {{
            box-shadow: 0 0 20px rgba(255,79,123,.18);
        }}
    }}

    .hero-title {{
        margin: 0;
        color: var(--text);
        font-size: clamp(2.5rem, 5vw, 4.6rem);
        line-height: .97;
        font-weight: 950;
        letter-spacing: -.06em;
    }}

    .hero-title span {{
        background: linear-gradient(90deg, #ff4f7b 0%, #ff9ab3 52%, #72c3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: shimmer 5s linear infinite;
    }}

    @keyframes shimmer {{
        0% {{ background-position: 0% center; }}
        100% {{ background-position: 200% center; }}
    }}

    .hero-subtitle {{
        max-width: 690px;
        margin-top: 1rem;
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.65;
    }}

    .mini-line {{
        width: 86px;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--pink), var(--blue));
        margin-top: 1.15rem;
        box-shadow: 0 0 22px rgba(255,79,123,.35);
        animation: linePulse 2.8s ease-in-out infinite;
    }}

    @keyframes linePulse {{
        0%, 100% {{ transform: scaleX(1); opacity: 1; }}
        50% {{ transform: scaleX(1.15); opacity: .82; }}
    }}

    /* Secciones */
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

    /* Formulario */
    div[data-testid="stForm"] {{
        background: linear-gradient(
            135deg,
            rgba(12, 20, 36, .84),
            rgba(8, 14, 27, .67)
        );
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.3rem 1.3rem 1rem 1.3rem;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 22px 65px rgba(0, 0, 0, .34);
        position: relative;
        overflow: hidden;
    }}

    div[data-testid="stForm"]::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            120deg,
            transparent 0%,
            rgba(255,255,255,.03) 35%,
            transparent 70%
        );
        animation: formGlow 7s linear infinite;
        pointer-events: none;
    }}

    @keyframes formGlow {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
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

    div[data-baseweb="slider"] > div > div {{
        background-color: #ff5c83 !important;
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
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 16px 38px rgba(255,85,126,.36);
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        color: #b5bfd0;
        font-weight: 750;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #ff789a;
    }}

    /* Tarjetas de resultados */
    .result-card {{
        border-radius: 24px;
        padding: 1.5rem 1.6rem;
        min-height: 210px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid var(--border);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 20px 55px rgba(0,0,0,.30);
        animation: cardRise .55s ease;
    }}

    @keyframes cardRise {{
        from {{
            opacity: 0;
            transform: translateY(14px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0px);
        }}
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
        font-size: 4rem;
        line-height: 1;
        font-weight: 950;
        letter-spacing: -.05em;
        margin: .45rem 0;
        animation: heartbeat 1.8s ease-in-out infinite;
        transform-origin: center;
    }}

    @keyframes heartbeat {{
        0%, 100% {{ transform: scale(1); }}
        10% {{ transform: scale(1.05); }}
        20% {{ transform: scale(.98); }}
        30% {{ transform: scale(1.08); }}
        40% {{ transform: scale(1); }}
    }}

    .result-copy {{
        color: #d8deea;
        font-size: .92rem;
        line-height: 1.5;
    }}

    /* Probabilidades */
    .prob-card {{
        background: rgba(8, 15, 28, .78);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.2rem 1.2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        min-height: 210px;
        animation: cardRise .55s ease;
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
        height: 10px;
        background: rgba(255,255,255,.08);
        border-radius: 999px;
        overflow: hidden;
        margin-top: .35rem;
    }}

    .prob-fill-no {{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #3e9be0, #78c8ff);
        animation: growBar 1.2s ease;
    }}

    .prob-fill-si {{
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #d92758, #ff7998);
        animation: growBar 1.2s ease;
    }}

    @keyframes growBar {{
        from {{ width: 0%; }}
    }}

    /* Métricas y tablas */
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

    @media (max-width: 768px) {{
        .heart-float {{
            opacity: 0.08;
        }}

        .block-container {{
            padding-top: 1.2rem;
        }}

        .hero-title {{
            font-size: 2.8rem;
        }}
    }}
    </style>
    """
)


# =========================================================
# CAPA DE CORAZONES FLOTANTES
# =========================================================
if icono_base64:
    html(
        """
        <div class="hearts-layer">
            <div class="heart-float heart-1"></div>
            <div class="heart-float heart-2"></div>
            <div class="heart-float heart-3"></div>
            <div class="heart-float heart-4"></div>
            <div class="heart-float heart-5"></div>
            <div class="heart-float heart-6"></div>
            <div class="heart-float heart-7"></div>
            <div class="heart-float heart-8"></div>
        </div>
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
        "No se encontró 'modelo-cla.pkl'. Debe estar en la misma carpeta que esta aplicación."
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


# =========================================================
# TABS
# =========================================================
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

        st.toast("Predicción generada correctamente", icon="🫀")

        # -------------------------------------------------
        # Conversión a los valores originales del dataset
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
        # Preprocesamiento igual al entrenamiento
        # -------------------------------------------------
        data_preparada = datos.copy()

        data_preparada = pd.get_dummies(
            data_preparada,
            columns=["smoking_status"],
            drop_first=False,
            dtype=int,
        )

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
        # Predicción
        # -------------------------------------------------
        prediccion_cod = int(modelo.predict(data_preparada)[0])

        prediccion = str(
            labelencoder.inverse_transform([prediccion_cod])[0]
        )

        probabilidades = modelo.predict_proba(data_preparada)[0]

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
        # Resultado visual
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

        col_resultado, col_prob = st.columns([1.05, 1], gap="large")

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
                    <div class="prob-big">{max(prob_no, prob_si):.1f} %</div>

                    <div class="prob-row">
                        <span>Clase NO</span>
                        <strong>{prob_no:.1f} %</strong>
                    </div>
                    <div class="prob-track">
                        <div class="prob-fill-no" style="width:{prob_no:.2f}%"></div>
                    </div>

                    <div class="prob-row" style="margin-top:.9rem;">
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
            data=resultado_descarga.to_csv(index=False).encode("utf-8"),
            file_name="resultado_prediccion.csv",
            mime="text/csv",
            use_container_width=True,
        )

        with st.expander("Ver variables preparadas para el modelo"):
            st.dataframe(
                data_preparada,
                use_container_width=True,
            )

        st.caption(
            "Uso académico. La salida del modelo no constituye un diagnóstico médico ni una probabilidad clínica individual."
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
                La tabla comparacion_CV corresponde a F1 macro promedio en los 10 folds.
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
        "KNN presentó el mayor F1 macro promedio dentro de los modelos comparados."
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
