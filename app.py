# -*- coding: utf-8 -*-
import streamlit as st
import base64, time, json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Guía de Reunión · Equipo #5 ENS",
    page_icon="✝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
LOGO_PATH    = Path(__file__).parent / "assets" / "logo.png"
REVIEWS_FILE = Path(__file__).parent / "reviews.json"
AUDIO_PATH   = Path(__file__).parent / "assets" / "cancion.mp3"
PAPIRO_PATH  = Path(__file__).parent / "assets" / "papiro.jpg"

REVIEWERS = [
    {"id":"DÍAZ ARIAS",                 "label":"DÍAZ ARIAS",                        "tipo":"pareja",      "icon":"👫", "fg":"#1B3A6B","bg":"#D6E4F7"},
    {"id":"RODRÍGUEZ ORTIZ",            "label":"RODRÍGUEZ ORTIZ",                   "tipo":"pareja",      "icon":"👫", "fg":"#A62020","bg":"#FDECEA"},
    {"id":"PRIETO HOYOS",               "label":"PRIETO HOYOS",                      "tipo":"pareja",      "icon":"👫", "fg":"#C9930A","bg":"#FFF8E1"},
    {"id":"OJEDA RODRÍGUEZ",            "label":"OJEDA RODRÍGUEZ",                   "tipo":"pareja",      "icon":"👫", "fg":"#2E7D32","bg":"#E8F5E9"},
    {"id":"OMAR Y SONIA",               "label":"OMAR Y SONIA",                      "tipo":"sector",      "icon":"🌟", "fg":"#B35C00","bg":"#FFF3E0"},
    {"id":"P. FAIDER SANTIAGO",         "label":"P. Faider Julián Santiago Díaz",    "tipo":"consiliario", "icon":"✝",  "fg":"#6A1B9A","bg":"#F3E5F5"},
]

# ── Datos de la reunión actual ─────────────────────────────────────────────────
MEETING_DATE  = "Mayo 29 de 2026"
MEETING_HOST  = "LUZ MARY Y HOLLMAN · OJEDA RODRÍGUEZ"
MEETING_TEMA  = "EL AMOR ES MUCHO MÁS QUE EL AMOR — Cap. 3: Incompletitud y Gratuidad"
MEETING_QUOTE = (
    '"En realidad lo que les faltaba era una persona complementaria. '
    'No alguien que pudiera ayudarles a colmar sus lagunas... sino alguien que les aportara '
    'lo que jamás podrían conseguir por ellos mismos: la otra mitad del mundo."'
)

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_B64   = img_b64(LOGO_PATH)   if LOGO_PATH.exists()   else ""
PAPIRO_B64 = img_b64(PAPIRO_PATH) if PAPIRO_PATH.exists() else ""

# URL pública de la app — actualizar cuando se despliegue en Streamlit Cloud
APP_URL = "https://ens-equipo5-reunion.streamlit.app"

# ─────────────────────────────────────────────────────────────────────────────
#  REVIEWS PERSISTENCE
#  • @st.cache_resource  → dict compartido entre TODOS los usuarios del mismo
#    link mientras la app esté viva (funciona en Streamlit Cloud sin BD externa)
#  • JSON local          → respaldo cuando se corre en el computador
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def _store():
    """Un solo dict en memoria compartido por todas las sesiones."""
    data = {}
    if REVIEWS_FILE.exists():
        try:
            data = json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return data          # devuelve la referencia mutable

def load_reviews():
    return _store()

def save_review(rid: str):
    _store()[rid] = {"ts": datetime.now().strftime("%d/%m/%Y %H:%M")}
    _flush()

def remove_review(rid: str):
    _store().pop(rid, None)
    _flush()

def _flush():
    try:
        REVIEWS_FILE.write_text(
            json.dumps(_store(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
#  COMPROMISOS DEL MES — compartidos entre todas las sesiones
# ─────────────────────────────────────────────────────────────────────────────
COMMITMENTS_FILE = Path(__file__).parent / "commitments.json"

@st.cache_resource
def _commitments_store():
    data = {}
    if COMMITMENTS_FILE.exists():
        try:
            data = json.loads(COMMITMENTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return data

def load_commitments():
    return _commitments_store()

def save_commitment(rid: str, text: str):
    _commitments_store()[rid] = {
        "text": text,
        "ts": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    _flush_commitments()

def remove_commitment(rid: str):
    _commitments_store().pop(rid, None)
    _flush_commitments()

def _flush_commitments():
    try:
        COMMITMENTS_FILE.write_text(
            json.dumps(_commitments_store(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
#  CSS — MOBILE-FIRST
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

/* ── Reset & base ─────────────────────────────────────── */
html, body, [class*="css"]  { font-family:'Lato',sans-serif; }
.main .block-container       { padding: 0.8rem 0.9rem 5rem; max-width: 700px; }

/* ── Fondo papiro antiguo — imagen real inyectada abajo ── */
.stApp {
    background-color: #D4B070;
}
#MainMenu, footer, header    { visibility: hidden; }

/* ── Sidebar colapsado en móvil ───────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1B3A6B,#0D2247);
    border-right: 3px solid #C9930A;
}
[data-testid="stSidebar"] * { color:#E8EDF5 !important; }
[data-testid="stSidebar"] .stButton>button {
    background:transparent !important; border:none !important;
    color:#E8EDF5 !important; text-align:left !important;
    padding:0.3rem 0.5rem !important; font-size:0.85rem !important;
    width:100% !important;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background:rgba(201,147,10,0.25) !important; border-radius:6px !important;
}

/* ── Botones grandes, aptos para dedo ─────────────────── */
.stButton > button {
    min-height: 48px !important;
    font-size: 0.95rem !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Sección activa ───────────────────────────────────── */
.section-card {
    background: rgba(255,252,242,0.92);
    border-radius:14px;
    box-shadow:0 3px 20px rgba(100,70,20,0.13);
    padding:1.4rem 1.2rem; margin-bottom:1rem;
    border-left:5px solid #1B3A6B;
    animation:fadeIn 0.35s ease;
    backdrop-filter: blur(2px);
}
.section-card.rojo   { border-left-color:#A62020; }
.section-card.dorado { border-left-color:#C9930A; }
@keyframes fadeIn    { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
@keyframes logoEntrance {
    0%   { opacity:0; transform:scale(0.2) rotate(-8deg); filter:blur(8px); }
    60%  { opacity:1; transform:scale(1.08) rotate(2deg); filter:blur(0); }
    80%  { transform:scale(0.97) rotate(-1deg); }
    100% { transform:scale(1) rotate(0deg); }
}
@keyframes glowPulse {
    0%,100% { box-shadow: 0 0 0px rgba(201,147,10,0); }
    50%     { box-shadow: 0 0 28px rgba(201,147,10,0.6); }
}
.logo-animate {
    animation: logoEntrance 1.1s cubic-bezier(.22,1,.36,1) forwards,
               glowPulse 2s ease-in-out 1.1s 2;
    border-radius: 16px;
}
.logo-static { border-radius: 16px; }

/* ── Número de sección ────────────────────────────────── */
.sec-num {
    display:inline-flex; align-items:center; justify-content:center;
    width:36px; height:36px; border-radius:50%;
    background:#1B3A6B; color:white;
    font-family:'Cinzel',serif; font-size:1rem; font-weight:700;
    margin-right:0.6rem; flex-shrink:0; vertical-align:middle;
}
.sec-num.rojo   { background:#A62020; }
.sec-num.dorado { background:#C9930A; }

.sec-title {
    font-family:'Cinzel',serif; font-size:1.1rem;
    font-weight:700; color:#1B3A6B; vertical-align:middle;
}
.sec-title.rojo   { color:#A62020; }
.sec-title.dorado { color:#8B6200; }

/* ── Cajas de oración ─────────────────────────────────── */
.prayer-box {
    background:linear-gradient(135deg,#EBF3FF,#F5F0FF);
    border-left:4px solid #2E5FA3; border-radius:0 10px 10px 0;
    padding:1rem 1.2rem; margin:0.8rem 0;
    font-style:italic; font-size:0.91rem; line-height:1.85; color:#1A1A2E;
}
.prayer-box.rojo   { background:linear-gradient(135deg,#FDECEA,#FFF5F5); border-left-color:#A62020; }
.prayer-box.dorado { background:linear-gradient(135deg,#FFF8E1,#FFFDE7); border-left-color:#C9930A; }

/* ── Magnificat ───────────────────────────────────────── */
.magnificat-box {
    background:linear-gradient(135deg,#1B3A6B,#0D2247);
    border:2px solid #C9930A; border-radius:12px;
    padding:1.5rem 1.2rem; color:white !important;
    text-align:center; font-style:italic; line-height:2.1;
}
.magnificat-box .gloria {
    color:#C9930A; font-weight:700; font-style:normal;
    font-family:'Cinzel',serif; font-size:0.95rem;
}

/* ── Puntos de esfuerzo ───────────────────────────────── */
.effort-row {
    display:flex; gap:0.8rem; align-items:flex-start;
    padding:0.7rem 0.8rem; border-radius:10px; margin-bottom:0.5rem;
    background:#F8FAFE; border:1px solid #E0E9F7;
}
.effort-badge {
    background:#1B3A6B; color:white; border-radius:50%;
    width:30px; height:30px; min-width:30px;
    display:flex; align-items:center; justify-content:center;
    font-size:0.75rem; font-weight:700;
}
.effort-title { font-weight:700; font-size:0.88rem; color:#1B3A6B; }
.effort-desc  { font-size:0.81rem; color:#444; line-height:1.5; font-style:italic; }

/* ── Mapa de reunión ──────────────────────────────────── */
.map-header {
    background:linear-gradient(135deg,#1B3A6B,#2E5FA3);
    border-radius:16px; padding:1.2rem 1.3rem;
    margin-bottom:1.2rem;
    box-shadow:0 4px 20px rgba(27,58,107,0.22);
}

/* Grid responsivo para tarjetas del mapa */
.map-grid {
    display:grid;
    grid-template-columns: repeat(2, 1fr);
    gap:0.7rem;
    margin-bottom:1rem;
}
@media(min-width:600px) {
    .map-grid { grid-template-columns: repeat(3, 1fr); }
}

.map-card {
    background: rgba(255,252,242,0.90);
    border-radius:12px;
    padding:0.9rem 0.7rem 0.7rem;
    text-align:center;
    box-shadow:0 2px 12px rgba(100,70,20,0.12);
    border-top:4px solid #1B3A6B;
    position:relative;
    cursor:pointer;
}
.map-card.rojo   { border-top-color:#A62020; }
.map-card.dorado { border-top-color:#C9930A; }
.map-card .mc-icon  { font-size:1.6rem; line-height:1; }
.map-card .mc-num   { font-family:'Cinzel',serif; font-size:0.65rem; color:#999; letter-spacing:1px; margin-top:3px; }
.map-card .mc-title { font-size:0.77rem; font-weight:700; color:#1B3A6B; margin:5px 0 3px; line-height:1.25; }
.map-card .mc-badge { position:absolute; top:6px; right:7px; font-size:0.8rem; }

/* ── Tarjetas de revisión por pareja ──────────────────── */
.review-card {
    border-radius:14px; padding:1rem 1.1rem;
    margin-bottom:0.7rem;
    display:flex; align-items:center; gap:0.9rem;
    box-shadow:0 2px 10px rgba(100,70,20,0.10);
    transition: transform 0.15s;
}
.review-card:active { transform:scale(0.98); }
.review-card .rv-name  { font-weight:700; font-size:1rem; flex:1; }
.review-card .rv-time  { font-size:0.75rem; opacity:0.75; }
.review-card .rv-icon  { font-size:1.6rem; }

/* ── Barra de progreso ────────────────────────────────── */
.prog-bg   { background:rgba(255,255,255,0.18); border-radius:10px; height:8px; margin:0.4rem 0 0.3rem; }
.prog-fill { background:linear-gradient(90deg,#C9930A,#FFD54F); border-radius:10px; height:8px; }

/* ── Banner de revisión ───────────────────────────────── */
.review-banner {
    background:linear-gradient(135deg,#1B3A6B,#2E5FA3);
    border-radius:14px; padding:1rem 1.2rem;
    margin-bottom:1rem;
    border:2px solid #C9930A;
}
.review-badge-grid {
    display:grid;
    grid-template-columns: repeat(2, 1fr);
    gap:0.5rem;
    margin-top:0.6rem;
}
.rv-badge {
    border-radius:10px; padding:0.45rem 0.7rem;
    display:flex; align-items:center; gap:0.5rem;
    font-size:0.8rem; font-weight:700;
}
.rv-badge.done    { background:#E8F5E9; color:#2E7D32; }
.rv-badge.pending { background:rgba(255,255,255,0.1); color:rgba(255,255,255,0.5); border:1px solid rgba(255,255,255,0.2); }

/* ── Separador de sección ────────────────────────────── */
.sec-sep { height:1px; background:linear-gradient(90deg,transparent,#C9930A,transparent); margin:1.2rem 0; }

/* ── textarea móvil ──────────────────────────────────── */
.stTextArea textarea { font-size:0.95rem !important; line-height:1.6 !important; }
</style>
""", unsafe_allow_html=True)

# Inyectar textura de papiro como fondo real (base64 cargado en runtime)
if PAPIRO_B64:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{PAPIRO_B64}") !important;
        background-repeat: repeat !important;
        background-size: 600px 600px !important;
        background-attachment: fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECCIONES
# ─────────────────────────────────────────────────────────────────────────────
SECTIONS = [
    {"id":0,"num":1,"title":"Oración de Bienvenida","icon":"🙏","color":"azul","tipo":"oracion","dur":4,
     "texto":"""**Señor, te damos gracias**

por el don del sacramento del matrimonio y por la inmensa riqueza de caminar acompañados por nuestros hermanos de equipo. Te pedimos que tu Espíritu Santo ilumine cada uno de nuestros intercambios, nos dé la gracia de escucharnos desde el corazón y nos impulse a progresar juntos en el amor a Ti y al prójimo. Bendice a los dueños de esta casa por su hospitalidad, y concédenos que todo lo que hoy compartamos fortalezca nuestra espiritualidad conyugal, acercándonos con paso firme hacia la santidad a la que nos llamas en nuestra vida cotidiana.

**✝ Amén.**"""},

    {"id":1,"num":2,"title":"Oración al Espíritu Santo","icon":"🕊","color":"rojo","tipo":"oracion","dur":3,
     "texto":"""Espíritu Santo, Amor del Padre y del Hijo, Tú que has sido enviado para iluminar nuestro camino hacia la verdad plena; Tú que llenas de sabiduría y fortaleza nuestra mente para hacer la voluntad del Padre eterno; Tú que eres aliento de vida que renueva todas las cosas:

Humildemente te pedimos que vengas en nuestra ayuda y habites nuestro ser, y cada hogar y equipo de nuestro movimiento, de modo que seamos dóciles al servicio, generosos en la entrega de nuestra vida y dispuestos a dar testimonio del Sacramento del matrimonio, para llevar a nuestras familias hacia Dios.

Espíritu Santo, inspíranos siempre las palabras y obras necesarias para vivir adecuadamente la espiritualidad conyugal y la ayuda mutua en compañía de nuestros consiliarios y hogares, y así poder ser constantemente un signo vivo de tu amor. **✝ Amén**"""},

    {"id":2,"num":3,"title":"Compartir","icon":"🍞","color":"dorado","tipo":"oracion","dur":15,
     "subtitulo":"Bendición del Alimento",
     "texto":""""Cuando comemos del pan que partimos, nos hacemos uno con Cristo en su cuerpo."  *(1 Co 10,16)*

Señor Jesucristo, al comer hoy nuestro pan, ayúdanos a vivir en comunión fraternal y que tu amor reine entre nosotros. **✝ Amén**"""},

    {"id":3,"num":4,"title":"Puesta en Común","icon":"💬","color":"azul","tipo":"mixto","dur":20,
     "texto":"""Queridos amigos del equipo:

**¿De qué se trata?** Es el momento para hablar sobre los acontecimientos más importantes que hemos vivido desde la última vez que nos vimos. Aquí ponemos en común nuestra vida real, enmarcada en la pareja pero sin dejar de lado las preocupaciones familiares o profesionales, nuestros éxitos y fracasos, los descubrimientos, las tristezas y las alegrías.

**¿Por qué lo hacemos?** Porque la voluntad de abrirse a los demás, de hablar y de escucharnos con atención fortalece nuestra amistad. Como nos enseña el movimiento: *"no podemos amar a quien no conocemos"*. Este espacio humano nos prepara para la "Participación", donde más adelante compartiremos nuestros esfuerzos puramente espirituales.

**Nuestra regla de oro:** Para que este momento funcione, necesitamos una gran confianza recíproca y la certeza de la discreción y del **secreto absoluto**. Lo que revelamos en el equipo, no debe salir de él.

*"Ante todo, tened entre vosotros intenso amor."* (1 Pe 4,8)""",
     "campos":[
         {"key":"compromisos_ant","label":"📋 Compromisos del mes anterior","ph":"¿Cómo nos fue con los compromisos?"},
         {"key":"experiencias","label":"✨ Experiencias significativas del mes","ph":"Momentos de gracia, dificultad o crecimiento..."},
     ]},

    {"id":4,"num":5,"title":"Escucha de la Palabra","icon":"📖","color":"azul","tipo":"mixto","dur":15,
     "instruccion":"Escucha activa del pasaje elegido para esta reunión.",
     "texto":"""**Génesis 2, 18-23**

El Señor Dios se dijo: *No es bueno que el hombre esté solo; voy a hacerle a alguien como él, que le ayude.* Entonces el Señor Dios formó de la tierra todas las bestias del campo y todos los pájaros del cielo, y se los presentó al hombre, para ver qué nombre les ponía. Y cada ser vivo llevaría el nombre que el hombre le pusiera. Así el hombre puso nombre a todos los ganados, a los pájaros del cielo y a las bestias del campo; pero no encontró ninguno como él, que le ayudase.

Entonces el Señor Dios hizo caer un letargo sobre el hombre, que se durmió; le sacó una costilla, y le cerró el sitio con carne. Y el Señor Dios formó, de la costilla que había sacado del hombre, una mujer, y se la presentó al hombre. El hombre dijo: *¡Esta sí que es hueso de mis huesos y carne de mi carne!* Su nombre será «mujer», porque ha salido del varón. Por eso abandonará el varón a su padre y a su madre, se unirá a su mujer y serán los dos una sola carne.""",
     "campos":[
         {"key":"reflexion","label":"💭 Reflexión y puntos clave","ph":"Ideas que surgieron en la reflexión compartida..."},
     ]},

    {"id":5,"num":6,"title":"Oración Litúrgica","icon":"📜","color":"azul","tipo":"oracion","dur":8,
     "texto":"""**Salmo 95**

*Contad las maravillas del Señor a todas las naciones.*

Cantad al Señor un cántico nuevo, cantad al Señor, toda la tierra; cantad al Señor, bendecid su nombre.

*Contad las maravillas del Señor a todas las naciones.*

Proclamad día tras día su victoria. Contad a los pueblos su gloria, sus maravillas a todas las naciones.

*Contad las maravillas del Señor a todas las naciones.*

Familias de los pueblos, aclamad al Señor, aclamad la gloria y el poder del Señor; aclamad la gloria del nombre del Señor.

*Contad las maravillas del Señor a todas las naciones.*

Decid a los pueblos: «El Señor es rey: él afianzó el orbe, y no se moverá; él gobierna a los pueblos rectamente».

*Contad las maravillas del Señor a todas las naciones.*"""},

    {"id":6,"num":7,"title":"Oración Comunitaria","icon":"🙌","color":"rojo","tipo":"mixto","dur":10,
     "texto":"""Hacemos silencio y recordamos lo que el Señor ha hecho con cada uno, todo lo que nos ha dado, las veces en que me he sentido amado y sanado por Él, dejando que brote en mi interior un agradecimiento sincero y profundo.

*«Te doy gracias, Señor…»*""",
     "campos":[
         {"key":"intercesiones","label":"🙏 Intenciones y acciones de gracias","ph":"Lo que el equipo lleva al Señor hoy..."},
     ]},

    {"id":7,"num":8,"title":"Puntos de Esfuerzo","icon":"⭐","color":"dorado","tipo":"esfuerzos","dur":10,
     "esfuerzos":[
         ("Escucha de la Palabra","Leer asiduamente la Sagrada Escritura para arraigarse en el Evangelio. (Hch 4,12)","#1B3A6B"),
         ("Oración Personal","Encuentro diario y silencioso con Dios — tiempo reservado para estar a solas con Él. (Col 4,2)","#1B3A6B"),
         ("Oración Conyugal","Orar juntos, esposo y esposa, cada día. (Jn 17,23)","#A62020"),
         ("Diálogo Conyugal","Tiempo mensual de diálogo profundo bajo la mirada del Señor — «El Deber de Sentarse». (Ef 5,21)","#A62020"),
         ("La Regla de Vida","Imponerse esfuerzos personales concretos para adherirse más al proyecto divino.","#C9930A"),
         ("Retiro Espiritual","Hacer cada año un retiro: tiempo para detenerse, escuchar y renovarse. (Mc 6,31)","#C9930A"),
     ],
     "instruccion":"""Los Puntos Concretos de Esfuerzo (PCE) son los pilares fundamentales de la espiritualidad conyugal. Lejos de ser obligaciones impuestas, son actitudes interiores que deben despertarse desde la libertad y la adhesión del corazón. Su objetivo es provocar un cambio de vida que acerque a los esposos al Señor, el uno al otro y a las demás personas en su camino hacia la santidad.""",
     "campos":[
         {"key":"compromisos_esf","label":"✍️ Compromisos personales de esta reunión","ph":"Cada pareja anota su compromiso para el próximo mes..."},
     ]},

    {"id":8,"num":9,"title":"Tema de Estudio","icon":"📚","color":"azul","tipo":"mixto","dur":25,
     "instruccion":"Presentación y reflexión sobre el tema del mes.",
     "texto":f"""**{MEETING_TEMA}**

*{MEETING_QUOTE}*

**El descubrimiento de la incompletitud:** Caffarel explica que, antes de enamorarse, las personas suelen vivir como si se bastaran a sí mismas. Sin embargo, el amor les hace tomar conciencia de una "pobreza radical": descubren que son seres incompletos que necesitan a esa persona complementaria —la "otra mitad del mundo"— para alcanzar la plenitud. Dios utiliza esta experiencia para llevarnos a descubrir una incompletitud aún más profunda: nuestra dependencia absoluta frente a Él.

**La gratuidad del amor:** El amor es un milagro imprevisible y libre que no se puede comprar ni exigir. Esta vivencia de recibir el amor humano gratuitamente nos sirve de espejo para comprender el "reino de la gracia" divina: el amor y la salvación de Dios son dones de absoluta gratuidad que el ser humano está llamado a acoger con humildad.""",
     "campos":[
         {"key":"tema_sint","label":"💡 Síntesis y puntos clave","ph":"Ideas principales, citas, preguntas del grupo..."},
     ]},

    {"id":9,"num":10,"title":"Informaciones","icon":"📣","color":"dorado","tipo":"notas","dur":5,
     "instruccion":"Momento para informar sobre eventos del movimiento (retiros, encuentros de sector, actividades formativas), organizar la logística interna del equipo y compartir cualquier otra información práctica necesaria.",
     "campos":[
         {"key":"sector","label":"📍 Reunión del Sector","ph":"Lugar / Tema / Fecha"},
         {"key":"interequipos","label":"🤝 Interequipos","ph":"Lugar / Tema / Fecha"},
         {"key":"prox","label":"🏠 Próxima Reunión","ph":"Hogar anfitrión / Fecha"},
         {"key":"otros","label":"📢 Otros anuncios","ph":""},
     ]},

    {"id":10,"num":11,"title":"Oración Final","icon":"✝","color":"rojo","tipo":"notas","dur":5,
     "instruccion":"Oración final a cargo de Amparo y Fernando — libre o preparada por el hogar.",
     "campos":[
         {"key":"oracion_final","label":"🙏 Oración final","ph":"Escribe aquí o deja en blanco si es espontánea..."},
     ]},

    {"id":11,"num":12,"title":"Oración por la Canonización del P. Henri Caffarel","icon":"✝","color":"rojo","tipo":"oracion","dur":4,
     "texto":"""**Dios, Padre nuestro,**

pusiste en el corazón de tu siervo Henri Caffarel,
un impulso de amor que le unía sin reserva a tu Hijo
y le inspiraba para hablar de Él.

Profeta de nuestro tiempo,
enseñó la dignidad y la bondad de la vocación de cada uno
según la llamada que Jesús nos dirige a todos: *"Ven y sígueme".*
Él despertó el entusiasmo de los cónyuges
ante la grandeza del sacramento del matrimonio,
imagen del misterio de unidad y de amor fecundo entre Cristo y la Iglesia.
Enseñó que sacerdotes y matrimonios
están llamados a vivir la vocación del amor.
Guió a las viudas: *¡El amor es más fuerte que la muerte!*
Impulsado por el Espíritu
dirigió a muchos creyentes por el camino de la oración.
Poseído por un fuego devorador, estuvo lleno de Ti, Señor.

**Dios, Padre nuestro,**
por la intercesión de nuestra Señora
te pedimos que aceleres el día
en que la Iglesia proclame la santidad de su vida,
para que todos descubran la alegría de seguir a tu Hijo,
cada cual según la vocación del Espíritu.

*Dios Padre nuestro, invocamos al Padre Caffarel para…*
*(precisar la gracia a pedir)*"""},

    {"id":12,"num":13,"title":"Magnificat","icon":"🌟","color":"dorado","tipo":"magnificat","dur":5},
]

TOTAL = len(SECTIONS)

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init():
    defs = {
        "in_meeting":   False,
        "show_map":     True,
        "current":      0,
        "completed":    [False]*TOTAL,
        "notes":        {},
        "duties":       [False]*6,
        "start":        None,
        "sec_start":    time.time(),
        "seen_preview": set(),
        "preview_sec":  None,
        "audio_played": False,
        "first_visit":  True,      # True = primera carga de esta sesión (anima logo)
    }
    for k,v in defs.items():
        if k not in st.session_state: st.session_state[k]=v

init()

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def go(idx):
    st.session_state.current   = idx
    st.session_state.show_map  = False
    st.session_state.sec_start = time.time()

def done_count(): return sum(st.session_state.completed)
def pct():        return int(done_count()/TOTAL*100)

def cc(sec):  # color class
    return {"rojo":"rojo","dorado":"dorado"}.get(sec["color"],"")

def border(sec):
    return {"rojo":"#A62020","dorado":"#C9930A"}.get(sec["color"],"#1B3A6B")

# ─────────────────────────────────────────────────────────────────────────────
#  COMPONENTE: BANNER DE REVISIONES
# ─────────────────────────────────────────────────────────────────────────────
def review_banner():
    reviews = load_reviews()
    count   = len(reviews)
    total_r = len(REVIEWERS)
    badges  = ""
    for r in REVIEWERS:
        if r["id"] in reviews:
            ts = reviews[r["id"]]["ts"]
            badges += (
                f'<div class="rv-badge done">'
                f'  {r["icon"]} {r["id"]}'
                f'  <span style="font-weight:400;font-size:0.65rem;display:block;">{ts}</span>'
                f'</div>'
            )
        else:
            badges += f'<div class="rv-badge pending">{r["icon"]} {r["id"]}</div>'

    st.markdown(f"""
    <div class="review-banner">
        <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.6rem;">
            <span style="font-size:1.3rem;">📋</span>
            <div>
                <div style="font-family:'Cinzel',serif;font-size:0.85rem;color:#C9930A;font-weight:700;">
                    REVISIÓN PREVIA AL ENCUENTRO
                </div>
                <div style="font-size:0.78rem;color:#B0C4DE;">
                    {count} de {total_r} han revisado el material
                </div>
            </div>
        </div>
        <div class="review-badge-grid">{badges}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PANTALLA: REVISIÓN PREVIA
# ─────────────────────────────────────────────────────────────────────────────
def render_downloads():
    """Botones de descarga de la guía y el capítulo de estudio."""
    ASSETS = Path(__file__).parent / "assets"
    docx_path = ASSETS / "reunion.docx"
    cap_path  = ASSETS / "capitulo3.pdf"

    has_docx = docx_path.exists()
    has_cap  = cap_path.exists()

    if not has_docx and not has_cap:
        return

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1B3A6B,#2E5FA3);
                border-radius:14px;padding:1rem 1.2rem;margin-bottom:0.8rem;">
        <div style="font-family:'Cinzel',serif;font-size:0.8rem;color:#C9930A;
                    letter-spacing:1px;margin-bottom:0.7rem;">
            📎 DOCUMENTOS DE LA REUNIÓN
        </div>
        <div style="font-size:0.8rem;color:#B0C4DE;margin-bottom:0.8rem;">
            Descarga la guía y el tema de estudio para tenerlos en tu dispositivo.
        </div>
    </div>
    """, unsafe_allow_html=True)

    n = sum([has_docx, has_cap])
    cols = st.columns(n)
    ci = 0

    if has_docx:
        with cols[ci]:
            st.download_button(
                label="📄 Guía de Reunión (.docx)",
                data=docx_path.read_bytes(),
                file_name="Guia_Reunion_Equipo5_ENS.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        ci += 1
    if has_cap:
        with cols[ci]:
            st.download_button(
                label="📕 Cap. 3 · Incompletitud y Gratuidad",
                data=cap_path.read_bytes(),
                file_name="Capitulo3_Incompletitud_Gratuidad.pdf",
                mime="application/pdf",
                use_container_width=True,
            )


def _sec_content_html(sec):
    """Devuelve el contenido HTML de una sección para la vista de revisión."""
    import re as _re
    tipo = sec.get("tipo","")
    cls  = {"rojo":"rojo","dorado":"dorado"}.get(sec["color"],"")
    out  = ""

    if tipo in ("oracion","mixto") and "texto" in sec:
        h = sec["texto"].replace("\n\n","<br><br>").replace("\n","<br>")
        h = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
        h = _re.sub(r"\*(.+?)\*",     r"<em>\1</em>", h)
        out += f'<div class="prayer-box {cls}">{h}</div>'

    elif tipo == "esfuerzos":
        for i,(t,d,col) in enumerate(sec["esfuerzos"]):
            out += f'''<div class="effort-row">
                <div class="effort-badge" style="background:{col};">{i+1}</div>
                <div><div class="effort-title">{t}</div>
                     <div class="effort-desc">{d}</div></div>
            </div>'''

    elif tipo == "magnificat":
        out += '''<div class="prayer-box" style="text-align:center;">
            <em>Proclama mi alma la grandeza del Señor,<br>
            se alegra mi espíritu en Dios, mi salvador…</em><br>
            <span style="font-size:0.8rem;color:#888;">(Lc 1, 46-55)</span>
        </div>'''

    if "instruccion" in sec:
        out += f'<div style="font-size:0.88rem;color:#555;font-style:italic;padding:0.5rem 0;">{sec["instruccion"]}</div>'

    if sec.get("campos"):
        for campo in sec["campos"]:
            out += f'<div style="font-size:0.82rem;color:#1B3A6B;font-weight:600;margin-top:8px;">• {campo["label"]}</div>'

    return out or '<div style="color:#999;font-size:0.85rem;font-style:italic;">Ver en la reunión.</div>'


def render_commitments():
    """Tablero de compromisos del mes — cada pareja escribe el suyo, visible para todos."""
    commitments = load_commitments()
    color_map   = {"azul":"#1B3A6B","rojo":"#A62020","dorado":"#C9930A"}

    st.markdown("""
    <div style="font-family:'Cinzel',serif;font-size:0.78rem;color:#8B6200;
                letter-spacing:2px;margin-bottom:0.8rem;text-align:center;">
        ✍️ COMPROMISOS DEL MES
    </div>
    """, unsafe_allow_html=True)

    # Tablero — compromisos ya guardados
    any_saved = any(r["id"] in commitments for r in REVIEWERS)
    if any_saved:
        for r in REVIEWERS:
            rid = r["id"]
            if rid in commitments:
                c = commitments[rid]
                st.markdown(f"""
                <div style="background:rgba(255,252,242,0.95);border-radius:12px;
                            padding:0.8rem 1rem;margin-bottom:0.5rem;
                            border-left:4px solid {r['fg']};
                            box-shadow:0 2px 8px rgba(100,70,20,0.10);">
                    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                        <span style="font-size:1.1rem;">{r['icon']}</span>
                        <span style="font-weight:700;color:{r['fg']};font-size:0.88rem;">{r['label']}</span>
                        <span style="margin-left:auto;font-size:0.65rem;color:#aaa;">{c['ts']}</span>
                    </div>
                    <div style="font-size:0.85rem;color:#333;line-height:1.55;
                                font-style:italic;">"{c['text']}"</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

    # Formulario para escribir / actualizar compromiso
    with st.expander("✍️ Escribe o actualiza tu compromiso"):
        rid_sel = st.selectbox(
            "¿Quién escribe?",
            options=[r["id"] for r in REVIEWERS],
            format_func=lambda x: next(r["label"] for r in REVIEWERS if r["id"] == x),
            key="commit_who",
        )
        existing = commitments.get(rid_sel, {}).get("text", "")
        txt = st.text_area(
            "Mi compromiso para este mes:",
            value=existing,
            placeholder="Ej: Dedicar 10 minutos diarios a la oración conyugal...",
            height=90,
            key="commit_txt",
        )
        c1, c2 = st.columns([3, 1])
        with c1:
            if st.button("💾 Guardar compromiso", use_container_width=True, type="primary",
                         key="commit_save"):
                if txt.strip():
                    save_commitment(rid_sel, txt.strip())
                    st.rerun()
        with c2:
            if rid_sel in commitments:
                if st.button("🗑️", use_container_width=True, key="commit_del",
                             help="Eliminar mi compromiso"):
                    remove_commitment(rid_sel)
                    st.rerun()


def render_whatsapp():
    """Botón para compartir el enlace de la app por WhatsApp."""
    import urllib.parse
    mensaje = (
        f"✝ *Equipo #5 ENS — Sector Fusagasugá*\n\n"
        f"📅 Reunión: *{MEETING_DATE}*\n"
        f"🏠 Anfitriones: {MEETING_HOST}\n"
        f"📚 Tema: _{MEETING_TEMA}_\n\n"
        f"Ingresa aquí para revisar el material antes de la reunión:\n"
        f"👉 {APP_URL}"
    )
    url = f"https://wa.me/?text={urllib.parse.quote(mensaje)}"
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="background:linear-gradient(135deg,#25D366,#128C7E);
                    border-radius:14px;padding:0.85rem 1.2rem;
                    display:flex;align-items:center;gap:0.8rem;
                    box-shadow:0 3px 12px rgba(18,140,126,0.35);
                    margin-bottom:0.8rem;cursor:pointer;">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"
                 fill="white">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15
                         -.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463
                         -2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606
                         .134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025
                         -.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008
                         -.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479
                         0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306
                         1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719
                         2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                <path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.558 4.122 1.532 5.855L.057 23.869
                         a.75.75 0 00.918.943l6.186-1.62A11.945 11.945 0 0012 24c6.627 0 12-5.373
                         12-12S18.627 0 12 0zm0 21.75a9.724 9.724 0 01-4.952-1.355l-.355-.211
                         -3.674.963.981-3.584-.231-.369A9.722 9.722 0 012.25 12C2.25 6.615 6.615
                         2.25 12 2.25S21.75 6.615 21.75 12 17.385 21.75 12 21.75z"/>
            </svg>
            <div>
                <div style="color:white;font-weight:700;font-size:0.95rem;">
                    Compartir por WhatsApp
                </div>
                <div style="color:rgba(255,255,255,0.8);font-size:0.75rem;margin-top:1px;">
                    Envía el enlace al grupo del equipo
                </div>
            </div>
            <span style="margin-left:auto;color:white;font-size:1.2rem;">→</span>
        </div>
    </a>
    """, unsafe_allow_html=True)


def render_audio():
    """Reproduce la canción una sola vez al entrar. Autoplay donde el navegador lo permite;
    si lo bloquea (iOS / Chrome móvil) queda el reproductor visible para que el usuario lo active."""
    if not AUDIO_PATH.exists():
        return

    audio_b64 = base64.b64encode(AUDIO_PATH.read_bytes()).decode()

    if not st.session_state.audio_played:
        # Primer render: intentar autoplay
        st.session_state.audio_played = True
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1B3A6B,#2E5FA3);
                    border-radius:14px;padding:0.8rem 1.1rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:0.8rem;">
            <span style="font-size:1.4rem;">🎵</span>
            <div style="flex:1;">
                <div style="font-family:'Cinzel',serif;font-size:0.72rem;
                            color:#C9930A;letter-spacing:1px;">CANCIÓN DE LA REUNIÓN</div>
                <div style="font-size:0.8rem;color:#B0C4DE;margin-top:2px;">
                    Incompletitud y Gratuidad
                </div>
            </div>
            <audio id="ens_audio" controls style="height:36px;border-radius:8px;max-width:170px;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mpeg">
            </audio>
        </div>
        <script>
            (function() {{
                var a = document.getElementById('ens_audio');
                if (a) {{ a.play().catch(function(){{}}); }}
            }})();
        </script>
        """, unsafe_allow_html=True)
    else:
        # Siguientes renders: solo el reproductor, sin autoplay
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1B3A6B,#2E5FA3);
                    border-radius:14px;padding:0.8rem 1.1rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:0.8rem;">
            <span style="font-size:1.4rem;">🎵</span>
            <div style="flex:1;">
                <div style="font-family:'Cinzel',serif;font-size:0.72rem;
                            color:#C9930A;letter-spacing:1px;">CANCIÓN DE LA REUNIÓN</div>
                <div style="font-size:0.8rem;color:#B0C4DE;margin-top:2px;">
                    Incompletitud y Gratuidad
                </div>
            </div>
            <audio controls style="height:36px;border-radius:8px;max-width:170px;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mpeg">
            </audio>
        </div>
        """, unsafe_allow_html=True)


def render_preview():
    seen = st.session_state.seen_preview
    open_sec = st.session_state.preview_sec   # None = grid  |  int = tarjeta abierta
    color_map = {"azul":"#1B3A6B","rojo":"#A62020","dorado":"#C9930A"}

    # ════════════════════════════════════════════════════════════════════════
    #  VISTA DETALLE — tarjeta individual abierta
    # ════════════════════════════════════════════════════════════════════════
    if open_sec is not None:
        sec  = SECTIONS[open_sec]
        bc   = color_map[sec["color"]]
        cls  = {"rojo":"rojo","dorado":"dorado"}.get(sec["color"],"")

        # Marcar como visto (aquí sí es fiable porque el usuario hizo click)
        if open_sec not in seen:
            seen.add(open_sec)
            st.session_state.seen_preview = seen

        # Botón volver
        if st.button("← Volver al temario", key="back_grid", use_container_width=True):
            st.session_state.preview_sec = None
            st.rerun()

        # Tarjeta detalle
        st.markdown(f"""
        <div class="section-card {cls}" style="border-left-color:{bc};margin-top:0.6rem;">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
                <span class="sec-num {cls}">{sec['num']}</span>
                <span class="sec-title {cls}">{sec['icon']} {sec['title']}</span>
            </div>
            {_sec_content_html(sec)}
        </div>
        """, unsafe_allow_html=True)

        # Descarga del capítulo en la sección Tema de Estudio (preview)
        if sec["id"] == 8:
            cap_path = Path(__file__).parent / "assets" / "capitulo3.pdf"
            if cap_path.exists():
                st.download_button(
                    label="📕 Descargar Cap. 3 · Incompletitud y Gratuidad",
                    data=cap_path.read_bytes(),
                    file_name="Capitulo3_Incompletitud_Gratuidad.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        # Navegación entre tarjetas
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if open_sec > 0:
                if st.button("◀ Ant.", key="prev_card", use_container_width=True):
                    st.session_state.preview_sec = open_sec - 1
                    st.rerun()
        with c2:
            remaining = [s["id"] for s in SECTIONS if s["id"] not in seen]
            next_unseen = next((i for i in range(open_sec+1, TOTAL) if i not in seen), None)
            if next_unseen is not None:
                if st.button(f"Siguiente →", key="next_card",
                             use_container_width=True, type="primary"):
                    st.session_state.preview_sec = next_unseen
                    st.rerun()
            else:
                st.markdown('<div style="text-align:center;color:#2E7D32;font-size:0.82rem;'
                            'font-weight:700;padding:0.5rem;">✅ Todo revisado</div>',
                            unsafe_allow_html=True)
        with c3:
            if open_sec < TOTAL - 1:
                if st.button("Sig. ▶", key="next_card2", use_container_width=True):
                    st.session_state.preview_sec = open_sec + 1
                    st.rerun()
        return   # no renderizar el grid mientras hay tarjeta abierta

    # ════════════════════════════════════════════════════════════════════════
    #  VISTA GRID — cabecera + tarjetas
    # ════════════════════════════════════════════════════════════════════════

    # ── HERO — fondo degradado ───────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(170deg,#0D2247 0%,#1B3A6B 55%,#2E5FA3 100%);
                border-radius:20px 20px 0 0;
                padding:1.8rem 1rem 0.5rem;
                text-align:center;
                box-shadow:0 8px 32px rgba(13,34,71,0.35);">
        <div style="font-size:0.72rem;color:#C9930A;font-weight:700;
                    letter-spacing:3px;margin-bottom:0.8rem;">
            ✦ &nbsp; EQUIPOS DE NUESTRA SEÑORA &nbsp; ✦
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Logo — con animación en primera visita
    if LOGO_PATH.exists():
        logo_cls = "logo-animate" if st.session_state.first_visit else "logo-static"
        if st.session_state.first_visit:
            st.session_state.first_visit = False
        col_l, col_c, col_r = st.columns([1, 6, 1])
        with col_c:
            st.markdown(f'<div class="{logo_cls}">', unsafe_allow_html=True)
            st.image(str(LOGO_PATH), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Texto de identidad sobre el mismo fondo
    st.markdown(f"""
    <div style="background:linear-gradient(170deg,#1B3A6B 0%,#2E5FA3 100%);
                border-radius:0 0 20px 20px;
                padding:0.6rem 1rem 1.6rem;
                text-align:center;
                box-shadow:0 8px 32px rgba(13,34,71,0.35);
                margin-bottom:0.5rem;">
        <div style="font-family:'Cinzel',serif;
                    font-size:2rem;font-weight:700;
                    color:#C9930A;letter-spacing:3px;line-height:1.1;">
            EQUIPO&nbsp;#5
        </div>
        <div style="font-size:0.95rem;color:#FFD54F;
                    font-weight:600;letter-spacing:4px;margin-top:6px;">
            SECTOR FUSAGASUGÁ
        </div>
        <div style="width:70px;height:2px;
                    background:linear-gradient(90deg,transparent,#C9930A,transparent);
                    margin:0.9rem auto 0.8rem;"></div>
        <div style="font-size:0.82rem;color:#B0C4DE;line-height:1.8;">
            Equipos de Nuestra Señora<br>
            <span style="color:#9FC3E8;">✝ &nbsp;P. Faider Julián Santiago Díaz</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tarjeta de datos de la reunión
    st.markdown(f"""
    <div style="background:white;border-radius:14px;padding:1rem 1.2rem;
                margin-bottom:1.2rem;box-shadow:0 3px 16px rgba(27,58,107,0.10);
                border-left:5px solid #C9930A;">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.7rem;">
            <span style="font-size:1.3rem;">📅</span>
            <div>
                <div style="font-family:'Cinzel',serif;font-size:0.72rem;
                            color:#888;letter-spacing:1px;">REUNIÓN</div>
                <div style="font-weight:700;color:#1B3A6B;font-size:0.95rem;">
                    {MEETING_DATE}
                </div>
            </div>
            <div style="margin-left:auto;text-align:right;">
                <div style="font-family:'Cinzel',serif;font-size:0.72rem;
                            color:#888;letter-spacing:1px;">ANFITRIONES</div>
                <div style="font-weight:700;color:#2E7D32;font-size:0.82rem;">
                    🏠 {MEETING_HOST}
                </div>
            </div>
        </div>
        <div style="border-top:1px solid #EEE;padding-top:0.7rem;
                    font-style:italic;font-size:0.82rem;color:#555;line-height:1.6;">
            📚 <strong>Tema:</strong> {MEETING_TEMA}
        </div>
        <div style="border-top:1px solid #EEE;padding-top:0.7rem;margin-top:0.6rem;
                    font-style:italic;font-size:0.78rem;color:#777;line-height:1.55;">
            {MEETING_QUOTE}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Canción ──────────────────────────────────────────────────────────────
    render_audio()

    # ── Descarga del documento ───────────────────────────────────────────────
    render_downloads()

    # ── Banner estado revisiones ─────────────────────────────────────────────
    review_banner()
    st.markdown("""<div class="sec-sep"></div>""", unsafe_allow_html=True)

    # ── Barra de progreso del temario ────────────────────────────────────────
    total_s  = len(SECTIONS)
    seen_n   = len(seen)
    all_seen = seen_n >= total_s
    pct_seen = int(seen_n / total_s * 100)

    progress_msg = ("✅ ¡Has leído todo el material!" if all_seen
                    else f"Toca cada tarjeta para leer · {seen_n}/{total_s}")
    progress_color = "#2E7D32" if all_seen else "#888"
    bar_grad = ("linear-gradient(90deg,#2E7D32,#66BB6A)" if all_seen
                else "linear-gradient(90deg,#1B3A6B,#2E5FA3)")

    st.markdown(f"""
    <div style="background:rgba(255,252,242,0.92);border-radius:12px;padding:0.8rem 1rem;
                margin-bottom:1rem;box-shadow:0 2px 8px rgba(100,70,20,0.10);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
            <span style="font-family:'Cinzel',serif;font-size:0.75rem;color:#888;letter-spacing:1px;">
                TEMARIO · LEE CADA SECCIÓN
            </span>
            <span style="font-size:0.8rem;font-weight:700;
                         color:{'#2E7D32' if all_seen else '#1B3A6B'};">{seen_n}/{total_s}</span>
        </div>
        <div style="background:#EEE;border-radius:6px;height:7px;">
            <div style="background:{bar_grad};width:{pct_seen}%;
                        height:7px;border-radius:6px;transition:width 0.4s;"></div>
        </div>
        <div style="text-align:center;font-size:0.75rem;color:{progress_color};
                    margin-top:5px;font-weight:{'700' if all_seen else '400'};">{progress_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Grid de tarjetas ─────────────────────────────────────────────────────
    rows = [SECTIONS[i:i+2] for i in range(0, total_s, 2)]
    for row in rows:
        cols = st.columns(len(row))
        for col, sec in zip(cols, row):
            with col:
                sid   = sec["id"]
                visto = sid in seen
                bc    = color_map[sec["color"]]
                badge = "✅" if visto else ""
                title_c = "#2E7D32" if visto else bc

                st.markdown(f"""
                <div class="map-card {'rojo' if sec['color']=='rojo' else 'dorado' if sec['color']=='dorado' else ''}"
                     style="border-top-color:{bc};margin-bottom:0.2rem;">
                    <div class="mc-badge">{badge}</div>
                    <div class="mc-icon">{sec['icon']}</div>
                    <div class="mc-num">PASO {sec['num']}</div>
                    <div class="mc-title" style="color:{title_c};">{sec['title']}</div>
                </div>
                """, unsafe_allow_html=True)

                btn_lbl  = "✅ Leído" if visto else "👁 Leer"
                btn_tipo = "secondary" if visto else "primary"
                if st.button(btn_lbl, key=f"open_{sid}",
                             use_container_width=True, type=btn_tipo):
                    st.session_state.preview_sec = sid
                    # marcar visto de inmediato
                    seen.add(sid)
                    st.session_state.seen_preview = seen
                    st.rerun()
        st.markdown("<div style='margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)

    # ── Confirmar revisión ───────────────────────────────────────────────────
    st.markdown("""<div class="sec-sep"></div>""", unsafe_allow_html=True)
    reviews = load_reviews()

    if not all_seen:
        faltan = total_s - seen_n
        st.markdown(f"""
        <div style="background:#FFF8E1;border:2px solid #C9930A;border-radius:14px;
                    padding:1rem;text-align:center;margin-bottom:0.5rem;">
            <div style="font-size:1.5rem;">🔒</div>
            <div style="font-size:0.88rem;color:#8B6200;font-weight:700;margin-top:4px;">
                Faltan {faltan} tarjeta{'s' if faltan>1 else ''} por leer
            </div>
            <div style="font-size:0.75rem;color:#AAA;margin-top:4px;">
                Lee todas las secciones para confirmar tu revisión
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-family:'Cinzel',serif;font-size:0.78rem;color:#888;
                    letter-spacing:2px;margin-bottom:0.8rem;text-align:center;">
            ¿QUIÉN YA REVISÓ? — CONFIRMA AQUÍ
        </div>
        """, unsafe_allow_html=True)

        for r in REVIEWERS:
            rid   = r["id"]
            ya    = rid in reviews
            ts    = reviews[rid]["ts"] if ya else ""
            border_c    = r["fg"] if ya else "#DDD"
            icon_html   = "✅" if ya else r["icon"]
            ts_html     = f'<span style="font-size:0.68rem;font-weight:400;opacity:0.75;display:block;">{ts}</span>' if ya else ""
            if r["tipo"] == "consiliario":
                badge_html = '<div style="font-size:0.7rem;color:#6A1B9A;font-style:italic;font-weight:600;">Consiliario</div>'
            elif r["tipo"] == "sector":
                badge_html = '<div style="font-size:0.7rem;color:#B35C00;font-weight:700;background:#FFF3E0;border-radius:6px;padding:1px 6px;display:inline-block;">⭐ Resp. de Sector</div>'
            else:
                badge_html = ""
            cons_html = badge_html

            st.markdown(
                f'<div class="review-card" style="background:{r["bg"]};border:2px solid {border_c};">'
                f'  <div class="rv-icon">{icon_html}</div>'
                f'  <div style="flex:1;">'
                f'    <div class="rv-name" style="color:{r["fg"]};">{r["label"]}{ts_html}</div>'
                f'    {cons_html}'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if ya:
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.button("✅ Confirmado", key=f"mk_{rid}",
                              use_container_width=True, disabled=True)
                with c2:
                    if st.button("↩", key=f"um_{rid}",
                                 use_container_width=True, help="Desmarcar"):
                        remove_review(rid); st.rerun()
            else:
                if r["tipo"] == "consiliario":
                    lbl = f"✝  Ya revisé — {r['label']}"
                elif r["tipo"] == "sector":
                    lbl = f"🌟  Ya revisamos — {r['label']}"
                else:
                    lbl = f"👫  Ya revisamos — {r['id']}"
                if st.button(lbl, key=f"mk_{rid}",
                             use_container_width=True, type="primary"):
                    save_review(rid); st.rerun()

    # ── Compromisos del mes ──────────────────────────────────────────────────
    st.markdown("""<div class="sec-sep"></div>""", unsafe_allow_html=True)
    render_commitments()

    # ── WhatsApp + acceso a guía ─────────────────────────────────────────────
    st.markdown("""<div class="sec-sep"></div>""", unsafe_allow_html=True)
    render_whatsapp()

    if st.button("🚀 Abrir guía completa de reunión",
                 use_container_width=True, type="primary"):
        st.session_state.in_meeting = True
        st.session_state.show_map   = True
        if not st.session_state.start:
            st.session_state.start = time.time()
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR (solo cuando hay reunión activa)
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        if LOGO_B64:
            st.markdown(f'<div style="text-align:center;padding:0.8rem 0 0.3rem;">'
                        f'<img src="data:image/png;base64,{LOGO_B64}" '
                        f'style="width:140px;border-radius:10px;"></div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-family:Cinzel,serif;'
                    'font-size:0.8rem;color:#C9930A;letter-spacing:1px;padding-bottom:0.5rem;">'
                    'EQUIPO #5 · FUSAGASUGÁ</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:0.75rem;color:#8899BB;margin-bottom:0.3rem;">'
                    f'📅 {MEETING_DATE}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.75rem;color:#8899BB;margin-bottom:0.3rem;">'
                    f'🏠 {MEETING_HOST}</div>', unsafe_allow_html=True)

        p = pct()
        st.markdown(f"""
        <div style="margin:0.7rem 0 0.2rem;font-size:0.75rem;color:#C9930A;font-weight:700;">
            Progreso {done_count()}/{TOTAL}
        </div>
        <div class="prog-bg"><div class="prog-fill" style="width:{p}%;"></div></div>
        """, unsafe_allow_html=True)

        # Mini review status en sidebar
        reviews = load_reviews()
        rv_line = "  ".join(["✅" if r["id"] in reviews else "⬜" for r in REVIEWERS])
        st.markdown(f'<div style="font-size:0.75rem;color:#8899BB;margin-bottom:0.5rem;">'
                    f'Revisiones: {rv_line}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div style="font-size:0.72rem;color:#C9930A;font-weight:700;'
                    'letter-spacing:1px;margin-bottom:0.4rem;">AGENDA</div>',
                    unsafe_allow_html=True)

        for sec in SECTIONS:
            idx = sec["id"]
            ico = "✅" if st.session_state.completed[idx] else ("🔵" if idx==st.session_state.current else "⬜")
            if st.button(f"{ico} {sec['num']}. {sec['title']}", key=f"sb_{idx}",
                         use_container_width=True):
                go(idx); st.rerun()

        st.markdown("---")
        if st.session_state.start:
            e = int(time.time()-st.session_state.start)
            hh,mm = divmod(e//60,60); ss=e%60
            st.markdown(f'<div style="text-align:center;font-size:0.78rem;'
                        f'color:#8899BB;">⏱ {hh:02d}:{mm:02d}:{ss:02d}</div>',
                        unsafe_allow_html=True)

        if st.button("🗺️ Mapa de reunión", use_container_width=True, key="sb_map"):
            st.session_state.show_map=True; st.rerun()
        if st.button("📋 Vista de revisión", use_container_width=True, key="sb_prev"):
            st.session_state.in_meeting=False; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  MAPA / DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def render_dashboard():
    reviews = load_reviews()
    host = MEETING_HOST
    date = MEETING_DATE
    num  = ""
    p    = pct()

    logo_html = (f'<img src="data:image/png;base64,{LOGO_B64}" '
                 f'style="width:90px;border-radius:10px;border:2px solid #C9930A;">') if LOGO_B64 else "✝"

    st.markdown(f"""
    <div class="map-header">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.8rem;">
            <div>{logo_html}</div>
            <div style="flex:1;">
                <div style="font-family:'Cinzel',serif;font-size:1.3rem;
                            font-weight:700;color:#C9930A;">Equipo #5 {num}</div>
                <div style="color:#B0C4DE;font-size:0.8rem;margin-top:2px;">
                    {date} · 🏠 {host}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2rem;font-weight:700;color:white;line-height:1;">{p}%</div>
                <div style="color:#8899BB;font-size:0.7rem;">completado</div>
            </div>
        </div>
        <div style="font-size:0.72rem;color:#8899BB;margin-bottom:4px;">
            Progreso · {done_count()}/{TOTAL} secciones
        </div>
        <div class="prog-bg"><div class="prog-fill" style="width:{p}%;"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Banner de revisiones compacto
    rv_count = len(reviews)
    rv_badges = ""
    for r in REVIEWERS:
        if r["id"] in reviews:
            rv_badges += f'<div class="rv-badge done">✅ {r["id"]}</div>'
        else:
            rv_badges += f'<div class="rv-badge pending">⬜ {r["id"]}</div>'
    st.markdown(f"""
    <div style="background:rgba(27,58,107,0.08);border:1px solid #C9930A22;
                border-radius:12px;padding:0.8rem 1rem;margin-bottom:1rem;">
        <div style="font-size:0.75rem;font-weight:700;color:#C9930A;margin-bottom:0.5rem;">
            📋 REVISIÓN PREVIA · {rv_count}/{len(REVIEWERS)} revisaron
        </div>
        <div class="review-badge-grid">{rv_badges}</div>
    </div>
    """, unsafe_allow_html=True)

    # Botón continuar
    next_idx = next((i for i,c in enumerate(st.session_state.completed) if not c), 0)
    next_sec = SECTIONS[next_idx]
    if st.button(f"▶  Continuar: {next_sec['icon']} {next_sec['title']}",
                 use_container_width=True, type="primary", key="map_cont"):
        go(next_idx); st.rerun()

    st.markdown("""
    <div style="font-family:'Cinzel',serif;font-size:0.72rem;color:#888;
                letter-spacing:2px;margin:1rem 0 0.7rem;text-align:center;">
        IR DIRECTAMENTE A CUALQUIER SECCIÓN
    </div>""", unsafe_allow_html=True)

    # Grid de tarjetas HTML + botones Streamlit intercalados
    color_map = {"azul":"#1B3A6B","rojo":"#A62020","dorado":"#C9930A"}
    rows = [SECTIONS[i:i+2] for i in range(0,len(SECTIONS),2)]

    for row in rows:
        cols = st.columns(len(row))
        for col, sec in zip(cols, row):
            with col:
                is_done = st.session_state.completed[sec["id"]]
                is_cur  = sec["id"] == st.session_state.current
                bc      = color_map[sec["color"]]
                badge   = "✅" if is_done else ("🔵" if is_cur else "")
                title_c = "#2E7D32" if is_done else (bc if is_cur else "#1B3A6B")

                st.markdown(f"""
                <div class="map-card {'rojo' if sec['color']=='rojo' else 'dorado' if sec['color']=='dorado' else ''}"
                     style="border-top-color:{bc};">
                    <div class="mc-badge">{badge}</div>
                    <div class="mc-icon">{sec['icon']}</div>
                    <div class="mc-num">PASO {sec['num']}</div>
                    <div class="mc-title" style="color:{title_c};">{sec['title']}</div>
                </div>
                """, unsafe_allow_html=True)

                lbl  = "✅ Ver" if is_done else ("🔵 Aquí" if is_cur else "→ Ir")
                tipo = "primary" if is_cur else "secondary"
                if st.button(lbl, key=f"mg_{sec['id']}",
                             use_container_width=True, type=tipo):
                    go(sec["id"]); st.rerun()

        st.markdown("<div style='margin-bottom:0.3rem;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECCIÓN: ORACIÓN FIJA
# ─────────────────────────────────────────────────────────────────────────────
def render_prayer(sec):
    import re
    cls   = cc(sec)
    pcls  = f"prayer-box {cls}".strip()
    html  = sec["texto"].replace("\n\n","<br><br>").replace("\n","<br>")
    html  = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html  = re.sub(r"\*(.+?)\*",     r"<em>\1</em>",          html)
    if "subtitulo" in sec:
        st.markdown(f'<p style="font-size:0.85rem;color:#888;font-style:italic;">{sec["subtitulo"]}</p>',
                    unsafe_allow_html=True)
    st.markdown(f'<div class="{pcls}">{html}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SECCIÓN: CAMPOS DE NOTAS
# ─────────────────────────────────────────────────────────────────────────────
def render_fields(sec):
    if "instruccion" in sec:
        st.info(sec["instruccion"])
    for campo in sec.get("campos",[]):
        key = f"n_{sec['id']}_{campo['key']}"
        val = st.session_state.notes.get(key,"")
        nv  = st.text_area(campo["label"], value=val,
                           placeholder=campo.get("ph",""), height=100, key=key)
        st.session_state.notes[key] = nv

# ─────────────────────────────────────────────────────────────────────────────
#  SECCIÓN: PUNTOS DE ESFUERZO
# ─────────────────────────────────────────────────────────────────────────────
def render_esfuerzos(sec):
    st.markdown("**Los 6 puntos concretos de esfuerzo de los E.N.S.:**")
    for i,(titulo,desc,color) in enumerate(sec["esfuerzos"]):
        c1,c2 = st.columns([0.07,0.93])
        with c1:
            ch = st.checkbox("",value=st.session_state.duties[i],
                             key=f"d_{i}", label_visibility="collapsed")
            st.session_state.duties[i]=ch
        with c2:
            op  = "0.45" if ch else "1"
            dec = "line-through" if ch else "none"
            st.markdown(f"""
            <div class="effort-row" style="opacity:{op}">
                <div class="effort-badge" style="background:{color};">{i+1}</div>
                <div>
                    <div class="effort-title" style="text-decoration:{dec};">{titulo}</div>
                    <div class="effort-desc">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    render_fields(sec)

# ─────────────────────────────────────────────────────────────────────────────
#  SECCIÓN: MAGNIFICAT
# ─────────────────────────────────────────────────────────────────────────────
def render_magnificat():
    VERSOS = [
        ("Proclama mi alma la grandeza del Señor,",False),
        ("se alegra mi espíritu en Dios, mi salvador;",False),
        ("porque ha mirado la humillación de su esclava.",False),
        ("Desde ahora me felicitarán todas las generaciones,",False),
        ("porque el Poderoso ha hecho obras grandes por mí: su nombre es santo,",False),
        ("y su misericordia llega a sus fieles de generación en generación.",False),
        ("Él hace proezas con su brazo: dispersa a los soberbios de corazón,",False),
        ("derriba del trono a los poderosos y enaltece a los humildes,",False),
        ("a los hambrientos los colma de bienes y a los ricos los despide vacíos.",False),
        ("Auxilia a Israel, su siervo, acordándose de la misericordia",False),
        ("—como lo había prometido a nuestros padres—",False),
        ("en favor de Abrahán y su descendencia por siempre.",False),
        ("Gloria al Padre, al Hijo y al Espíritu Santo.",True),
        ("Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén",True),
    ]
    lines = "".join(
        f'<div class="gloria">✦ {t} ✦</div>' if g else f"<div>{t}</div>"
        for t,g in VERSOS
    )
    st.markdown(f"""
    <div class="magnificat-box">
        <div style="font-family:'Cinzel',serif;font-size:1rem;color:#C9930A;
                    margin-bottom:1rem;letter-spacing:2px;">✦ MAGNIFICAT ✦</div>
        {lines}
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER SECCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def render_section(sec):
    cls = cc(sec)
    nc  = f"sec-num {cls}".strip()
    tc  = f"sec-title {cls}".strip()
    bc  = border(sec)

    st.markdown(f"""
    <div class="section-card {cls}" style="border-left-color:{bc};">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap;">
            <span class="{nc}">{sec['num']}</span>
            <span class="{tc}">{sec['icon']} {sec['title']}</span>
        </div>
    """, unsafe_allow_html=True)

    tipo = sec["tipo"]
    if tipo == "oracion":
        render_prayer(sec)
    elif tipo == "notas":
        render_fields(sec)
    elif tipo == "mixto":
        render_prayer(sec)
        st.markdown("<br>", unsafe_allow_html=True)
        render_fields(sec)
    elif tipo == "esfuerzos":
        render_esfuerzos(sec)
    elif tipo == "magnificat":
        render_magnificat()

    # Descarga del capítulo en la sección Tema de Estudio
    if sec["id"] == 8:
        cap_path = Path(__file__).parent / "assets" / "capitulo3.pdf"
        if cap_path.exists():
            st.download_button(
                label="📕 Descargar Cap. 3 · Incompletitud y Gratuidad",
                data=cap_path.read_bytes(),
                file_name="Capitulo3_Incompletitud_Gratuidad.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  NAVEGACIÓN (mobile-friendly: botones grandes)
# ─────────────────────────────────────────────────────────────────────────────
def render_nav(idx):
    is_last = idx == TOTAL-1

    # Mapa — siempre visible
    if st.button("🗺️ Volver al mapa", use_container_width=True, key="nav_map"):
        st.session_state.show_map=True; st.rerun()

    st.markdown("<div style='margin:0.4rem 0;'></div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if idx>0:
            if st.button("◀", use_container_width=True, key="nav_prev",
                         help="Sección anterior"):
                go(idx-1); st.rerun()
    with c2:
        if not st.session_state.completed[idx]:
            if st.button("✅  Marcar completada", use_container_width=True,
                         type="primary", key="nav_done"):
                st.session_state.completed[idx]=True
                if not is_last: go(idx+1)
                st.rerun()
        else:
            st.markdown('<div style="text-align:center;color:#2E7D32;'
                        'font-weight:700;padding:0.7rem;font-size:0.9rem;">✅ Completada</div>',
                        unsafe_allow_html=True)
    with c3:
        if is_last:
            if st.session_state.completed[idx]:
                if st.button("🎉", use_container_width=True, key="nav_fin",
                             help="Finalizar reunión"):
                    st.session_state.current=TOTAL; st.rerun()
        else:
            if st.button("▶", use_container_width=True, key="nav_next",
                         help="Siguiente sección"):
                go(idx+1); st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  PANTALLA FINAL
# ─────────────────────────────────────────────────────────────────────────────
def render_final():
    e  = int(time.time()-st.session_state.start) if st.session_state.start else 0
    hh,mm = divmod(e//60,60)
    reviews = load_reviews()

    rv_html = "".join(
        f'<div class="rv-badge done">✅ {r["id"]}</div>'
        if r["id"] in reviews else
        f'<div class="rv-badge pending">⬜ {r["id"]}</div>'
        for r in REVIEWERS
    )

    if LOGO_B64:
        st.markdown(f'<div style="text-align:center;">'
                    f'<img src="data:image/png;base64,{LOGO_B64}" '
                    f'style="width:120px;border-radius:12px;border:3px solid #C9930A;'
                    f'margin-bottom:1rem;"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;padding:2rem 1rem;
                background:linear-gradient(135deg,#1B3A6B,#0D2247);
                border-radius:20px;color:white;border:3px solid #C9930A;
                margin-bottom:1.5rem;">
        <div style="font-size:3.5rem;">🎉</div>
        <div style="font-family:'Cinzel',serif;font-size:1.6rem;
                    color:#C9930A;margin:0.5rem 0;">¡Reunión completada!</div>
        <div style="color:#B0C4DE;font-size:0.85rem;">Equipo #5 · Sector Fusagasugá</div>
        <div style="margin-top:1rem;font-size:0.9rem;color:#E0E9FF;">
            ⏱ {hh:02d}h {mm:02d}min &nbsp;·&nbsp; ✅ {done_count()}/{TOTAL} secciones
        </div>
        <div style="margin-top:1rem;">
            <div style="font-size:0.72rem;color:#8899BB;margin-bottom:0.5rem;">REVISIONES PREVIAS</div>
            <div class="review-badge-grid" style="max-width:320px;margin:auto;">{rv_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Notas
    notas = {k:v for k,v in st.session_state.notes.items() if v.strip()}
    if notas:
        st.markdown("### 📝 Notas de la reunión")
        labels = {}
        for sec in SECTIONS:
            for c in sec.get("campos",[]):
                labels[f"n_{sec['id']}_{c['key']}"] = f"{sec['num']}. {sec['title']} · {c['label']}"

        txt = f"GUÍA · EQUIPO #5 ENS · {MEETING_DATE}\n"
        txt += f"Hogar: {MEETING_HOST}\n"
        txt += "="*50+"\n\n"
        for k,v in notas.items():
            lbl = labels.get(k,k)
            st.markdown(f"**{lbl}**")
            st.caption(v)
            txt += f"{lbl}\n{v}\n\n"

        st.download_button("⬇️ Descargar acta (.txt)", data=txt.encode("utf-8"),
                           file_name=f"acta_{st.session_state.date.replace('/','')}.txt",
                           mime="text/plain", use_container_width=True)

    if st.button("🔄 Nueva reunión", type="primary", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  ROUTER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.in_meeting:
    # Vista de revisión previa — la ven todos días antes de la reunión
    render_preview()

elif st.session_state.current >= TOTAL:
    render_sidebar()
    render_final()

elif st.session_state.show_map:
    render_sidebar()
    render_dashboard()

else:
    render_sidebar()
    idx = st.session_state.current
    sec = SECTIONS[idx]

    # Barra de progreso compacta
    p = pct()
    st.markdown(f"""
    <div style="background:white;border-radius:10px;padding:0.6rem 1rem;
                margin-bottom:0.8rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <div style="display:flex;align-items:center;gap:0.8rem;">
            <div style="flex:1;">
                <div style="background:#EEE;border-radius:6px;height:8px;">
                    <div style="background:linear-gradient(90deg,#1B3A6B,#2E5FA3);
                                width:{p}%;height:8px;border-radius:6px;"></div>
                </div>
            </div>
            <div style="font-size:0.8rem;font-weight:700;color:#1B3A6B;white-space:nowrap;">
                {done_count()}/{TOTAL}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_section(sec)
    st.markdown("<br>", unsafe_allow_html=True)
    render_nav(idx)
