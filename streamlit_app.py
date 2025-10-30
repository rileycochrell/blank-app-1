import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="Environmental Justice Index (EJI) — New Mexico", layout="wide")

# --- Title and description ---
st.title("🌎 Environmental Justice Index Visualization (New Mexico)")
st.write("""
The **Environmental Justice Index (EJI)** measures cumulative environmental, social, and health burdens in communities 
relative to others across the U.S.  
Use the dropdowns below to explore data for **New Mexico** or specific **counties** and compare them to **U.S. averages**.
""")

# --- Load data from GitHub ---
@st.cache_data
def load_data():
    state_url = "https://raw.githubusercontent.com/rileycochrell/idktrying/main/NewMexicoEJI.csv"
    county_url = "https://github.com/rileycochrell/blank-app-1/raw/refs/heads/main/EJI_NewMexico_CountyMeans.csv"
    usa_url = "https://raw.githubusercontent.com/rileycochrell/idktrying/main/USA_EJI.csv"
    
    try:
        state_df = pd.read_csv(state_url)
        county_df = pd.read_csv(county_url)
        usa_df = pd.read_csv(usa_url)
        return state_df, county_df, usa_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

state_df, county_df, usa_df = load_data()

if state_df is None:
    st.stop()

# --- Define dropdown options ---
counties = sorted(county_df["COUNTY"].unique())
parameter1 = ["New Mexico", "County"]

# --- Selection ---
selected_parameter = st.selectbox("View EJI data for:", parameter1)
st.write(f"**You selected:** {selected_parameter} vs United States")

# --- Display data and visuals ---
if selected_parameter == "County":
    selected_county = st.selectbox("Select a New Mexico County:", counties)
    subset = county_df[county_df["COUNTY"] == selected_county]
    st.success(f"Displaying data for **{selected_county}**.")

    # --- Table view ---
    st.subheader(f"📋 EJI Data for {selected_county}")
    st.dataframe(subset)

    # --- Comparison plot ---
    metrics = ["mean_RPL_EJI", "mean_RPL_EBM", "mean_RPL_SVM", "mean_RPL_HVM", "mean_RPL_CBM"]
    nm_means = subset[metrics].mean()
    usa_means = usa_df[metrics].mean()

    compare_df = pd.DataFrame({
        "Metric": metrics,
        f"{selected_county}": nm_means.values,
        "U.S. Average": usa_means.values
    })

    fig = px.bar(compare_df, x="Metric", y=[f"{selected_county}", "U.S. Average"],
                 barmode="group", title=f"EJI Comparison: {selected_county} vs U.S. Average")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.success("Displaying statewide averages for **New Mexico**.")

    # --- Statewide table ---
    st.subheader("📋 New Mexico EJI Statewide Averages")
    st.dataframe(state_df)

    # --- Comparison plot ---
    metrics = ["mean_RPL_EJI", "mean_RPL_EBM", "mean_RPL_SVM", "mean_RPL_HVM", "mean_RPL_CBM"]
    nm_means = state_df[metrics].mean()
    usa_means = usa_df[metrics].mean()

    compare_df = pd.DataFrame({
        "Metric": metrics,
        "New Mexico": nm_means.values,
        "U.S. Average": usa_means.values
    })

    fig = px.bar(compare_df, x="Metric", y=["New Mexico", "U.S. Average"],
                 barmode="group", title="EJI Comparison: New Mexico vs U.S. Average")
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
