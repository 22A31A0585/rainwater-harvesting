import streamlit as st



# Set page background color to light green
# ✅ Full Dark Mode Styling
light_mode_css = """
<style>
html, body {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Headings and general text */
h1, h2, h3, h4, h5, h6,
p, div, span, label, strong {
    color: #000000 !important;
}

/* Input fields */
input, textarea, select {
    background-color: #f0f0f0 !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
}

/* Tables */
thead, tbody, tr, th, td {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-color: #dddddd !important;
}

/* Buttons */
button, .stButton > button {
    background-color: #e0e0e0 !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
}

/* Charts & tables container */
.stPlotlyChart, .stTable {
    background-color: #ffffff !important;
}

/* Sidebar & labels fix */
.css-1cpxqw2, .css-81oif8 {
    color: #000000 !important;
}
</style>
"""
st.markdown(light_mode_css, unsafe_allow_html=True)



# Title
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>Smart Rainwater Harvesting System</h1>", unsafe_allow_html=True)


# Team Info with moderate spacing
# Team Info — beginner friendly
st.markdown("""
<div style='
    background-color: #f5f7fa;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
    font-family: "Segoe UI", sans-serif;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
'>

<h2 style='color: #2c3e50;'>👨‍💻 Team Information</h2>

<p style='font-size:18px; margin-top: 20px;'>
    <strong>Project Name:</strong><br>🌧️ Smart Rainwater Harvesting System
</p>

<p style='font-size:18px; margin-top: 15px;'>
    <strong>Team Name:</strong><br>💧 HydroVanta
</p>

<p style='font-size:18px; margin-top: 15px;'>
    <strong>Team Members:</strong><br>
    Md. Anjum Sharifa<br>
    M. Lokesh
</p>

<p style='font-size:18px; margin-top: 15px;'>
    <strong>Institution:</strong><br>🏫 Pragati Engineering College
</p>

<p style='font-size:18px; margin-top: 15px;'>
    <strong>Branch & Year:</strong><br>💻 CSE, Final Year (4th Year)
</p>

</div>
""", unsafe_allow_html=True)


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
import plotly.express as px

labels = ['Collected Water', 'Future Usage', 'Remaining Capacity']
values = [collected_water, future_usage, max(0, tank_capacity - final_tank_level)]

fig_pie = px.pie(
    names=labels,
    values=values,
    title="💧 Water Distribution Over Next 7 Days",
    color_discrete_sequence=px.colors.sequential.Blues
)
fig_pie.update_layout(height=300, width=500)
st.plotly_chart(fig_pie)




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
    template="plotly_dark",  # Dark mode
    height=300,  # Smaller height
    width=600    # Smaller width
)
st.plotly_chart(fig)


fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = final_tank_level,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "🔄 Tank Level (liters)", 'font': {'size': 18}},
    gauge = {
        'axis': {'range': [0, tank_capacity]},
        'bar': {'color': "#1f77b4"},
        'steps': [
            {'range': [0, 300], 'color': "darkred"},
            {'range': [300, 700], 'color': "goldenrod"},
            {'range': [700, 1000], 'color': "green"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': tank_capacity
        }
    }
))
fig_gauge.update_layout(height=300, width=600)
st.plotly_chart(fig_gauge)

from streamlit_chat import message

st.markdown("---")
st.markdown("## 🤖 Ask a Question")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Clear Chat button
if st.button("🔄 Clear Chat"):
    st.session_state['messages'] = []

# Input
user_input = st.text_input("💬 Ask me anything about water storage or rainfall:", key="input")

if user_input:
    lower_input = user_input.lower()

    if lower_input in ["hi", "hello", "hey"]:
        answer = "👋 Hello! I’m your water assistant. Ask me anything about rainfall, tank usage, or overflow."
    elif "rain" in lower_input:
        answer = "🌧️ Rainfall is predicted using weather data for 7 days. It helps calculate water you can collect from your rooftop."
    elif "tank" in lower_input:
        answer = "🚰 Tank level is based on current level, rainfall collection, and usage. This helps predict shortage or overflow."
    elif "overflow" in lower_input:
        answer = "⚠️ Overflow means your tank might exceed capacity. You can drain it or redirect it to garden/well."
    elif "efficiency" in lower_input:
        answer = "✅ 90% efficiency is assumed due to small losses in pipes or filters. You can increase it by cleaning and maintaining your system."
    elif "harvesting" in lower_input:
        answer = "🌿 Rainwater harvesting is collecting and storing rainwater for reuse. It reduces dependency on groundwater."
    elif "improve" in lower_input or "better" in lower_input:
        answer = "🛠️ Improve by: cleaning rooftop, using mesh filters, and connecting overflow to a backup tank."
    else:
        answer = "🤖 I didn’t get that. Try asking about: rain prediction, tank usage, overflow risks, or tips."

    # Save to chat history
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", answer))

# Display chat history
for sender, msg in st.session_state.messages:
    message(msg, is_user=(sender == "user"))
