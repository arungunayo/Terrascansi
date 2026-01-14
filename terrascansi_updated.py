import streamlit as st
from pathlib import Path
import folium
from streamlit_folium import st_folium
import pandas as pd
import ee
import folium
from streamlit_folium import st_folium
import geemap.foliumap as geemap
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json
st.set_page_config(page_title="Terrascansi", layout="wide")
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #2E8B57;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            margin-bottom: 30px;
            color: #444;
        }
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 40px;
        }
        .nav-buttons a {
            background-color: #e6f2ec;
            color: #2E8B57;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            font-size: 16px;
        }
        .nav-buttons a:hover {
            background-color: #cce5d6;
        }
        </style>
        <div class='title'>🌱Terrascansi — Urban Green Space Intelligence</div>
        <div class='subtitle'>Empowering urban planners and citizens to combat heat inequality through data-driven insights</div>
        """, unsafe_allow_html=True)


# Navigation buttons using session state
if "page" not in st.session_state:
    st.session_state.page = "Urban Heat Island"

st.markdown("""
    <style>
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .nav-buttons button {
            background-color: #e6f2ec;
            color: #2E8B57;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            font-size: 16px;
            border: none;
        }
        .nav-buttons button:hover {
            background-color: #cce5d6;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🌱 Terrascansi — Urban Green Space Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Empowering urban planners and citizens to combat heat inequality through data-driven insights</h4>", unsafe_allow_html=True)

# Button layout
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Urban Heat Island"):
        st.session_state.page = "Urban Heat Island"
with col2:
    if st.button("LST Map"):
        st.session_state.page = "LST Map"
with col3:
    if st.button("Data Upload"):
        st.session_state.page = "Data Upload"
with col4:
    if st.button("Vegetation"):
        st.session_state.page = "Vegetation"
with col5:
    if st.button("Recommendations"):
        st.session_state.page = "Recommendations"

if st.session_state.page == "Urban Heat Island":
    st.subheader("Detect heat, measure vegetation, and prioritize greening interventions")
    st.write(
        "Urban heat is not just a climate issue — it’s a social one. Across cities like Delhi, temperature disparities between neighborhoods are growing more severe, driven by unequal access to vegetation, poor infrastructure, and rapid urbanization. While some areas benefit from tree-lined streets and green parks, others endure blistering heat with little relief. These disparities aren’t random — they reflect deeper patterns of inequality. Terrascansi is a data-driven dashboard designed to expose and address this imbalance")
    if st.button("Explore Map", type="primary", width=250):
        st.info("Now open the sidebar and click **LST Map** to explore the interactive map.")
    APP_DIR = Path(__file__).parent  # my_app
    image_path = APP_DIR / "images" / "earth_on_fire.webp"

    st.image(
        image_path,
        caption="Earth On Fire",
        width=400

    )
    st.write(
        "Our mission is simple: to empower planners, researchers, and citizens with actionable insights into urban heat and vegetation coverage. Using satellite-derived data like Land Surface Temperature (LST) and NDVI (Normalized Difference Vegetation Index), EquiHeat visualizes where heat stress is highest and where green infrastructure is lacking. The platform is built to be intuitive, interactive, and scalable — whether you're analyzing one ward or an entire city.")
    st.write(
        "What sets EquiHeat apart is its focus on thermal justice — the idea that cooling resources should be distributed equitably. We don’t just show where it’s hot; we show why it’s hot, and what can be done about it. Our dashboard lets users upload their own CSV or GeoTIFF files, explore live maps, and receive ward-level recommendations for rooftop greening, tree planting, and policy interventions.")
    st.write(
        "This isn’t just a technical tool — it’s a storytelling engine. Investors and policymakers can use EquiHeat to identify high-risk zones, simulate cooling interventions, and prioritize funding where it’s needed most. The interface is designed for clarity and impact, with thematic color palettes, interactive layers, and per-page customization that makes each insight visually compelling.")
    st.write(
        "We believe that data should drive decisions — but only when it’s accessible. That’s why EquiHeat is built with open-source tools like Streamlit, Folium, and GeoPandas, making it affordable and adaptable for NGOs, municipalities, and academic researchers. The dashboard supports multiple formats, including CSV and GeoTIFF, and can be extended to include real-time sensor data, citizen feedback, or AI-based predictions.")
    st.write(
        "In a world facing rising temperatures and shrinking budgets, EquiHeat offers a pragmatic path forward. It’s not just about planting trees — it’s about planting them where they matter most. By combining geospatial analysis with equity-focused design, we aim to make cities cooler, fairer, and more resilient.")
    st.write(
        "Whether you're an investor looking to support climate innovation, a planner seeking data clarity, or a citizen advocating for your neighborhood, EquiHeat is your ally in the fight for thermal justice.")
    subtopic = st.selectbox("Explore More", [
        "Overview",
        "Population Exposure",
        "Vegetation Correlation",
        "Priority Zones"
    ])
    if subtopic == "Overview":
        st.subheader("Urban Heat Island Overview")
        st.write(
            "Urban heat islands are areas, such as cities, that experience significantly higher temperatures than their surrounding rural areas. This phenomenon occurs due to several factors:Surface Absorption: Dark surfaces like asphalt and concrete absorb more sunlight and heat, leading to warmer temperatures. Reduced Ventilation: Tall buildings and narrow streets can block wind flow, preventing natural cooling. Human Activities: Energy consumption and industrial processes contribute to heat emissions, further increasing temperatures. Urban Geometry: The layout of cities can create urban canyons that trap heat. Overall, urban heat islands pose significant challenges to urban environments, affecting air quality and human health.")
    elif subtopic == "Population Exposure":
        exec(open("urban_heat_subpages/Population_Exposure.py").read())
    elif subtopic == "Vegetation Correlation":
        exec(open("urban_heat_subpages/Vegetation_Correlation.py").read())
    elif subtopic == "Priority Zones":
        exec(open("urban_heat_subpages/Priority_Zones.py").read())
elif st.session_state.page == "LST Map":
    st.title("LST Map")
    import streamlit as st

    st.title("Land Surface Temperature (LST) Analysis")
    st.header("🌡️ What is LST?")
    st.write("""
           Land Surface Temperature (LST) measures how hot the ground surface is, 
           derived from thermal infrared bands of satellites like Landsat-8/9.
           Unlike air temperature, LST directly reflects how surfaces such as 
           concrete, asphalt, and vegetation absorb and radiate heat.
           """)
    st.header("Overview of LST in Urban Heat Islands")
    st.write("""
           Urban Heat Islands (UHIs) form when built-up areas trap heat, raising LST compared to rural surroundings.
           - **High LST zones** → hotspots where vegetation is scarce.  
           - **Low LST zones** → cooler areas with trees, parks, or water bodies.  
           - **Correlation** → Higher NDVI (healthy vegetation) usually lowers LST.
           """)
    st.header("LST Map ")
    m = folium.Map(location=[28.669081, 77.430412], zoom_start=10)
    st_folium(m, width=700, height=500)
    import streamlit as st


    # ---------------------------------
    # Streamlit config
    # ---------------------------------
    st.set_page_config(layout="wide")
    st.title("Green Spaces Analysis – Ghaziabad")

    # ---------------------------------
    # Initialize Earth Engine
    # ---------------------------------
    ee.Initialize(project='My ')

    # ---------------------------------
    # City boundary
    # ---------------------------------
    city = (
        ee.FeatureCollection("FAO/GAUL/2015/level2")
        .filter(ee.Filter.eq("ADM2_NAME", "Ghaziabad"))
    )

    # ---------------------------------
    # Sentinel-2 ImageCollection
    # ---------------------------------
    sentinel = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(city)
        .filterDate("2024-01-01", "2026-01-01")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .median()
    )

    # ---------------------------------
    # NDVI
    # ---------------------------------
    ndvi = sentinel.normalizedDifference(["B8", "B4"]).rename("NDVI")

    # ---------------------------------
    # NDVI threshold for green spaces
    # ---------------------------------
    green_spaces = ndvi.gt(0.3).selfMask()

    # ---------------------------------
    # Convert raster → vector polygons
    # ---------------------------------
    zones = green_spaces.reduceToVectors(
        geometry=city.geometry(),
        scale=10,
        geometryType="polygon",
        reducer=ee.Reducer.countEvery(),
        maxPixels=1e10
    )


    # ---------------------------------
    # Add area + centroid
    # ---------------------------------
    def add_props(f):
        geom = f.geometry()
        centroid = geom.centroid(maxError=30)
        return f.set({
            "area_ha": geom.area(maxError=30).divide(10000),
            "centroid_lon": centroid.coordinates().get(0),
            "centroid_lat": centroid.coordinates().get(1)
        })


    zones_with_props = zones.map(add_props)

    # ---------------------------------
    # Map
    # ---------------------------------
    m = folium.Map(location=[28.67, 77.42], zoom_start=10)

    # NDVI layer
    geemap.ee_tile_layer(
        ndvi,
        {"min": 0, "max": 1, "palette": ["white", "yellow", "green"]},
        "NDVI"
    ).add_to(m)

    # Green spaces layer
    geemap.ee_tile_layer(
        green_spaces,
        {"palette": ["006400"]},
        "Green Spaces"
    ).add_to(m)

    # Boundary
    geemap.ee_tile_layer(
        city.style(**{"color": "red", "fillColor": "00000000"}),
        {},
        "Ghaziabad Boundary"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # ---------------------------------
    # Display map in Streamlit
    # ---------------------------------
    st_folium(m, width=1300, height=650)

    st.header("How LST Helps in UHI Analysis")
    st.write("""
           - **Pinpoints hotspots**: Identifies areas where heat stress is highest.  
           - **Guides greening**: Shows where vegetation buffers or parks are most needed.  
           - **Supports health & policy**: Helps planners reduce heat exposure for vulnerable populations.
           """)
    # st.header("⚡ Why Terrascansi is Different")
    # comparison = pd.DataFrame({
    #     "Old Heavy Tools": [
    #         "Show vegetation only",
    #         "Static maps",
    #         "Analyst-centric",
    #         "Retrospective (past data only)",
    #         "Heavy, complex platforms"
    #     ],
    #     "Terrascansi": [
    #         "Suggest new vegetation strategies",
    #         "Interactive decision-support",
    #         "Accessible to planners, NGOs, communities",
    #         "Forward-looking (predictive + recommendations)",
    #         "Lightweight, Streamlit-based, easy to use"
    #     ]
    # })
    # st.table(comparison)
elif st.session_state.page == "Data Upload":
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFF8F0; }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title(" Data Upload & Feature Extraction")
    st.header("🌐 Data Sources")
    st.write("""
          Terrascansi uses open satellite data to monitor vegetation and heat stress:
          - **Sentinel‑2 imagery** → High‑resolution vegetation data for NDVI.  
          - **Landsat‑8/9 thermal bands** → Land Surface Temperature (LST).  
          - **Multi‑temporal datasets** → Seasonal and historical trend analysis.
          """)
    st.info("These sources are free, global, and updated regularly — making Terrascansi scalable and future‑ready.")
    st.header("Upload Your Own Data")
    uploaded_file = st.file_uploader("Upload satellite data (CSV or GeoTIFF)", type=["csv", "tif", "tiff"])
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df.head())
        else:
            st.write("GeoTIFF uploaded. Raster visualization will be processed in future integration.")
    st.header("🔍 Feature Extraction")
    st.write("""
          From raw satellite data, Terrascansi extracts key indicators:
          - **NDVI (Normalized Difference Vegetation Index)** → Vegetation density and health.  
          - **LST (Land Surface Temperature)** → Detects Urban Heat Islands.  
          - **Change Detection** → Highlights vegetation degradation over time.
          """)
    data = {
        "Date": ["2020", "2021", "2022", "2023", "2024"],
        "NDVI": [0.45, 0.42, 0.40, 0.38, 0.35]
    }
    df = pd.DataFrame(data)
    st.subheader(" NDVI Trend Example")
    st.line_chart(df.set_index("Date"))
    st.header("Sample Map Preview")
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)  # Example: Delhi coords
    folium.CircleMarker(
        location=[28.61, 77.23],
        radius=15,
        color="green",
        fill=True,
        fill_opacity=0.6,
        popup="High NDVI (Healthy Vegetation)"
    ).add_to(m)
    folium.CircleMarker(
        location=[28.65, 77.18],
        radius=15,
        color="red",
        fill=True,
        fill_opacity=0.6,
        popup="Low NDVI (Vegetation Loss)"
    ).add_to(m)
    st_folium(m, width=700, height=500)
    # st.header("⚡ Why Terrascansi is Different at This Stage")
    # comparison = pd.DataFrame({
    #     "Traditional Tools": [
    #         "Require manual preprocessing",
    #         "Static vegetation maps",
    #         "Limited temporal analysis"
    #     ],
    #     "Terrascansi": [
    #         "Automated NDVI & LST extraction",
    #         "Interactive maps with overlays",
    #         "Multi‑year trend detection"
    #     ]
    # })
    # st.table(comparison)

elif st.session_state.page == "Vegetation":
    st.title("Zone Analysis & Vegetation")
    st.header(" Why Zone Analysis?")
    st.write("""
           Terrascansi divides the urban area into grid-based zones.  
           Each zone is analyzed for:
           - **High LST (Land Surface Temperature)**  
           - **Low or declining NDVI (vegetation health)**  
           - **Historical vegetation loss**  

           This produces a **Priority Index** that ranks zones by urgency for greening interventions.
           """)

    st.header(" Example Zone Data")
    data = {
        "Zone": ["A", "B", "C", "D", "E"],
        "Avg_LST": [38, 36, 40, 33, 37],
        "NDVI": [0.25, 0.45, 0.20, 0.55, 0.30],
        "Historical_Loss": [0.15, 0.10, 0.20, 0.05, 0.18]
    }
    df = pd.DataFrame(data)
    df["Priority_Index"] = df["Avg_LST"] * (1 - df["NDVI"]) + (df["Historical_Loss"] * 100)
    df_sorted = df.sort_values("Priority_Index", ascending=False)
    st.dataframe(df_sorted)
    st.success("Zones with the highest Priority Index should be targeted first for greening interventions.")
    st.header(" Priority Zones Map")
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=10)
    colors = ["red", "orange", "yellow", "green", "blue"]
    for i, row in df_sorted.iterrows():
        folium.CircleMarker(
            location=[28.60 + i * 0.02, 77.20 + i * 0.01],
            radius=15,
            color=colors[i % len(colors)],
            fill=True,
            fill_opacity=0.6,
            popup=f"Zone {row['Zone']} | Priority Index: {row['Priority_Index']:.2f}"
        ).add_to(m)
    st_folium(m, width=700, height=500)
    # st.header("⚡ Why Terrascansi is Different at Zone Analysis Stage")
    # comparison = pd.DataFrame({
    #     "Traditional Tools": [
    #         "Show raw maps only",
    #         "No prioritization",
    #         "Reactive after crisis"
    #     ],
    #     "Terrascansi": [
    #         "Ranks zones by urgency",
    #         "Provides actionable recommendations",
    #         "Supports proactive planning"
    #     ]
    # })
    # st.table(comparison)

elif st.session_state.page == "Recommendations":
    st.title("Recommendations")
    st.header("Why Recommendations Matter")
    st.write("""
          After identifying priority zones, Terrascansi suggests practical greening strategies 
          to reduce heat stress and improve urban resilience. These recommendations are tailored 
          to each zone’s conditions and urgency.
          """)
    st.header("🌱 Recommended Strategies")
    st.write("""
          - **New Parks & Green Corridors** → Cool down high‑LST zones.  
          - **Vegetation Buffers Along Roads** → Reduce heat and pollution exposure.  
          - **Rooftop & Vertical Greening** → Add greenery in dense built‑up areas.  
          - **Water Bodies & Reflective Surfaces** → Lower surface heat retention.  
          - **Community‑Driven Planting Programs** → Engage citizens in sustainable action.
          """)
    st.header("Example Recommendation Matrix")
    data = {
        "Zone": ["A", "B", "C", "D", "E"],
        "Priority_Index": [72.5, 65.3, 80.1, 50.2, 68.7],
        "Suggested_Action": [
            "New Park Development",
            "Vegetation Buffers",
            "Rooftop Greening",
            "Community Planting",
            "Water Body Restoration"
        ],
        "Expected_Impact": [
            "Reduce LST by 2‑3°C",
            "Lower roadside heat & AQI",
            "Cool dense urban blocks",
            "Increase vegetation cover",
            "Improve micro‑climate"
        ]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)
    st.success(
        "These strategies help planners move from analysis to action, ensuring cooler, healthier, and more sustainable cities.")
    # st.header("⚡ Why Terrascansi is Different at Recommendation Stage")
    # comparison = pd.DataFrame({
    #     "Traditional Tools": [
    #         "Stop at visualization",
    #         "Leave action to external experts",
    #         "No citizen engagement"
    #     ],
    #     "Terrascansi": [
    #         "Suggests actionable greening strategies",
    #         "Integrates analysis with decision support",
    #         "Encourages community participation"
    #     ]
    # })
    # st.table(comparison)

#Hide the sidebar
st.markdown("""
   <style>
   [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)


