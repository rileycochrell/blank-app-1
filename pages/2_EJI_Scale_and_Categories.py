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
st.image("ff9aadd5-e7d0-4bb7-8ecf-3533237d8d05.png", caption="EJI Percentile Scale (Low to High Burden)", use_container_width=False)
