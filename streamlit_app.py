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
Use the dropdowns below to explore data for **New Mexico** or specific **counties**.
""")

# --- Load data from GitHub ---
@st.cache_data
def load_data():
    state_url = "https://github.com/rileycochrell/blank-app-1/raw/refs/heads/main/EJI_StateAverages_RPL.csv"
    county_url = "https://github.com/rileycochrell/blank-app-1/raw/refs/heads/main/EJI_NewMexico_CountyMeans.csv"

    try:
        state_df = pd.read_csv(state_url)
        county_df = pd.read_csv(county_url)

        # 🧹 Clean up any extra columns or rows
        if "Count" in state_df.columns:
            state_df = state_df[state_df["State"] != "Count"]
        if "Count" in county_df.columns:
            county_df = county_df[county_df["County"] != "Count"]

        # Remove index column (just display clean)
        state_df = state_df.reset_index(drop=True)
        county_df = county_df.reset_index(drop=True)

        return state_df, county_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

state_df, county_df = load_data()

if state_df is None or county_df is None:
    st.stop()

# --- Define dropdown options ---
counties = sorted(county_df["County"].dropna().unique())
parameter1 = ["New Mexico", "County"]

# --- Selection ---
selected_parameter = st.selectbox("View EJI data for:", parameter1)
st.write(f"**You selected:** {selected_parameter}")

# --- Define the metric columns actually in your data ---
metrics = ["Mean_EJI", "Mean_EBM", "Mean_SVM", "Mean_HVM", "Mean_CBM", "Mean_EJI_CBM"]

# --- Display data and visuals ---
if selected_parameter == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["County"] == selected_county]

    if subset.empty:
        st.warning(f"No data found for {selected_county}.")
    else:
        st.success(f"Displaying data for **{selected_county}**.")
        st.subheader(f"📋 EJI Data for {selected_county}")
        st.dataframe(subset, hide_index=True)

        # --- Bar chart ---
        county_means = subset[metrics].mean(numeric_only=True)
        fig = px.bar(
            x=metrics,
            y=county_means.values,
            labels={"x": "EJI Metric", "y": "Mean Value"},
            title=f"EJI Metrics for {selected_county}"
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.success("Displaying statewide averages for **New Mexico**.")

    st.subheader("📋 New Mexico Statewide Averages")
    st.dataframe(state_df, hide_index=True)

    nm_means = state_df[metrics].mean(numeric_only=True)
    fig = px.bar(
        x=metrics,
        y=nm_means.values,
        labels={"x": "EJI Metric", "y": "Mean Value"},
        title="EJI Metrics — New Mexico Statewide Averages"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
