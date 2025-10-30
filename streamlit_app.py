import streamlit as st 
import pandas as pd
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="Environmental Justice Index (EJI) — New Mexico", layout="wide")

# --- Title and description ---
st.title("🌎 Environmental Justice Index Visualization (New Mexico)")
st.write("""
The **Environmental Justice Index (EJI)** measures cumulative environmental, social, and health burdens 
in communities relative to others across the U.S.  

Use the dropdowns below to explore data for **New Mexico** or specific **counties**,  
and optionally compare datasets side-by-side.
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

# --- Rename columns to RPL-style ---
rename_map = {
    "Mean_EJI": "RPL_EJI",
    "Mean_EBM": "RPL_EBM",
    "Mean_SVM": "RPL_SVM",
    "Mean_HVM": "RPL_HVM",
    "Mean_CBM": "RPL_CBM",
    "Mean_EJI_CBM": "RPL_EJI_CBM"
}
state_df.rename(columns=rename_map, inplace=True)
county_df.rename(columns=rename_map, inplace=True)

# --- Define metrics and dropdown options ---
metrics = ["RPL_EJI", "RPL_EBM", "RPL_SVM", "RPL_HVM", "RPL_CBM", "RPL_EJI_CBM"]
counties = sorted(county_df["County"].dropna().unique())
states = sorted(state_df["State"].dropna().unique())
parameter1 = ["New Mexico", "County"]

# --- Custom color palettes ---
dataset1_colors = {
    "RPL_EJI": "#911eb4",
    "RPL_EBM": "#c55c29",
    "RPL_SVM": "#4363d8",
    "RPL_HVM": "#f032e6",
    "RPL_CBM": "#469990",
    "RPL_EJI_CBM": "#801650"
}

dataset2_colors = {
    "RPL_EJI": "#b88be1",
    "RPL_EBM": "#D2B48C",
    "RPL_SVM": "#87a1e5",
    "RPL_HVM": "#f79be9",
    "RPL_CBM": "#94c9c4",
    "RPL_EJI_CBM": "#f17cb0"
}

# --- Helper function to plot grouped comparison ---
def plot_comparison(data1, data2, label1, label2, metrics):
    """
    Shows: (1) transposed comparison table (datasets x metrics),
           (2) grouped bar chart with per-metric per-dataset colors,
           (3) annotations under each metric: left = label1, right = label2,
              centered larger text = metric name.
    """
    # --- Comparison table (datasets as rows) ---
    compare_table = pd.DataFrame({
        "Metric": metrics,
        label1: data1.values,
        label2: data2.values
    }).set_index("Metric").T
    st.subheader("📊 Data Comparison Table")
    st.dataframe(compare_table.style.format("{:.3f}"), use_container_width=True)

    # --- Prepare data for plotting (two traces: label1 and label2) ---
    scores1 = list(data1.values)
    scores2 = list(data2.values)

    # create bar chart with two traces, using per-metric colors
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=metrics,
        y=scores1,
        name=label1,
        marker_color=[dataset1_colors[m] for m in metrics],
        offsetgroup=0,
        width=0.35,
        hovertemplate="%{x}<br>" + f"{label1}: " + "%{y:.3f}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=metrics,
        y=scores2,
        name=label2,
        marker_color=[dataset2_colors[m] for m in metrics],
        offsetgroup=1,
        width=0.35,
        hovertemplate="%{x}<br>" + f"{label2}: " + "%{y:.3f}<extra></extra>"
    ))

    # --- Layout: fixed y axis, gridlines, no automatic legend (we use table) ---
    fig.update_layout(
        barmode='group',
        yaxis=dict(range=[0, 1], dtick=0.25, gridcolor="#E0E0E0", showgrid=True),
        xaxis=dict(tickmode='array', tickvals=metrics, ticktext=metrics),
        margin=dict(t=60, b=140),  # extra bottom margin for annotations
        title=f"EJI Metric Comparison — {label1} vs {label2}",
        legend=dict(title_text="")  # keep legend if you want; toggle as desired
    )

    # --- Annotations beneath each metric ---
    # We'll place two small labels per metric (left/right) and a larger centered metric name.
    annotations = []
    # y positions in 'paper' coordinates (0 = bottom of plotting area, 1 = top).
    # We'll put the dataset subtitles slightly below the axis (y = -0.12 & -0.08 paper coords),
    # and the big metric label further below (y = -0.20).
    small_y1 = -0.12
    small_y2 = -0.08
    big_y = -0.20

    for i, m in enumerate(metrics):
        # left small subtitle (dataset1)
        annotations.append(dict(
            x=m, y=small_y1, xref='x', yref='paper',
            text=f"<b>{label1}</b>", showarrow=False,
            font=dict(size=10, color=dataset1_colors[m]),
            xanchor='center', xshift=-40  # shift left so it sits under left bar
        ))
        # right small subtitle (dataset2)
        annotations.append(dict(
            x=m, y=small_y2, xref='x', yref='paper',
            text=f"<b>{label2}</b>", showarrow=False,
            font=dict(size=10, color=dataset2_colors[m]),
            xanchor='center', xshift=40  # shift right so it sits under right bar
        ))
        # centered metric label (larger)
        annotations.append(dict(
            x=m, y=big_y, xref='x', yref='paper',
            text=f"<span style='font-size:13px'>{m}</span>", showarrow=False,
            font=dict(size=12, color='#333333'),
            xanchor='center'
        ))

    fig.update_layout(annotations=annotations)

    # Render the figure and the table
    st.plotly_chart(fig, use_container_width=True)
    # Table already shown above; optionally show again below:
    # st.dataframe(compare_table.style.format("{:.3f}"), use_container_width=True)


# --- MAIN DISPLAY ---
selected_parameter = st.selectbox("View EJI data for:", parameter1)
st.write(f"**You selected:** {selected_parameter}")

if selected_parameter == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["County"] == selected_county]

    if subset.empty:
        st.warning(f"No data found for {selected_county}.")
    else:
        st.subheader(f"📋 EJI Data for {selected_county}")
        st.dataframe(subset, hide_index=True)

        county_values = subset[metrics].iloc[0]
        fig = px.bar(
            x=metrics,
            y=county_values.values,
            color=metrics,
            color_discrete_map=dataset1_colors,
            labels={"x": "EJI Metric", "y": "RPL Value"},
            title=f"EJI Metrics — {selected_county}"
        )
        fig.update_layout(
            yaxis=dict(range=[0, 1], dtick=0.25, gridcolor="#E0E0E0", showgrid=True),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Comparison Option ---
        if st.checkbox("Compare with another dataset"):
            compare_type = st.radio("Compare with:", ["State", "County"])
            if compare_type == "State":
                comp_state = st.selectbox("Select state:", states)
                comp_row = state_df[state_df["State"] == comp_state]
                if not comp_row.empty:
                    comp_values = comp_row[metrics].iloc[0]
                    plot_comparison(county_values, comp_values, selected_county, comp_state, metrics)
            else:
                comp_county = st.selectbox("Select county:", [c for c in counties if c != selected_county])
                comp_row = county_df[county_df["County"] == comp_county]
                if not comp_row.empty:
                    comp_values = comp_row[metrics].iloc[0]
                    plot_comparison(county_values, comp_values, selected_county, comp_county, metrics)

elif selected_parameter == "New Mexico":
    nm_row = state_df[state_df["State"].str.strip().str.lower() == "new mexico"]

    if nm_row.empty:
        st.warning("No New Mexico data found in the state file.")
    else:
        st.subheader("📋 New Mexico Statewide EJI Scores")
        st.dataframe(nm_row, hide_index=True)

        nm_values = nm_row[metrics].iloc[0]
        fig = px.bar(
            x=metrics,
            y=nm_values.values,
            color=metrics,
            color_discrete_map=dataset1_colors,
            labels={"x": "EJI Metric", "y": "RPL Value"},
            title="EJI Metrics — New Mexico"
        )
        fig.update_layout(
            yaxis=dict(range=[0, 1], dtick=0.25, gridcolor="#E0E0E0", showgrid=True),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Comparison Option ---
        if st.checkbox("Compare with another dataset"):
            compare_type = st.radio("Compare with:", ["State", "County"])
            if compare_type == "State":
                comp_state = st.selectbox("Select state:", [s for s in states if s.lower() != "new mexico"])
                comp_row = state_df[state_df["State"] == comp_state]
                if not comp_row.empty:
                    comp_values = comp_row[metrics].iloc[0]
                    plot_comparison(nm_values, comp_values, "New Mexico", comp_state, metrics)
            else:
                comp_county = st.selectbox("Select county:", counties)
                comp_row = county_df[county_df["County"] == comp_county]
                if not comp_row.empty:
                    comp_values = comp_row[metrics].iloc[0]
                    plot_comparison(nm_values, comp_values, "New Mexico", comp_county, metrics)

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
