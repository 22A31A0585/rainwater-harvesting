import streamlit as st



# Set page background color to light green
page_bg = """
<style>
body {
    background-color: #e6f9e6;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'> Smart Rainwater Harvesting System 🌱</h1>", unsafe_allow_html=True)

# Team Info with moderate spacing
st.markdown("""
<div style='text-align: center; font-size:18px; line-height:1.5;'>

<strong>Developed by:</strong> HydroVanta 💧<br><br>
<strong>Team Members:</strong><br>
Md. Anjum Sharifa<br>
M. Lokesh<br><br>
<strong>College:</strong><br>
Pragati Engineering College<br><br>
<strong>Branch & Year:</strong><br>
CSE, 4th Year

</div>
""", unsafe_allow_html=True)

# Divider and intro text
st.markdown("---")
st.write("Welcome! This application helps monitor and forecast water storage using rainfall prediction and real-time analytics. Designed to support sustainable water management practices. 💧📊")

import pandas as pd
import numpy as np

st.markdown("## 📈 Rainfall Forecast (Next 7 Days)")

# Generate dummy rainfall data
days = pd.date_range(start=pd.Timestamp.now().normalize(), periods=7)
rainfall = np.random.randint(10, 100, size=7)  # Random values between 10–100 mm

forecast_df = pd.DataFrame({
    "Date": days.strftime("%d %b %Y"),
    "Predicted Rainfall (mm)": rainfall
})

# Display table
st.table(forecast_df)

# Display bar chart
st.bar_chart(forecast_df.set_index("Date"))
st.markdown("## 💧 Smart Tank Forecast & Suggestions")

# 📌 User Inputs
st.subheader("Enter Your Tank Details:")

current_level = st.number_input("Current tank level (in liters):", min_value=0, max_value=2000, value=500)
roof_area = st.number_input("Rooftop area (in sq. meters):", min_value=10, max_value=500, value=50)
daily_usage = st.number_input("Daily water usage (in liters):", min_value=0, max_value=1000, value=150)

# 📌 Calculations
rainfall_sum = forecast_df["Predicted Rainfall (mm)"].sum()
efficiency = 0.9  # 90% efficiency of collection

# 1 mm rain = 1 liter per sq. meter
collected_water = rainfall_sum * roof_area * efficiency
future_usage = daily_usage * 7  # next 7 days
final_tank_level = current_level + collected_water - future_usage

# Cap within tank capacity
tank_capacity = 1000
final_tank_level = max(0, min(final_tank_level, tank_capacity))

# 📌 Results
st.write(f"Expected Rainfall: **{rainfall_sum:.1f} mm**")
st.write(f"Water that can be collected: **{collected_water:.0f} liters**")
st.write(f"Estimated tank level after 7 days: **{final_tank_level:.0f} / {tank_capacity} liters**")

# 📌 Suggestions
if final_tank_level > tank_capacity:
    st.warning("⚠️ Risk of overflow! Consider draining some water.")
elif final_tank_level < 200:
    st.error("🔄 Risk of water shortage! Try to conserve or store more.")
else:
    st.success("✅ You’re all set! Tank level is optimal.")

    import plotly.graph_objects as go

# Bar chart for predicted rainfall
fig = go.Figure(data=[
    go.Bar(x=forecast_df["Date"], y=forecast_df["Predicted Rainfall (mm)"], marker_color='skyblue')
])

fig.update_layout(
    title="📅 Predicted Rainfall Over Next 7 Days",
    xaxis_title="Day",
    yaxis_title="Rainfall (mm)",
    template="plotly_white"
)

st.plotly_chart(fig)

fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = final_tank_level,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "🔄 Tank Level (liters)", 'font': {'size': 20}},
    gauge = {
        'axis': {'range': [0, tank_capacity]},
        'bar': {'color': "#1f77b4"},
        'steps': [
            {'range': [0, 300], 'color': "lightcoral"},
            {'range': [300, 700], 'color': "khaki"},
            {'range': [700, 1000], 'color': "lightgreen"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': tank_capacity
        }
    }
))

st.plotly_chart(fig_gauge)

from streamlit_chat import message

st.markdown("---")
st.markdown("## 🤖 Ask a Question")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Input box for user
user_input = st.text_input("💬 Ask me anything about water storage or rainfall:", key="input", help="Try: How is rainwater collected?")


if user_input:
    # Predefined detailed responses
    if "rain" in user_input.lower():
        answer = """🌧️ Rainfall Forecast Info:
We use predicted data for the next 7 days to estimate how much rain will fall. This helps in understanding how much water your rooftop can collect, which supports sustainable planning."""
    elif "tank" in user_input.lower():
        answer = """🚰 Tank Level Explanation:
Your water tank level is calculated using:
- Current tank level
- Total rainwater collected from your rooftop
- Daily household usage over 7 days
This helps you know if there’s enough water or a shortage risk."""
    elif "overflow" in user_input.lower():
        answer = """⚠️ Overflow Warning:
If the collected rainwater + current level > tank capacity, the app shows a warning.
Tip: You can divert the excess water to a storage sump or reuse it for gardening."""
    elif "efficiency" in user_input.lower():
        answer = """✅ Harvesting Efficiency:
We assume 90% efficiency. This means 10% of rainwater is lost due to leakage or poor collection.
You can improve efficiency by cleaning rooftops, checking pipes, and installing filters."""
    else:
        answer = """🤖 I didn’t get that. Try asking me about:
- Rain prediction
- Tank usage
- Overflow risks
- Efficiency tips"""

    # Save conversation
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", answer))

# Display chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        message(msg, is_user=True)
    else:
        message(msg)
