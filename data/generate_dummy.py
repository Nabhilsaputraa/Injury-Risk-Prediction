import numpy as np
import pandas as pd

# ==============================
# CONFIG
# ==============================
N_SAMPLES = 3000
RANDOM_SEED = 42
OUTPUT_PATH = "data/athlete_injury_risk_dummy.csv"

np.random.seed(RANDOM_SEED)

# ==============================
# GENERATE BASE DATA
# ==============================
df = pd.DataFrame({
    "Athlete_ID": np.arange(1, N_SAMPLES + 1),
    "Age": np.random.randint(17, 35, N_SAMPLES),
    "Gender": np.random.choice(["Male", "Female"], N_SAMPLES),
    "Position": np.random.choice(
        ["Forward", "Midfielder", "Defender", "Goalkeeper", "Sprinter", "Swimmer"],
        N_SAMPLES
    ),
    "Training_Intensity": np.random.randint(4, 10, N_SAMPLES),  # scale 1–10
    "Training_Hours_Per_Week": np.random.randint(5, 20, N_SAMPLES),
    "Recovery_Days_Per_Week": np.random.randint(1, 4, N_SAMPLES),
    "Match_Count_Per_Week": np.random.randint(0, 4, N_SAMPLES),
    "Rest_Between_Events_Days": np.random.randint(0, 5, N_SAMPLES),
    "Fatigue_Score": np.random.randint(30, 95, N_SAMPLES),
    "Sleep_Hours": np.clip(np.random.normal(7, 1, N_SAMPLES), 4, 9),
    "HRV": np.clip(np.random.normal(70, 15, N_SAMPLES), 30, 120),
})

# ==============================
# FEATURE ENGINEERING (WITH NOISE)
# ==============================
df["Training_Load"] = (
    df["Training_Intensity"] * df["Training_Hours_Per_Week"]
    + np.random.normal(0, 15, N_SAMPLES)
)

df["Acute_Load"] = df["Training_Load"] + np.random.normal(0, 20, N_SAMPLES)
df["Chronic_Load"] = (
    df["Training_Load"].rolling(4, min_periods=1).mean()
    + np.random.normal(0, 10, N_SAMPLES)
)

df["ACWR"] = df["Acute_Load"] / (df["Chronic_Load"] + 1)

df["Recovery_Index"] = (
    df["Recovery_Days_Per_Week"] * df["Rest_Between_Events_Days"]
    + np.random.normal(0, 1, N_SAMPLES)
)

df["Fatigue_Ratio"] = (
    df["Fatigue_Score"] / (df["Recovery_Days_Per_Week"] + 1)
    + np.random.normal(0, 0.5, N_SAMPLES)
)

# ==============================
# LATENT RISK SCORE (STOCHASTIC)
# ==============================
risk_score = (
    0.35 * df["Training_Load"]
    + 0.30 * df["Fatigue_Score"]
    + 25 * df["ACWR"]
    - 12 * df["Recovery_Days_Per_Week"]
    - 8 * df["Sleep_Hours"]
    + np.random.normal(0, 35, N_SAMPLES)  # <- noise kunci
)

# ==============================
# RISK LEVEL (TARGET)
# ==============================
df["Risk_Level"] = pd.cut(
    risk_score,
    bins=[-np.inf, 140, 200, np.inf],
    labels=["low", "Medium", "High"]
)

# ==============================
# INJURY INDICATOR (FUTURE EVENT)
# ==============================
injury_prob = np.clip(
    0.05
    + 0.15 * (df["Risk_Level"] == "Medium").astype(int)
    + 0.35 * (df["Risk_Level"] == "High").astype(int)
    + np.random.normal(0, 0.05, N_SAMPLES),
    0,
    1
)

df["Injury_Indicator"] = np.random.binomial(1, injury_prob)

# ==============================
# FINAL CLEANING
# ==============================
df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

# ==============================
# SAVE TO CSV
# ==============================
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Dummy dataset generated successfully!")
print("Shape:", df.shape)
print("Risk Level distribution:")
print(df["Risk_Level"].value_counts())
print(f"Saved to: {OUTPUT_PATH}")
