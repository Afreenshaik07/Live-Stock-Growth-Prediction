import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from src.auth import require_login

require_login("Farmer")

model = joblib.load("model/livestock_growth_model.pkl")

# ================= PAGE HEADER =================
st.title("Farmer Dashboard")
st.caption("Livestock Growth Decision Support System")

# ================= SYSTEM DASHBOARD =================
st.subheader("System Overview")

o1, o2, o3 = st.columns(3)
o1.metric("System Status", "Active")
o2.metric("Prediction Type", "Single Livestock")
o3.metric("Model Version", "v1.0")

st.divider()

# ================= INPUT PARAMETERS =================
st.subheader("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    feed = st.selectbox("Feed Quality (1 = Low, 3 = High)", [1, 2, 3])
    health = st.slider("Health Score (1–10)", 1, 10, 6)

with col2:
    temperature = st.slider("Temperature (°C)", 15, 45, 28)
    humidity = st.slider("Humidity (%)", 30, 90, 60)

# ================= INPUT VALIDATION =================
if health < 3:
    st.warning("Low health score may significantly reduce growth.")
if temperature > 40:
    st.warning("High temperature may cause heat stress.")
if humidity > 85:
    st.warning("High humidity may affect livestock comfort.")

input_df = pd.DataFrame(
    [[feed, health, temperature, humidity]],
    columns=["feed_quality", "health_score", "temperature", "humidity"]
)

# ================= PREDICTION =================
if st.button("Predict Growth"):
    growth = model.predict(input_df)[0]

    st.divider()
    st.subheader("Prediction Output")

    # PRINT RESULT CLEARLY
    st.write(f"**Predicted Growth Rate:** `{growth:.2f} kg/month`")

    # ================= STATUS =================
    if growth < 1.2:
        status = "Critical"
        st.error("🔴 Livestock Growth Status: CRITICAL")
    elif growth < 1.6:
        status = "Moderate"
        st.warning("🟡 Livestock Growth Status: MODERATE")
    else:
        status = "Good"
        st.success("🟢 Livestock Growth Status: GOOD")

    # ================= VISUAL =================
    st.subheader("Impact of Input Factors")

    fig, ax = plt.subplots()
    ax.bar(
        ["Feed Quality", "Health Score", "Temperature", "Humidity"],
        [feed, health, temperature / 10, humidity / 10]
    )
    ax.set_ylabel("Relative Impact")
    st.pyplot(fig)

    # ================= RECOMMENDATIONS =================
    st.subheader("System Recommendations")

    if feed == 1:
        st.write("• Improve feed quality to enhance growth rate.")
    if health < 5:
        st.write("• Conduct a veterinary health check.")
    if temperature > 38:
        st.write("• Reduce heat stress using cooling or shade.")
    if status == "Good":
        st.write("• Maintain current livestock management practices.")

    # ================= SUMMARY =================
    st.info(
        f"""
        **Result Summary**
        - Predicted Growth Rate: {growth:.2f} kg/month  
        - Growth Status: {status}  
        - Recommendation: Improve weak parameters if any
        """
    )

# ================= ABOUT SYSTEM =================
st.divider()
st.subheader("About This System")

st.write(
    "This system assists farmers in predicting livestock growth using machine learning "
    "based on feed quality, animal health, and environmental conditions. "
    "It supports data-driven decisions to improve productivity."
)

st.subheader("System Notes & Limitations")
st.write(
    "• Predictions depend on data quality and accuracy\n"
    "• Extreme environmental conditions may affect results\n"
    "• The model is trained on representative dataset patterns"
)
