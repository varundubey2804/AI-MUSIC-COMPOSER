import streamlit as st
import os
import time
import json
import plotly.graph_objects as go
from dotenv import load_dotenv
import streamlit.components.v1 as components

# --- BACKEND IMPORTS ---
from composer import BollywoodComposer
from coach import SingingCoach
from music_engine import MusicEngine
from audio_analyzer import AudioAnalyzer
from voice_cloning import VoiceCloningEngine
from raga_knowledge import RAGA_DB

load_dotenv()

# -----------------------------------------------------------------------------
# 1. SETUP & INDUSTRIAL THEME ENGINE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MACHINA | Audio Synthesis",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_machina_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Chakra+Petch:wght@400;600;700&display=swap');
        
        .stApp {
            background-color: #050505;
            color: #dcdcdc;
            font-family: 'Space Mono', monospace;
        }

        /* INDUSTRIAL CONTAINERS */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #0f0f0f;
            border: 2px solid #222;
            border-left: 6px solid #222;
            border-radius: 0px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-left-color: #00FF9D;
            border-color: #333;
            box-shadow: -5px 0 15px rgba(0, 255, 157, 0.1);
        }

        /* TYPOGRAPHY */
        h1 {
            font-family: 'Chakra Petch', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.5rem;
            font-size: 3rem !important;
            color: #fff;
            margin-bottom: 0px;
        }
        h2, h3 { font-family: 'Space Mono', monospace; text-transform: uppercase; letter-spacing: 2px; color: #888; }
        .accent-text { color: #00FF9D; font-weight: bold; }
        .copper-text { color: #C4804E; font-weight: bold; }

        /* BUTTONS */
        .stButton button {
            background-color: #1a1a1a !important;
            color: #00FF9D !important;
            border: 1px solid #00FF9D !important;
            border-radius: 0px !important;
            font-family: 'Space Mono', monospace;
            font-weight: 700;
            text-transform: uppercase;
            padding: 15px 30px;
            transition: all 0.2s;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #00FF9D !important;
            color: #000 !important;
            box-shadow: 0 0 10px #00FF9D;
        }

        /* INPUTS */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: #0a0a0a !important;
            color: #fff !important;
            border: 1px solid #333 !important;
            border-radius: 0px !important;
            font-family: 'Space Mono', monospace;
        }
        .stTextInput input:focus, .stTextArea textarea:focus { border-color: #C4804E !important; }
        
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111; color: #666; border: 1px solid #222; border-radius: 0px;
            padding: 10px 20px; font-family: 'Chakra Petch', sans-serif;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00FF9D; color: #000; border-color: #00FF9D; font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 3D RENDER ENGINE (PYTHON -> JS)
# -----------------------------------------------------------------------------
def render_3d_panel(file_path, data_dict, height=350):
    """
    Reads an HTML file, injects a JSON dictionary into the 'DATA' const,
    and renders it in Streamlit.
    """
    try:
        with open(file_path, 'r') as f:
            html_content = f.read()
        
        # Inject Python data into JS
        json_data = json.dumps(data_dict)
        html_content = html_content.replace('const DATA = null;', f'const DATA = {json_data};')
        
        components.html(html_content, height=height, scrolling=False)
    except FileNotFoundError:
        st.error(f"UI Component missing: {file_path}")

# -----------------------------------------------------------------------------
# 3. VISUALIZATIONS
# -----------------------------------------------------------------------------
def plot_machine_radar(scores):
    categories = ['PITCH', 'TIMING', 'VIBE', 'STABILITY', 'RANGE']
    values = [
        int(scores.get('pitch_accuracy', "0").strip('%')),
        int(scores.get('rhythm_accuracy', "0").strip('%')),
        int(scores.get('emotion_match', "0").strip('%')),
        int(scores.get('swara_correctness', "0").strip('%')), 
        80
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill='toself',
        fillcolor='rgba(0, 255, 157, 0.1)', line_color='#00FF9D',
        marker=dict(color='#000', size=6, line=dict(width=1, color='#00FF9D'))
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#333'),
            angularaxis=dict(tickfont=dict(color='#00FF9D', size=12, family='Space Mono')),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300, showlegend=False
    )
    return fig

# -----------------------------------------------------------------------------
# 4. MAIN APP
# -----------------------------------------------------------------------------
def main():
    inject_machina_theme()
    
    st.markdown("<h1 style='text-align:center;'>M A C H I N A . O S</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#C4804E; letter-spacing:3px; margin-bottom:30px;'>// AUDIO_SYNTHESIS_UNIT_V4</div>", unsafe_allow_html=True)

    tabs = st.tabs(["01_COMPOSER", "02_DIAGNOSTICS", "03_CLONING_VAT"])

    # =========================================================================
    # TAB 1: COMPOSER
    # =========================================================================
    with tabs[0]:
        col_controls, col_monitor = st.columns([1, 1.6], gap="large")
        
        with col_controls:
            with st.container(border=True):
                st.markdown("### INPUT_PARAMETERS")
                st.markdown("---")
                prompt = st.text_area("CORE_DIRECTIVE", "Industrial techno in Raag Puriya...", height=100)
                
                c1, c2 = st.columns(2)
                with c1: mood = st.selectbox("ATMOSPHERE", ["Mechanical", "Dark", "Ethereal", "Aggressive"])
                with c2: raga = st.selectbox("SCALE_PROTOCOL", list(RAGA_DB.keys()))
                
                voice = st.radio("EMITTER", ["Male", "Female"], horizontal=True)
                
                st.write("")
                if st.button("INITIATE_SEQUENCE"):
                    composer = BollywoodComposer()
                    engine = MusicEngine()
                    
                    # Set a temporary flag to trigger animation if we were using callbacks
                    # Here we just run the heavy process
                    with st.spinner("PROCESSING WAVEFORMS..."):
                        song_data = composer.generate_full_song(prompt, mood, raga, voice) #
                        if "error" in song_data:
                            st.error(song_data["error"])
                        else:
                            wav = engine.generate_preview_wav(song_data) #
                            st.session_state['song'] = song_data
                            st.session_state['audio'] = wav

        with col_monitor:
            # 3D REACTOR PANEL
            # We determine state based on whether a song exists or user just clicked (simulated)
            reactor_state = "idle"
            if 'song' in st.session_state:
                reactor_state = "generating" # Keep it high energy if song is loaded
            
            # RENDER THE 3D COMPONENT
            render_3d_panel("ui/composer_3d.html", {"state": reactor_state})

            # RESULTS DISPLAY
            if 'song' in st.session_state:
                song = st.session_state['song']
                with st.container(border=True):
                    h1, h2 = st.columns([3, 1])
                    with h1:
                        st.markdown(f"<h2 class='accent-text'>{song.get('meta_emotion', 'TRACK')}</h2>", unsafe_allow_html=True)
                        st.caption(f"ID: {raga.upper()} // ROOT: {song.get('root_note', 'C')}")
                    with h2:
                        st.markdown("<div style='border:1px solid #C4804E; color:#C4804E; padding:5px; text-align:center;'>LIVE</div>", unsafe_allow_html=True)
                    
                    if st.session_state.get('audio'):
                        st.audio(st.session_state['audio'], format='audio/wav')
                    
                    st.markdown("### DATA_STREAM")
                    lyrics_html = "<br>".join([f">> {l}" for l in song.get('lyrics', [])])
                    st.markdown(f"""
                    <div style="height: 200px; overflow-y: auto; background:#000; border:1px solid #333; padding:15px; color:#00FF9D; font-family:'Space Mono'; font-size:0.8rem;">
                        {lyrics_html}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("// SYSTEM_IDLE: AWAITING INPUT")

    # =========================================================================
    # TAB 2: DIAGNOSTICS
    # =========================================================================
    with tabs[1]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            with st.container(border=True):
                st.markdown("### SIGNAL_SOURCE")
                st.markdown("---")
                uploaded_file = st.file_uploader("UPLOAD_WAVEFORM", type=['wav', 'mp3'])
                coach_raga = st.selectbox("PROTOCOL", list(RAGA_DB.keys()), key="anl_raga")
                if st.button("RUN_DIAGNOSTICS", use_container_width=True):
                    if uploaded_file:
                        coach = SingingCoach()
                        analyzer = AudioAnalyzer()
                        with st.spinner("PARSING..."):
                            d = uploaded_file.read()
                            analysis = analyzer.analyze_singing(d, coach_raga) #
                            feedback = coach.evaluate_performance(coach_raga, "Male", "Ref", analysis['detected_notes'], analysis['pitch_score']) #
                            st.session_state['feedback'] = feedback
        with c2:
            if 'feedback' in st.session_state:
                res = st.session_state['feedback']
                with st.container(border=True):
                    if "error" not in res:
                        st.markdown("### BIOMETRICS")
                        fig = plot_machine_radar(res.get('performance_score', {}))
                        st.plotly_chart(fig, use_container_width=True)
                        st.success(f"SYS_MSG: {res.get('guru_comment', 'COMPLETE')}")

    # =========================================================================
    # TAB 3: CLONING VAT
    # =========================================================================
    with tabs[2]:
        with st.container(border=True):
            col_a, col_b = st.columns([1, 1], gap="large")
            with col_a:
                st.markdown("### REPLICATION_PROTOCOL")
                consent = st.text_input("SECURITY_PHRASE", placeholder="i confirm that this is my own voice")
                files = st.file_uploader("SAMPLES", accept_multiple_files=True)
                if st.button("ENGAGE_NEURAL_ENGINE", use_container_width=True):
                    cloner = VoiceCloningEngine()
                    valid, msg = cloner.verify_consent(consent, files) #
                    if valid:
                        with st.spinner("TRAINING..."):
                            time.sleep(2)
                            res = cloner.train_user_model("SUBJECT_01", files) #
                            st.session_state['model'] = res['model_id']
                            st.success("ARCHIVED")
                    else: st.error(msg)
            with col_b:
                st.markdown("### NODES")
                if 'model' in st.session_state:
                    st.markdown(f"<div style='border:2px solid #00FF9D; padding:20px; text-align:center;'><h2>{st.session_state['model']}</h2></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='border:1px dashed #333; padding:20px; text-align:center;'>NO_DATA</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()