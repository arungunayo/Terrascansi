import streamlit as st
import pandas as pd
st.subheader("Priority Zones for Intervention")
data = {
    "Zone": ["A", "B", "C", "D", "E"],
    "Avg_LST": [38, 36, 40, 33, 37],   # Land Surface Temperature °C
    "NDVI": [0.25, 0.45, 0.20, 0.55, 0.30],  # Vegetation health
    "Historical_Loss": [0.15, 0.10, 0.20, 0.05, 0.18]  # Vegetation loss fraction
}
df = pd.DataFrame(data)
df["Priority_Index"] = df["Avg_LST"] * (1 - df["NDVI"]) + (df["Historical_Loss"] * 100)
df_sorted = df.sort_values("Priority_Index", ascending=False)
st.write("Zones ranked by urgency for greening interventions:")
st.dataframe(df_sorted)
st.success("Top priority zones should be targeted for new parks, vegetation buffers, or rooftop greening.")
