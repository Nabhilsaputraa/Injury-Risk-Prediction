import streamlit as st
import requests
import pandas as pd

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="Injury Risk Prediction",
    layout="centered"
)

st.title("🏃 Injury Risk Prediction Dashboard")
st.caption(
    "Early warning system untuk memprediksi risiko cedera atlet "
    "dalam jangka pendek berdasarkan beban latihan & pemulihan"
)

# ========================
# ATHLETE PROFILE
# ========================
st.subheader("👤 Athlete Profile")

gender = st.selectbox(
    "Gender",
    ["Male", "Female"],
    help="Jenis kelamin atlet. Digunakan untuk menyesuaikan karakteristik fisiologis."
)

age = st.number_input(
    "Age",
    15, 50, 22,
    help="Usia atlet (tahun). Usia memengaruhi daya tahan tubuh dan risiko cedera."
)

height = st.number_input(
    "Height (cm)",
    140, 210, 175,
    help="Tinggi badan atlet dalam sentimeter."
)

weight = st.number_input(
    "Weight (kg)",
    40, 130, 70,
    help="Berat badan atlet dalam kilogram."
)

bmi = round(weight / ((height / 100) ** 2), 1)
st.write(
    f"**BMI:** {bmi} "
    "(Indikator keseimbangan berat badan terhadap tinggi badan)"
)

injury_history = st.selectbox(
    "Previous Injury History",
    [0, 1],
    format_func=lambda x: "No" if x == 0 else "Yes",
    help="Apakah atlet pernah mengalami cedera sebelumnya. "
         "Riwayat cedera meningkatkan risiko cedera berulang."
)

stress = st.slider(
    "Stress Level (1–10)",
    1, 10, 5,
    help="Tingkat stres fisik & mental atlet. "
         "Stres tinggi dapat menghambat pemulihan dan meningkatkan risiko cedera."
)

# ========================
# TRAINING LOAD
# ========================
st.subheader("🏋️ Training Load")

freq = st.slider(
    "Training Frequency (days/week)",
    1, 7, 5,
    help="Jumlah hari latihan dalam satu minggu. "
         "Frekuensi tinggi tanpa pemulihan cukup meningkatkan beban tubuh."
)

duration = st.slider(
    "Training Duration (minutes/session)",
    30, 180, 90,
    help="Durasi latihan per sesi (menit). "
         "Sesi yang terlalu lama meningkatkan kelelahan otot."
)

intensity = st.slider(
    "Training Intensity (RPE 1–10)",
    1, 10, 7,
    help="Intensitas latihan berdasarkan RPE (Rate of Perceived Exertion). "
         "1 = sangat ringan, 10 = sangat berat."
)

# ========================
# RECOVERY
# ========================
st.subheader("🛌 Recovery")

sleep = st.slider(
    "Sleep Hours",
    3.0, 10.0, 7.0, 0.5,
    help="Rata-rata durasi tidur per malam. "
         "Tidur < 6 jam berhubungan erat dengan peningkatan risiko cedera."
)

recovery_time = st.slider(
    "Recovery Time (hours)",
    6, 72, 24,
    help="Waktu pemulihan antar sesi latihan (jam). "
         "Pemulihan yang cukup penting untuk regenerasi otot."
)

warmup = st.slider(
    "Warm-up Time (minutes)",
    0, 30, 10,
    help="Durasi pemanasan sebelum latihan. "
         "Pemanasan membantu mengurangi risiko cedera otot & sendi."
)

# ========================
# BIOMECHANICS
# ========================
st.subheader("⚖️ Biomechanics")

muscle_asym = st.slider(
    "Muscle Asymmetry (0–1)",
    0.0, 1.0, 0.2,
    help="Tingkat ketidakseimbangan kekuatan otot kiri dan kanan. "
         "0 = seimbang, 1 = sangat tidak seimbang."
)

flexibility = st.slider(
    "Flexibility Score (1–10)",
    1, 10, 6,
    help="Skor fleksibilitas tubuh atlet. "
         "Fleksibilitas rendah meningkatkan risiko cedera otot."
)

# ========================
# DATA PAYLOAD
# ========================
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

# ========================
# PREDICTION
# ========================
if st.button("🔍 Predict Injury Risk"):
    with st.spinner("Analyzing athlete injury risk..."):
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload
        )
        res = response.json()

    st.divider()

    # ========================
    # RESULT
    # ========================
    if res["risk_level"] == "High":
        st.error("🔴 HIGH INJURY RISK")
    elif res["risk_level"] == "Medium":
        st.warning("🟡 MODERATE INJURY RISK")
    else:
        st.success("🟢 LOW INJURY RISK")

    st.metric(
        label="Estimated Injury Probability",
        value=f"{res['confidence']*100:.1f}%"
    )

    # ========================
    # GRAPH: RISK FACTORS
    # ========================
    st.subheader("🧠 Risk Factor Profile")

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

    st.line_chart(risk_df.set_index("Factor"))

    # ========================
    # WARNINGS
    # ========================
    st.subheader("🤖 AI Sports Injury Risk Consultant")

    st.markdown("Berikut adalah interpretasi risiko cedera **berdasarkan data yang Anda masukkan**:")

    # ======================
    # SLEEP
    # ======================
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

    # ======================
    # RECOVERY
    # ======================
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

    # ======================
    # STRESS
    # ======================
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

    # ======================
    # MUSCLE ASYMMETRY
    # ======================
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

    # ======================
    # FLEXIBILITY
    # ======================
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
        st.success(f"""
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


