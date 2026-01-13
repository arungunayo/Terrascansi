# urban_heat_subpages/Vegetation_Correlation.py
import streamlit as st
import matplotlib.pyplot as plt
st.subheader("Vegetation vs Heat Correlation")
ndvi = [0.2, 0.3, 0.5, 0.7, 0.8]
lst = [39, 37, 34, 31, 29]  # °C
st.write("Scatter plot showing how higher NDVI (healthier vegetation) reduces land surface temperature.")
fig, ax = plt.subplots()
ax.scatter(ndvi, lst, color="green")
ax.set_xlabel("NDVI (Vegetation Health)")
ax.set_ylabel("Land Surface Temperature (°C)")
ax.set_title("NDVI vs LST Correlation")
st.pyplot(fig)
