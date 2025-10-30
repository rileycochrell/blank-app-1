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

# --- Main selection ---
selected_parameter = st.selectbox("View EJI data for:", parameter1)
st.write(f"**You selected:** {selected_parameter}")

# --- Helper function to plot grouped comparison ---
def plot_comparison(data1, data2, label1, label2, metrics):
    # --- Create comparison table (datasets as rows, metrics as columns) ---
    compare_df = pd.DataFrame([list(data1.values), list(data2.values)], 
                              index=[label1, label2], 
                              columns=metrics)

    # --- Display table ---
    st.subheader("📊 Data Comparison Table")
    st.dataframe(compare_df.style.format("{:.3f}"), hide_index=False)

    # --- Prepare data for grouped bar chart ---
    plot_df = compare_df.reset_index().melt(id_vars="index", 
                                            var_name="Metric", 
                                            value_name="Score")
    plot_df.rename(columns={"index": "Dataset"}, inplace=True)

    # --- Grouped bar chart ---
    fig = px.bar(
        plot_df,
        x="Metric",
        y="Score",
        color="Dataset",
        barmode="group",
        title=f"EJI Metric Comparison — {label1} vs {label2}",
        labels={"Score": "RPL Value", "Metric": "Metric"},
    )

    fig.update_layout(yaxis=dict(range=[0, 1]))
    st.plotly_chart(fig, use_container_width=True)

# --- MAIN DISPLAY ---
if selected_parameter == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["County"] == selected_county]

    if subset.empty:
        st.warning(f"No data found for {selected_county}.")
    else:
        st.subheader(f"📋 EJI Data for {selected_county}")
        st.dataframe(subset, hide_index=True)

        county_values = subset[metrics].iloc[0]
        st.plotly_chart(px.bar(
            x=metrics, y=county_values.values,
            labels={"x": "EJI Metric", "y": "RPL Value"},
            title=f"EJI Metrics — {selected_county}"
        ), use_container_width=True)

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
        st.plotly_chart(px.bar(
            x=metrics, y=nm_values.values,
            labels={"x": "EJI Metric", "y": "RPL Value"},
            title="EJI Metrics — New Mexico"
        ), use_container_width=True)

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
