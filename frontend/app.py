import streamlit as st
import requests
import os
import pandas as pd

API_KEY = "eaebdc64-30f3-4f74-8d16-67d69644cf2b"
PREDICT_URL = "https://injury-risk-prediction-production.up.railway.app/predict"

#! PAGE CONFIG
st.set_page_config(
    page_title="Injury Risk Prediction - Inspant",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Fixed and improved
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* ===== CSS VARIABLES ===== */
    :root {
        --primary-bg: #0a0a0a;
        --secondary-bg: #111111;
        --surface-bg: #1a1a1a;
        --elevated-bg: #222222;
        
        --accent-primary: #3b82f6;
        --accent-secondary: #2563eb;
        --accent-success: #10b981;
        --accent-warning: #f59e0b;
        --accent-danger: #ef4444;
        --accent-sport: #f97316;
        
        --text-primary: #ffffff;
        --text-secondary: #e5e5e5;
        --text-tertiary: #a3a3a3;
        --text-quaternary: #737373;
        
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-hover: rgba(255, 255, 255, 0.08);
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        --shadow-3d: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(59, 130, 246, 0.1);
        
        --transition-base: 0.3s ease;
    }

    /* ===== BASE STYLES ===== */
    .stApp {
        background: var(--primary-bg) !important;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container padding */
    .main .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Background gradient */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: 
            radial-gradient(600px circle at 20% 30%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
            radial-gradient(400px circle at 80% 70%, rgba(249, 115, 22, 0.03) 0%, transparent 50%);
        pointer-events: none;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 800 !important;
    }
    
    h1 {
        font-size: clamp(2.5rem, 5vw, 3.5rem) !important;
        line-height: 1.2 !important;
        background: linear-gradient(135deg, var(--text-primary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        padding-top: 0 !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        margin: 0 !important;
        padding: 0 !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
        color: var(--accent-primary) !important;
        -webkit-text-fill-color: var(--accent-primary) !important;
    }
    
    p {
        color: var(--text-tertiary) !important;
        line-height: 1.7 !important;
    }
    
    /* Caption styling */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-quaternary) !important;
        font-size: 1.1rem !important;
        margin-bottom: 2rem !important;
    }

    /* ===== HEADER BADGE ===== */
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .section-icon {
        font-size: 1.5rem;
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    /* ===== STREAMLIT LABELS ===== */
    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ===== SELECT BOX ===== */
    .stSelectbox {
        margin-bottom: 1.25rem;
    }
    
    .stSelectbox > div > div {
        background: var(--elevated-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-base) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 1px var(--accent-primary) !important;
    }
    
    /* Dropdown text color */
    .stSelectbox [data-baseweb="select"] > div {
        color: var(--text-primary) !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="menu"] {
        background: var(--elevated-bg) !important;
        border: 1px solid var(--glass-border) !important;
    }
    
    [data-baseweb="menu"] li {
        background: var(--elevated-bg) !important;
        color: var(--text-primary) !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: var(--glass-hover) !important;
    }

    /* ===== NUMBER INPUT ===== */
    .stNumberInput {
        margin-bottom: 1.25rem;
    }
    
    .stNumberInput > div > div {
        background: var(--elevated-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
    }
    
    .stNumberInput input {
        background: var(--elevated-bg) !important;
        color: var(--text-primary) !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stNumberInput input::placeholder {
        color: var(--text-quaternary) !important;
    }
    
    .stNumberInput > div > div:hover {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 1px var(--accent-primary) !important;
    }
    
    .stNumberInput > div > div:focus-within {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Number input buttons */
    .stNumberInput button {
        background: var(--glass-bg) !important;
        color: var(--text-primary) !important;
        border: none !important;
    }
    
    .stNumberInput button:hover {
        background: var(--glass-hover) !important;
    }

    /* ===== SLIDER ===== */
    .stSlider {
        margin-bottom: 1.5rem;
        padding-top: 0.5rem;
    }
    
    /* Slider track */
    .stSlider > div > div > div[role="slider"] {
        background: var(--elevated-bg) !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div {
        background: var(--glass-border) !important;
    }
    
    /* Slider filled track */
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    }
    
    /* Slider thumb */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent-primary) !important;
        border: 3px solid var(--primary-bg) !important;
        box-shadow: 0 0 0 6px rgba(59, 130, 246, 0.2) !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"]:hover {
        box-shadow: 0 0 0 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Slider value */
    .stSlider [data-testid="stTickBar"] > div {
        color: var(--text-tertiary) !important;
    }

    /* ===== BUTTON ===== */
    .stButton {
        margin-top: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.25rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow-lg) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-3d) !important;
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary)) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ===== ALERTS ===== */
    .stAlert {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        color: var(--text-primary) !important;
    }
    
    .stAlert p {
        color: var(--text-secondary) !important;
    }
    
    [data-baseweb="notification"] {
        background: var(--glass-bg) !important;
        border-left-width: 4px !important;
    }
    
    /* Success alert */
    [data-baseweb="notification"][kind="success"] {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left-color: var(--accent-success) !important;
    }
    
    /* Warning alert */
    [data-baseweb="notification"][kind="warning"] {
        background: rgba(245, 158, 11, 0.1) !important;
        border-left-color: var(--accent-warning) !important;
    }
    
    /* Error alert */
    [data-baseweb="notification"][kind="error"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left-color: var(--accent-danger) !important;
    }
    
    /* Info alert */
    [data-baseweb="notification"][kind="info"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left-color: var(--accent-primary) !important;
    }

    /* ===== METRIC ===== */
    [data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: var(--accent-primary) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        border-top: 2px solid var(--glass-border) !important;
        margin: 3rem 0 !important;
        opacity: 0.5;
    }

    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-color: var(--accent-primary) transparent transparent transparent !important;
    }

    /* ===== CHART ===== */
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        padding: 0 !important; /* ← PENTING */
    }

    /* ===== INFO TEXT ===== */
    .info-text {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 8px;
        padding: 0.875rem 1.25rem;
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .info-text strong {
        color: var(--accent-primary);
    }

    /* ===== COLUMNS GAP ===== */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    [data-testid="column"]:first-child {
        padding-left: 0;
    }
    
    [data-testid="column"]:last-child {
        padding-right: 0;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            padding: 1rem 2rem !important;
            font-size: 1rem !important;
        }
        
        [data-testid="column"] {
            padding: 0 !important;
        }
        
        .section-icon {
            width: 40px;
            height: 40px;
            font-size: 1.25rem;
        }
    }

    /* ===== MARKDOWN CONTENT ===== */
    .stMarkdown {
        color: var(--text-secondary) !important;
    }
    
    .stMarkdown strong {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown em {
        color: var(--text-tertiary) !important;
    }
    
    .stMarkdown code {
        background: var(--elevated-bg) !important;
        color: var(--accent-primary) !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }

    /* ===== TOOLTIP ===== */
    [data-testid="stTooltipIcon"] {
        color: var(--accent-primary) !important;
    }
    
    [role="tooltip"] {
        background: var(--elevated-bg) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--glass-border) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header with badge
st.markdown("""
<div class="header-badge">
    <span>🏃</span>
    AI-Powered Sports Analytics
</div>
""", unsafe_allow_html=True)

st.title("Injury Risk Prediction Dashboard")
st.caption(
    "Early warning system untuk memprediksi risiko cedera atlet "
    "dalam jangka pendek berdasarkan beban latihan & pemulihan"
)

st.markdown("<br>", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    #! ATHLETE PROFILE
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">👤</div>
        <h2>Athlete Profile</h2>
    </div>
    """, unsafe_allow_html=True)

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"],
        help="Jenis kelamin atlet. Digunakan untuk menyesuaikan karakteristik fisiologis."
    )

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=50,
        value=22,
        step=1,
        help="Usia atlet (tahun). Usia memengaruhi daya tahan tubuh dan risiko cedera."
    )

    height = st.number_input(
        "Height (cm)",
        min_value=140,
        max_value=210,
        value=175,
        step=1,
        help="Tinggi badan atlet dalam sentimeter."
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=40,
        max_value=130,
        value=70,
        step=1,
        help="Berat badan atlet dalam kilogram."
    )

    bmi = round(weight / ((height / 100) ** 2), 1)
    st.markdown(f"""
    <div class="info-text">
        <strong>BMI:</strong> {bmi} — Indikator keseimbangan berat badan terhadap tinggi badan
    </div>
    """, unsafe_allow_html=True)

    injury_history = st.selectbox(
        "Previous Injury History",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="Apakah atlet pernah mengalami cedera sebelumnya. "
             "Riwayat cedera meningkatkan risiko cedera berulang."
    )

    stress = st.slider(
        "Stress Level (1–10)",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Tingkat stres fisik & mental atlet. "
             "Stres tinggi dapat menghambat pemulihan dan meningkatkan risiko cedera."
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    #! RECOVERY
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🛌</div>
        <h2>Recovery</h2>
    </div>
    """, unsafe_allow_html=True)

    sleep = st.slider(
        "Sleep Hours",
        min_value=3.0,
        max_value=10.0,
        value=7.0,
        step=0.5,
        help="Rata-rata durasi tidur per malam. "
             "Tidur < 6 jam berhubungan erat dengan peningkatan risiko cedera."
    )

    recovery_time = st.slider(
        "Recovery Time (hours)",
        min_value=6,
        max_value=72,
        value=24,
        step=1,
        help="Waktu pemulihan antar sesi latihan (jam). "
             "Pemulihan yang cukup penting untuk regenerasi otot."
    )

    warmup = st.slider(
        "Warm-up Time (minutes)",
        min_value=0,
        max_value=30,
        value=10,
        step=1,
        help="Durasi pemanasan sebelum latihan. "
             "Pemanasan membantu mengurangi risiko cedera otot & sendi."
    )

with col2:
    #! TRAINING LOAD
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏋️</div>
        <h2>Training Load</h2>
    </div>
    """, unsafe_allow_html=True)

    freq = st.slider(
        "Training Frequency (days/week)",
        min_value=1,
        max_value=7,
        value=5,
        step=1,
        help="Jumlah hari latihan dalam satu minggu. "
             "Frekuensi tinggi tanpa pemulihan cukup meningkatkan beban tubuh."
    )

    duration = st.slider(
        "Training Duration (minutes/session)",
        min_value=30,
        max_value=180,
        value=90,
        step=5,
        help="Durasi latihan per sesi (menit). "
             "Sesi yang terlalu lama meningkatkan kelelahan otot."
    )

    intensity = st.slider(
        "Training Intensity (RPE 1–10)",
        min_value=1,
        max_value=10,
        value=7,
        step=1,
        help="Intensitas latihan berdasarkan RPE (Rate of Perceived Exertion). "
             "1 = sangat ringan, 10 = sangat berat."
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    #! BIOMECHANICS
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">⚖️</div>
        <h2>Biomechanics</h2>
    </div>
    """, unsafe_allow_html=True)

    muscle_asym = st.slider(
        "Muscle Asymmetry (0–1)",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.01,
        help="Tingkat ketidakseimbangan kekuatan otot kiri dan kanan. "
             "0 = seimbang, 1 = sangat tidak seimbang."
    )

    flexibility = st.slider(
        "Flexibility Score (1–10)",
        min_value=1,
        max_value=10,
        value=6,
        step=1,
        help="Skor fleksibilitas tubuh atlet. "
             "Fleksibilitas rendah meningkatkan risiko cedera otot."
    )

#! DATA PAYLOAD
payload = {
    "Gender": gender,
    "Age": age,
    "Height_cm": height,
    "Weight_kg": weight,
    "BMI": bmi,
    "Warmup_Time": warmup,
    "Stress_Level": stress,
    "Injury_History": injury_history,
    "Training_Frequency": freq,
    "Training_Duration": duration,
    "Training_Intensity": intensity,
    "Sleep_Hours": sleep,
    "Recovery_Time": recovery_time,
    "Muscle_Asymmetry": muscle_asym,
    "Flexibility_Score": flexibility
}

#! PREDICTION BUTTON
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 ANALYZE INJURY RISK"):
    with st.spinner("Analyzing athlete injury risk..."):
        try:
            response = requests.post(
                "http://localhost:8000/predict",
                json=payload
            )
            res = response.json()

            st.divider()

            # RESULT - Risk Level Display
            if res["risk_level"] == "High":
                st.error("🔴 **HIGH INJURY RISK**")
            elif res["risk_level"] == "Medium":
                st.warning("🟡 **MODERATE INJURY RISK**")
            else:
                st.success("🟢 **LOW INJURY RISK**")

            # Metric in center
            col_left, col_metric, col_right = st.columns([1, 2, 1])
            with col_metric:
                st.metric(
                    label="Estimated Injury Probability",
                    value=f"{res['confidence']*100:.1f}%"
                )

            # GRAPH: RISK FACTORS
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <div class="section-icon">🧠</div>
                <h2>Risk Factor Profile</h2>
            </div>
            """, unsafe_allow_html=True)

            risk_df = pd.DataFrame({
                "Factor": [
                    "Training Intensity",
                    "Sleep Deficit",
                    "Stress Level",
                    "Muscle Asymmetry",
                    "Low Flexibility"
                ],
                "Score": [
                    intensity,
                    10 - sleep,
                    stress,
                    muscle_asym * 10,
                    10 - flexibility
                ]
            })

            # Wrapper 
            st.markdown(
                '<div style="padding: 1.5rem;">',
                unsafe_allow_html=True
            )

            st.line_chart(
                risk_df.set_index("Factor"),
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # WARNINGS
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <div class="section-icon">🤖</div>
                <h2>AI Sports Injury Risk Consultant</h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("Berikut adalah interpretasi risiko cedera **berdasarkan data yang Anda masukkan**:")
            st.markdown("<br>", unsafe_allow_html=True)

            # SLEEP
            if sleep < 6:
                st.warning(f"""
**Berdasarkan data Anda**, durasi tidur Anda rata-rata **{sleep} jam per malam**,
yang berada di bawah rekomendasi ilmiah untuk atlet.

Dari sudut pandang fisiologis, kurang tidur dapat mengganggu proses regenerasi otot
dan koordinasi neuromuskular, sehingga meningkatkan risiko cedera non-kontak,
terutama pada latihan atau pertandingan intensitas tinggi.

Penelitian oleh **Milewski et al. (2014)** menunjukkan bahwa atlet yang tidur
kurang dari 8 jam per malam memiliki risiko cedera hingga **1.7–2 kali lebih tinggi**
dibandingkan atlet dengan tidur yang cukup.

📚 *Journal of Pediatric Orthopaedics*

**Rekomendasi berbasis jurnal untuk Anda:**
- Tingkatkan durasi tidur menjadi **7–9 jam per malam**
- Jika tidur kurang dari 6 jam, sebaiknya hindari latihan eksplosif atau intensitas tinggi
                """)

            # RECOVERY
            if recovery_time < 24:
                st.warning(f"""
**Berdasarkan data Anda**, waktu pemulihan antar sesi latihan berat hanya sekitar
**{recovery_time} jam**, yang tergolong kurang optimal.

Secara ilmiah, recovery yang tidak memadai menyebabkan akumulasi kelelahan fisiologis
dan micro-damage jaringan otot, yang meningkatkan risiko *overuse injury*.

Menurut **Kellmann et al. (2018)**, ketidakseimbangan antara beban latihan dan pemulihan
merupakan salah satu prediktor utama cedera olahraga.

📚 *Frontiers in Physiology*

**Rekomendasi berbasis jurnal untuk Anda:**
- Tambahkan waktu pemulihan menjadi minimal **24–48 jam**
- Terapkan prinsip *hard–easy training* untuk mengurangi akumulasi kelelahan
                """)

            # STRESS
            if stress >= 8:
                st.warning(f"""
**Berdasarkan data Anda**, tingkat stres psikologis Anda berada pada level **{stress}/10**,
yang tergolong tinggi.

Penelitian menunjukkan bahwa stres psikologis meningkatkan hormon kortisol,
yang berdampak negatif pada pemulihan jaringan dan kontrol motorik.
Kondisi ini dapat meningkatkan risiko cedera non-kontak meskipun beban fisik tidak ekstrem.

Studi oleh **Ivarsson et al. (2017)** menemukan bahwa stres psikologis merupakan
prediktor signifikan terjadinya cedera olahraga.

📚 *Sports Medicine*

**Rekomendasi berbasis jurnal untuk Anda:**
- Pertimbangkan penurunan sementara volume latihan
- Integrasikan mental recovery seperti breathing exercise atau mindfulness
                """)

            # MUSCLE ASYMMETRY
            if muscle_asym >= 0.4:
                st.warning(f"""
**Berdasarkan data Anda**, tingkat ketidakseimbangan otot Anda berada pada nilai
**{muscle_asym:.2f}**, yang menunjukkan adanya perbedaan kekuatan yang signifikan
antara sisi kiri dan kanan tubuh.

Secara biomekanik, kondisi ini dapat menyebabkan distribusi gaya yang tidak merata
saat bergerak, sehingga meningkatkan risiko cedera pada ekstremitas bawah.

Penelitian oleh **Bishop et al. (2018)** menunjukkan bahwa inter-limb asymmetry
berkorelasi dengan peningkatan risiko cedera atlet.

📚 *British Journal of Sports Medicine*

**Rekomendasi berbasis jurnal untuk Anda:**
- Fokuskan latihan pada **unilateral strength training**
- Lakukan evaluasi kekuatan secara berkala sebelum meningkatkan intensitas latihan
                """)

            # FLEXIBILITY
            if flexibility <= 4:
                st.warning(f"""
**Berdasarkan data Anda**, skor fleksibilitas Anda adalah **{flexibility}/10**,
yang tergolong rendah.

Fleksibilitas yang terbatas dapat membatasi range of motion sendi
dan meningkatkan tegangan pada jaringan otot saat gerakan eksplosif,
yang merupakan mekanisme utama terjadinya muscle strain.

Penelitian oleh **Witvrouw et al. (2004)** menyatakan bahwa fleksibilitas rendah
merupakan faktor risiko independen untuk cedera otot.

📚 *American Journal of Sports Medicine*

**Rekomendasi berbasis jurnal untuk Anda:**
- Lakukan dynamic stretching sebelum latihan
- Tambahkan latihan mobility dan flexibility minimal **3–4 kali per minggu**
                """)
                
            if res["risk_level"] == "Low":
                st.success("""
### ✅ Low Injury Risk Detected

**Berdasarkan data yang Anda masukkan**, model memprediksi bahwa risiko cedera Anda
saat ini berada pada kategori **rendah**.

Hal ini menunjukkan bahwa **beban latihan, kualitas pemulihan, dan faktor fisik**
Anda berada dalam kondisi yang relatif seimbang. Secara ilmiah, kondisi ini
mengindikasikan bahwa tubuh Anda mampu beradaptasi dengan tuntutan latihan
tanpa mengalami stres fisiologis yang berlebihan.

Penelitian dalam sports science menunjukkan bahwa atlet dengan:
- durasi tidur yang cukup,
- recovery time yang memadai,
- beban latihan yang terkontrol,
memiliki risiko cedera yang lebih rendah dan adaptasi performa yang lebih optimal.

📚 **Soligard et al., 2016 – British Journal of Sports Medicine**  
📚 **Gabbett, 2016 – British Journal of Sports Medicine**

**Apa arti hasil ini bagi Anda?**
- Tubuh Anda saat ini berada dalam fase *functional adaptation*
- Risiko cedera akut maupun overuse relatif rendah
- Pola latihan dan pemulihan yang Anda lakukan sudah berada pada jalur yang tepat

**Rekomendasi berbasis jurnal untuk mempertahankan kondisi ini:**
- Pertahankan durasi tidur **7–9 jam per malam**
- Naikkan beban latihan secara bertahap (≤10% per minggu)
- Tetap lakukan monitoring recovery dan tanda kelelahan
- Jangan mengabaikan pemanasan dan latihan fleksibilitas

📌 *Catatan penting:*  
Risiko rendah **bukan berarti nol risiko**. Perubahan mendadak pada beban latihan,
kurang tidur, atau peningkatan stres psikologis dapat meningkatkan risiko cedera
dalam waktu singkat.

Model ini berfungsi sebagai **early warning system** untuk membantu Anda
menjaga konsistensi dan keberlanjutan performa.
                """)

        except requests.exceptions.ConnectionError:
            st.error("❌ **Error:** Cannot connect to prediction API")
            st.info("🔧 VPS Disconected")
        except Exception as e:
            st.error(f"❌ **Error:** {str(e)}")
