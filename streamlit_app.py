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
Use the dropdowns below to explore data for **New Mexico** or specific **counties**, and optionally **compare datasets**.
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

# --- Prep data ---
metrics = ["Mean_EJI", "Mean_EBM", "Mean_SVM", "Mean_HVM", "Mean_CBM", "Mean_EJI_CBM"]

counties = sorted(county_df["County"].dropna().unique())
states = sorted(state_df["State"].dropna().unique())
parameter1 = ["New Mexico", "County"]

# --- Main selection ---
selected_parameter = st.selectbox("View EJI data for:", parameter1)
st.write(f"**You selected:** {selected_parameter}")

# Helper function for plots
def plot_metrics(title, values, labels):
    fig = px.bar(
        x=labels,
        y=values,
        labels={"x": "EJI Metric", "y": "Score"},
        title=title
    )
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
        plot_metrics(f"EJI Metrics — {selected_county}", county_values.values, metrics)

        # --- Comparison Option ---
        compare = st.radio("Would you like to compare with another dataset?", ["No", "Yes"])
        if compare == "Yes":
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"### {selected_county}")
                plot_metrics(f"{selected_county}", county_values.values, metrics)

            with col2:
                compare_type = st.radio("Compare with:", ["State", "County"])
                if compare_type == "State":
                    comp_state = st.selectbox("Select state:", states)
                    comp_row = state_df[state_df["State"] == comp_state]
                    if not comp_row.empty:
                        comp_values = comp_row[metrics].iloc[0]
                        st.write(f"### {comp_state}")
                        plot_metrics(f"{comp_state}", comp_values.values, metrics)
                else:
                    comp_county = st.selectbox("Select county:", [c for c in counties if c != selected_county])
                    comp_row = county_df[county_df["County"] == comp_county]
                    if not comp_row.empty:
                        comp_values = comp_row[metrics].iloc[0]
                        st.write(f"### {comp_county}")
                        plot_metrics(f"{comp_county}", comp_values.values, metrics)

elif selected_parameter == "New Mexico":
    nm_row = state_df[state_df["State"].str.strip().str.lower() == "new mexico"]

    if nm_row.empty:
        st.warning("No New Mexico data found in the state file.")
    else:
        st.subheader("📋 New Mexico Statewide EJI Scores")
        st.dataframe(nm_row, hide_index=True)

        nm_values = nm_row[metrics].iloc[0]
        plot_metrics("EJI Metrics — New Mexico", nm_values.values, metrics)

        # --- Comparison Option ---
        compare = st.radio("Would you like to compare with another dataset?", ["No", "Yes"])
        if compare == "Yes":
            col1, col2 = st.columns(2)
            with col1:
                st.write("### New Mexico")
                plot_metrics("New Mexico", nm_values.values, metrics)

            with col2:
                compare_type = st.radio("Compare with:", ["State", "County"])
                if compare_type == "State":
                    comp_state = st.selectbox("Select state:", [s for s in states if s.lower() != "new mexico"])
                    comp_row = state_df[state_df["State"] == comp_state]
                    if not comp_row.empty:
                        comp_values = comp_row[metrics].iloc[0]
                        st.write(f"### {comp_state}")
                        plot_metrics(f"{comp_state}", comp_values.values, metrics)
                else:
                    comp_county = st.selectbox("Select county:", counties)
                    comp_row = county_df[county_df["County"] == comp_county]
                    if not comp_row.empty:
                        comp_values = comp_row[metrics].iloc[0]
                        st.write(f"### {comp_county}")
                        plot_metrics(f"{comp_county}", comp_values.values, metrics)

# --- Footer ---
st.divider()
st.caption("Data Source: CDC Environmental Justice Index | Visualization by Riley Cochrell")
