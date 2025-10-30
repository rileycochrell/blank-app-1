import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page setup ---
st.set_page_config(page_title="Environmental Justice Index (EJI) — New Mexico", layout="wide")

# --- Title and description ---
st.title("🌎 Environmental Justice Index Visualization (New Mexico)")
st.write("""
The **Environmental Justice Index (EJI)** measures cumulative environmental, social, and health burdens 
in communities relative to others across the U.S.  
Use the dropdowns below to explore data for **New Mexico** or specific **counties**, and optionally compare with another dataset.
""")

# --- Load data from GitHub ---
@st.cache_data
def load_data():
    state_url = "https://github.com/rileycochrell/blank-app-1/raw/refs/heads/main/EJI_StateAverages_RPL.csv"
    county_url = "https://github.com/rileycochrell/blank-app-1/raw/refs/heads/main/EJI_NewMexico_CountyMeans.csv"
    
    try:
        state_df = pd.read_csv(state_url)
        county_df = pd.read_csv(county_url)
        return state_df, county_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

state_df, county_df = load_data()
if state_df is None or county_df is None:
    st.stop()

# --- Metric columns ---
metrics = ["RPL_EJI", "RPL_EBM", "RPL_SVM", "RPL_HVM", "RPL_CBM"]

# --- Color palette (based on CDC EJI map) ---
base_colors = {
    "RPL_EJI": "#009682",   # teal
    "RPL_EBM": "#007D3C",   # green
    "RPL_SVM": "#0050A0",   # blue
    "RPL_HVM": "#5A2A7E",   # purple
    "RPL_CBM": "#B2182B",   # red/orange
}

def lighten_color(hex_color, factor=0.5):
    """Lighten a hex color by blending it with white"""
    import colorsys
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    l = min(1, l + (1 - l) * factor)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

# --- Dropdown selections ---
parameter1 = ["New Mexico", "County"]
selected_parameter = st.selectbox("View EJI data for:", parameter1)

counties = sorted(county_df["County"].dropna().unique())
selected_dataset = None

if selected_parameter == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["County"] == selected_county]
    title_text = f"EJI Metrics — {selected_county}"
else:
    subset = state_df[state_df["State"] == "New Mexico"]
    title_text = "EJI Metrics — New Mexico Statewide"

if subset.empty:
    st.warning("No data found for your selection.")
    st.stop()

# --- Comparison mode ---
compare_toggle = st.toggle("🔄 Compare with another dataset?")
if compare_toggle:
    st.write("Choose a second dataset to compare with the first one.")
    compare_type = st.radio("Compare by:", ["State", "County"], horizontal=True)
    if compare_type == "County":
        compare_target = st.selectbox("Select comparison county:", counties)
        compare_subset = county_df[county_df["County"] == compare_target]
        compare_label = compare_target
    else:
        compare_states = sorted(state_df["State"].dropna().unique())
        compare_target = st.selectbox("Select comparison state:", compare_states)
        compare_subset = state_df[state_df["State"] == compare_target]
        compare_label = compare_target
else:
    compare_subset = None
    compare_label = None

# --- Visualization Section ---
col1, col2 = (st.columns(2) if compare_toggle else (st.container(), None))

def plot_chart(df, label, color_shade=1.0):
    """Generate a single EJI bar chart with color shading"""
    values = [df[m].values[0] if m in df.columns else None for m in metrics]
    colors = [base_colors[m] for m in metrics]

    # Apply lightening for comparison dataset
    if color_shade < 1.0:
        colors = [lighten_color(c, factor=color_shade) for c in colors]

    fig = go.Figure()
    for metric, val, color in zip(metrics, values, colors):
        fig.add_trace(go.Bar(
            x=[metric],
            y=[val],
            name=metric,
            marker_color=color,
            hovertemplate=f"<b>{metric}</b><br>Score: {val:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title=label,
        xaxis_title="EJI Metric",
        yaxis_title="Percentile Rank (0–1)",
        yaxis=dict(range=[0, 1]),
        showlegend=False,
        height=450,
    )
    return fig

# --- Display charts ---
with col1:
    st.subheader(f"📊 {title_text}")
    st.plotly_chart(plot_chart(subset, title_text), use_container_width=True)
    st.dataframe(subset.style.highlight_max(axis=1, color="#C2F0C2"))

if compare_toggle and compare_subset is not None and not compare_subset.empty:
    with col2:
        st.subheader(f"📊 Comparison — {compare_label}")
        st.plotly_chart(plot_chart(compare_subset, f"{compare_label}", color_shade=0.45), use_container_width=True)
        st.dataframe(compare_subset.style.highlight_max(axis=1, color="#E2D9F3"))

# --- Legend Section ---
st.markdown("---")
st.subheader("📈 EJI Percentile Scale")

st.markdown("""
| Range | Classification | Color Meaning |
|:------|:----------------|:---------------|
| ⬜ No data | — | — |
| 🟢 0.00–0.25 | Low | Least cumulative burden |
| 🟡 0.25–0.50 | Low–Moderate | Some burden |
| 🟠 0.50–0.75 | Moderate–High | Elevated burden |
| 🔴 0.75–1.00 | High | Greatest cumulative burden |
""")

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
