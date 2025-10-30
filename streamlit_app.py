import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import colorsys

# --- Page setup ---
st.set_page_config(page_title="Environmental Justice Index (EJI) — New Mexico", layout="wide")

# --- Title ---
st.title("🌎 Environmental Justice Index Visualization (New Mexico)")
st.write("""
The **Environmental Justice Index (EJI)** measures cumulative environmental, social, and health burdens 
in communities relative to others across the U.S.  
Use the dropdowns below to explore **New Mexico** data or compare it to another dataset.
""")

# --- Load data ---
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

with st.spinner("Loading data..."):
    state_df, county_df = load_data()

if state_df is None or county_df is None:
    st.stop()

# --- Color palette (based on CDC EJI color scheme) ---
base_colors = {
    "RPL_EJI": "#009682",   # teal
    "RPL_EBM": "#007D3C",   # green
    "RPL_SVM": "#5A2A7E",   # purple
    "RPL_HVM": "#0050A0",   # blue
    "RPL_CBM": "#B2182B",   # red/orange
}

def lighten_color(hex_color, factor=0.5):
    """Lighten a hex color by blending it with white."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(*rgb)
    l = min(1, l + (1 - l) * factor)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

# --- Metric handling ---
possible_metrics = ["RPL_EJI", "RPL_EBM", "RPL_SVM", "RPL_HVM", "RPL_CBM"]

# --- Dropdowns ---
view_type = st.selectbox("View EJI data for:", ["New Mexico", "County"])
counties = sorted(county_df["County"].dropna().unique())

if view_type == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["County"] == selected_county]
    title_text = f"EJI Metrics — {selected_county}"
else:
    subset = state_df[state_df["State"] == "New Mexico"]
    title_text = "EJI Metrics — New Mexico (State Average)"

if subset.empty:
    st.warning("No data found for your selection.")
    st.stop()

# --- Comparison toggle ---
compare_toggle = st.toggle("🔄 Compare with another dataset?")
if compare_toggle:
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

# --- Plot function ---
def plot_chart(df, label, color_shade=1.0):
    # Identify which metric columns exist in the dataset
    cols = [c for c in df.columns if c in possible_metrics]
    metrics_found = [m for m in possible_metrics if m in cols]

    values = []
    for m in metrics_found:
        if m in df.columns and pd.notna(df[m].values[0]):
            values.append(float(df[m].values[0]))
        else:
            values.append(None)

    colors = [base_colors[m] for m in metrics_found]
    if color_shade < 1.0:
        colors = [lighten_color(c, factor=color_shade) for c in colors]

    fig = go.Figure()
    for metric, val, color in zip(metrics_found, values, colors):
        hover_text = (
            f"<b>{metric}</b><br>Score: {val:.2f}<extra></extra>"
            if val is not None
            else f"<b>{metric}</b><br>No data<extra></extra>"
        )
        fig.add_trace(go.Bar(
            x=[metric],
            y=[val if val is not None else 0],
            marker_color=color if val is not None else "#D3D3D3",
            hovertemplate=hover_text,
            name=metric,
        ))

    fig.update_layout(
        title=label,
        yaxis_title="Percentile Rank (0–1)",
        yaxis=dict(range=[0, 1]),
        xaxis_title="EJI Metric",
        height=450,
        showlegend=False,
        margin=dict(t=50, l=40, r=20, b=40)
    )
    return fig

# --- Layout ---
col1, col2 = (st.columns(2) if compare_toggle else (st.container(), None))

with col1:
    st.subheader(f"📊 {title_text}")
    st.plotly_chart(plot_chart(subset, title_text), use_container_width=True)
    numeric_cols = subset.select_dtypes(include="number").columns
    st.dataframe(subset.style.highlight_max(axis=1, subset=numeric_cols, color="#C2F0C2"))

if compare_toggle and compare_subset is not None and not compare_subset.empty:
    with col2:
        st.subheader(f"📊 Comparison — {compare_label}")
        st.plotly_chart(plot_chart(compare_subset, f"{compare_label}", color_shade=0.45), use_container_width=True)
        numeric_cols = compare_subset.select_dtypes(include="number").columns
        st.dataframe(compare_subset.style.highlight_max(axis=1, subset=numeric_cols, color="#E2D9F3"))

# --- Legend ---
st.markdown("---")
st.subheader("📈 EJI Percentile Scale and Color Key")
st.markdown("""
| Metric | Meaning | Color |
|:--------|:---------|:-------|
| **RPL_EJI** | Overall Environmental Justice Index | 🟩 Teal |
| **RPL_EBM** | Environmental Burden Metric | 🟢 Green |
| **RPL_SVM** | Social Vulnerability Metric | 🟣 Purple |
| **RPL_HVM** | Health Vulnerability Metric | 🔵 Blue |
| **RPL_CBM** | Cumulative Burden Metric | 🔴 Red/Orange |
""")

st.markdown("""
| Percentile Range | Classification | Implication |
|:-----------------|:----------------|:-------------|
| 🟢 0.00–0.25 | Low | Least cumulative burden |
| 🟡 0.25–0.50 | Low–Moderate | Some burden |
| 🟠 0.50–0.75 | Moderate–High | Elevated burden |
| 🔴 0.75–1.00 | High | Greatest cumulative burden |
| ⚪ No data | — | — |
""")

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
