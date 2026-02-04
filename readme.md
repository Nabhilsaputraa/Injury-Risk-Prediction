██╗███╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗████████╗
██║████╗  ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝
██║██╔██╗ ██║███████╗██████╔╝███████║██╔██╗ ██║   ██║   
██║██║╚██╗██║╚════██║██╔═══╝ ██╔══██║██║╚██╗██║   ██║   
██║██║ ╚████║███████║██║     ██║  ██║██║ ╚████║   ██║   
╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   


# 🏃‍♂️ Injury Risk Prediction System

## 📌 Project Overview
**Injury Risk Prediction System** is a Machine Learning–based application designed to predict **athlete injury risk within the next 7–14 days** using training load, physiological indicators, and recovery-related features.

The system functions as an **early warning decision-support tool** to help coaches, sports scientists, and athletes:
- Prevent overtraining
- Optimize training and recovery planning
- Reduce short-term injury risk

---

## 🎯 Project Objectives
This project aims to:
- Predict short-term injury risk (7–14 days ahead)
- Identify athletes with elevated injury risk early
- Provide interpretable insights into injury-related risk factors
- Support data-driven training and recovery decisions

---

## 📤 Model Outputs
The model produces the following outputs:
- **Injury Risk Classification**
  - 🟢 Low
  - 🟡 Medium
  - 🔴 High
- **Confidence Score** (prediction probability)
- **Key Risk Indicators**
- **Feature Importance Insights**

All outputs are visualized through an interactive **Streamlit dashboard**.

---
## 📊 Features Used
Model ini menggunakan kombinasi **fitur mentah (raw features)** dari dataset asli dan **fitur turunan (feature engineering)** yang dihitung selama preprocessing.

### 🔹 Raw Features (Input Dataset)
Fitur-fitur berikut diambil langsung dari dataset Kaggle dan digunakan sebagai input model:

| Feature | Description |
|------|------------|
| `Gender` | Jenis kelamin atlet (Male / Female) |
| `Age` | Usia atlet (tahun) |
| `Height_cm` | Tinggi badan atlet (cm) |
| `Weight_kg` | Berat badan atlet (kg) |
| `BMI` | Body Mass Index |
| `Training_Frequency` | Jumlah sesi latihan per minggu |
| `Training_Duration` | Durasi rata-rata latihan per sesi (menit) |
| `Training_Intensity` | Intensitas latihan (skala numerik) |
| `Warmup_Time` | Durasi pemanasan sebelum latihan (menit) |
| `Sleep_Hours` | Rata-rata jam tidur per malam |
| `Recovery_Time` | Waktu pemulihan antar sesi latihan (jam) |
| `Stress_Level` | Tingkat stres psikologis (skala numerik) |
| `Muscle_Asymmetry` | Tingkat ketidakseimbangan otot |
| `Flexibility_Score` | Skor fleksibilitas tubuh |
| `Injury_History` | Riwayat cedera sebelumnya (0 = Tidak, 1 = Ya) |

---

### 🔹 Engineered Features (Computed During Preprocessing)
Fitur-fitur berikut **tidak ada secara langsung di dataset**, tetapi dihitung selama preprocessing untuk menangkap hubungan fisiologis yang lebih relevan dengan risiko cedera:

| Feature | Formula | Interpretation |
|------|--------|---------------|
| `Training_Load` | `Training_Frequency × Training_Duration × Training_Intensity` | Representasi total beban latihan atlet |
| `Recovery_Quality` | `Sleep_Hours × Recovery_Time` | Indikator kualitas pemulihan atlet |
| `Physical_Imbalance` | `Muscle_Asymmetry / (Flexibility_Score + 1)` | Risiko biomekanik akibat ketidakseimbangan dan fleksibilitas rendah |

---

### 🎯 Target Variable
Model memprediksi variabel target berikut:

| Target | Description |
|------|------------|
| `Injury_Risk` | Risiko cedera atlet (0 = Low Risk, 1 = High Risk) |

---

## 📈 Dataset
This project is trained using a **real-world dataset** obtained from Kaggle:

🔗 **SIRP-600: Sports Injury Risk Prediction Dataset**  
https://www.kaggle.com/datasets/yuanchunhong/sirp-600-sports-injury-risk-prediction-dataset

The dataset contains athlete training data, physiological parameters, and injury risk labels.

---

## 🧪 Synthetic / Dummy Data Usage
In addition to the original dataset, **synthetic (dummy) data** is used **only for system validation purposes**, including:
- API endpoint testing
- Streamlit dashboard interaction testing
- Extreme-case scenario simulation (high-risk vs low-risk athletes)

📌 **Synthetic data is NOT used as the primary training dataset**, but solely for:
- Proof of concept
- End-to-end system validation
- UI and deployment testing

---

## 🔍 Model Explainability
To improve interpretability, the system uses **Logistic Regression coefficients** to:
- Identify the most influential injury risk factors
- Provide understandable insights for coaches and athletes
- Generate **Key Risk Indicators** displayed in the dashboard

This approach ensures the model is **transparent and explainable**, avoiding black-box predictions.

---

## ⚠️ Limitations
- The dataset does not cover all athlete populations or sports
- Biomechanical and motion-capture data are not included
- Predictions are probabilistic and **not medical diagnoses**

📌 This system is intended as a **decision-support tool**, not a medical diagnostic system.

---

## 🚀 Project Status
- ✅ Real-world dataset implemented
- ✅ Preprocessing & training pipeline completed
- ✅ Model inference validated
- ✅ REST API (FastAPI) deployed
- ✅ Streamlit dashboard integrated
- ✅ Docker-ready architecture
- ⚠️ Early-stage deployment / research prototype

---

## 🔮 Future Improvements
Planned enhancements include:
- Time-series modeling (LSTM / Temporal ML)
- Explainable AI (SHAP)
- Wearable sensor data integration
- Longitudinal athlete monitoring
- Real-world validation with larger datasets

---

## 🛠 Tech Stack
- **Python**
- **Scikit-learn**
- **FastAPI**
- **Streamlit**
- **Docker**
- **Pandas / NumPy**

---

## 📄 Disclaimer
This project is developed for **research and educational purposes only**.  
It does not replace professional medical advice or injury diagnosis.

---


