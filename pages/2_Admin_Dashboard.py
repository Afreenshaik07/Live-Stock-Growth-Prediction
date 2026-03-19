import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from src.auth import require_login

require_login("Admin")

model = joblib.load("model/livestock_growth_model.pkl")

# ================= PAGE HEADER =================
st.title("Admin Dashboard")
st.caption("System Monitoring, Batch Analytics & Decision Support")

# ================= SYSTEM DASHBOARD =================
st.subheader("System Overview")

s1, s2, s3, s4 = st.columns(4)
s1.metric("System Status", "Running")
s2.metric("Model Used", "Random Forest")
s3.metric("Prediction Mode", "Batch")
s4.metric("Version", "v1.0")

st.divider()

# ================= DATA UPLOAD =================
st.subheader("Batch Data Upload")

file = st.file_uploader(
    "Upload Livestock Dataset (CSV with feed_quality, health_score, temperature, humidity)",
    type=["csv"]
)

if file:
    df = pd.read_csv(file)

    # ================= VALIDATION =================
    required_cols = ["feed_quality", "health_score", "temperature", "humidity"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Dataset error: Missing required column '{col}'")
            st.stop()

    df["predicted_growth"] = model.predict(df)

    st.divider()
    st.subheader("Batch Performance Summary")

    k1, k2, k3 = st.columns(3)
    k1.metric("Average Growth Rate", f"{df['predicted_growth'].mean():.2f}")
    k2.metric("Low Growth Count", (df["predicted_growth"] < 1.2).sum())
    k3.metric("Maximum Growth Rate", f"{df['predicted_growth'].max():.2f}")

    # ================= BATCH ANALYSIS GRAPHS =================
    st.subheader("Batch Analysis Graphs")

    fig1, ax1 = plt.subplots()
    ax1.hist(df["predicted_growth"], bins=10)
    ax1.set_title("Growth Rate Distribution")
    ax1.set_xlabel("Growth Rate (kg/month)")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.scatter(df["health_score"], df["predicted_growth"])
    ax2.set_xlabel("Health Score")
    ax2.set_ylabel("Growth Rate")
    ax2.set_title("Health Score vs Growth Rate")
    st.pyplot(fig2)

    # ================= CORRELATION =================
    st.subheader("Correlation Analysis")

    fig3, ax3 = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

    # ================= LOW PERFORMERS =================
    st.subheader("Low Performing Livestock")
    st.dataframe(df[df["predicted_growth"] < 1.2])

    # ================= SYSTEM RECOMMENDATIONS =================
    st.subheader("Batch-Level Recommendations")

    if (df["predicted_growth"] < 1.2).mean() > 0.3:
        st.warning("More than 30% livestock show low growth.")
    if df["health_score"].mean() < 6:
        st.warning("Average health score is low across the batch.")
    if df["temperature"].mean() > 35:
        st.warning("High average temperature detected in dataset.")

    st.success("Batch analysis completed successfully.")

    st.divider()
    st.subheader("Processed Dataset Preview")
    st.dataframe(df)

# ================= ABOUT SYSTEM =================
st.divider()
st.subheader("About This System")

st.write(
    "This admin module provides batch-level analysis, performance monitoring, "
    "and decision support for farm managers using livestock growth predictions."
)
