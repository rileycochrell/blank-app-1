import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="EJI Scale and Categories", layout="wide")

st.title("🌡️ Understanding the EJI Scale")

st.write("""
The Environmental Justice Index (EJI) ranges from **0 to 1**, where:
- Lower scores (green) indicate **fewer cumulative impacts** and **lower environmental justice concern**.
- Higher scores (red) indicate **greater cumulative impacts** and **higher environmental justice concern**.

Below is a visual scale and a reference table showing percentile ranges, categories, and their meanings.
""")

# --- COLOR SCALE BAR (green → yellow → orange → red)
fig = go.Figure(data=[
    go.Indicator(
        mode="gauge+number",
        value=0.5,
        title={'text': "EJI Percentile Scale (0 to 1)"},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "lightgray"},
            'steps': [
                {'range': [0, 0.25], 'color': '#4CAF50'},   # green
                {'range': [0.25, 0.5], 'color': '#FFEB3B'}, # yellow
                {'range': [0.5, 0.75], 'color': '#FF9800'}, # orange
                {'range': [0.75, 1.0], 'color': '#F44336'}  # red
            ]
        }
    )
])

fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

# --- CATEGORY TABLE
data = {
    "Percentile Range": ["0.00–0.25", "0.26–0.50", "0.51–0.75", "0.76–1.00"],
    "Category": ["Low Concern", "Moderate Concern", "High Concern", "Very High Concern"],
    "Color": ["🟩 Green", "🟨 Yellow", "🟧 Orange", "🟥 Red"],
    "Description": [
        "Communities with lower cumulative environmental, social, and health burdens.",
        "Communities with some environmental or social stressors but not extreme.",
        "Communities with elevated levels of cumulative burden and vulnerability.",
        "Communities facing the highest combined burdens across indicators."
    ]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True, hide_index=True)
