import streamlit as st
import plotly.express as px
import pandas as pd

# Example datasets (replace these with your actual data)
df1 = pd.DataFrame({
    "RPL_EJI": [0.78],
    "RPL_SI": [0.61],
    "RPL_HVM": [0.84],
    "RPL_EBM": [0.57]
}, index=["Dataset 1"])

df2 = pd.DataFrame({
    "RPL_EJI": [0.81],
    "RPL_SI": [0.65],
    "RPL_HVM": [0.79],
    "RPL_EBM": [0.63]
}, index=["Dataset 2"])

metrics = ["RPL_EJI", "RPL_SI", "RPL_HVM", "RPL_EBM"]

# Define pretty labels
pretty = {
    "RPL_EJI": "Overall EJI",
    "RPL_SI": "Socioeconomic Indicators",
    "RPL_HVM": "Health Vulnerability",
    "RPL_EBM": "Environmental Burden"
}

dataset1_colors = {
    "RPL_EJI": "#1f77b4",
    "RPL_SI": "#ff7f0e",
    "RPL_HVM": "#2ca02c",
    "RPL_EBM": "#d62728"
}

# First dataset bar chart (single dataset)
st.subheader("Environmental Justice Index Metric Breakdown — Dataset 1")

nm_row = df1
nm_values = nm_row[metrics].iloc[0]

fig1 = px.bar(
    x=[pretty.get(m, m) for m in metrics],
    y=nm_values.values,
    color=metrics,
    color_discrete_map=dataset1_colors,
    text=[f"{v:.2f}" for v in nm_values.values],
)

fig1.update_traces(
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="white", size=12),
)

fig1.update_layout(
    title=dict(
        text="Environmental Justice Index Metric Breakdown",
        font=dict(color="black", size=18)
    ),
    xaxis_title=dict(text="Percentile Rank Value", font=dict(color="black", size=14)),
    yaxis_title=dict(text="Environmental Justice Index Metric", font=dict(color="black", size=14)),
    xaxis_tickangle=-45,
    plot_bgcolor="white",
    showlegend=False,
)

st.plotly_chart(fig1, use_container_width=True)

# Comparison chart (two datasets)
st.subheader("Environmental Justice Index Comparison")

comp_df = pd.DataFrame({
    "Metric": [pretty.get(m, m) for m in metrics for _ in range(2)],
    "Dataset": ["Dataset 1"] * len(metrics) + ["Dataset 2"] * len(metrics),
    "Value": list(df1.iloc[0][metrics].values) + list(df2.iloc[0][metrics].values)
})

fig2 = px.bar(
    comp_df,
    x="Value",
    y="Metric",
    color="Dataset",
    orientation="h",
    barmode="group",
    text=comp_df["Dataset"],
    color_discrete_sequence=["#1f77b4", "#9467bd"]
)

fig2.update_traces(
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="white", size=12),
)

fig2.update_layout(
    title=dict(
        text="Environmental Justice Index Comparison Between Datasets",
        font=dict(color="black", size=18)
    ),
    xaxis_title=dict(text="Percentile Rank Value", font=dict(color="black", size=14)),
    yaxis_title=dict(text="Environmental Justice Index Metric", font=dict(color="black", size=14)),
    plot_bgcolor="white",
    showlegend=True,
)

st.plotly_chart(fig2, use_container_width=True)
