import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.subheader("Population Exposure to Urban Heat")
data = {
    "Zone": ["A", "B", "C", "D", "E"],
    "Population": [5000, 12000, 8000, 3000, 15000],
    "Avg_LST": [34, 38, 36, 32, 40]  
}
df = pd.DataFrame(data)
df["Exposure_Index"] = df["Population"] * df["Avg_LST"]
st.write("This chart shows which zones have the highest combined heat and population exposure.")
fig, ax = plt.subplots()
ax.bar(df["Zone"], df["Exposure_Index"], color="tomato")
ax.set_xlabel("City Zone")
ax.set_ylabel("Heat Exposure Index")
ax.set_title("Population Exposure to Urban Heat")
st.pyplot(fig)
st.dataframe(df)
