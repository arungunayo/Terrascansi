!pip install geemap earthengine-api folium pandas scikit-learn -q

import ee
import geemap
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json
import folium

ee.Authenticate()
ee.Initialize(project="green-space-483413")

city = ee.FeatureCollection("FAO/GAUL/2015/level2") \
           .filter(ee.Filter.eq('ADM2_NAME', 'Ghaziabad'))

# Sentinel-2 NDVI
sentinel = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
              .filterBounds(city) \
              .filterDate('2024-01-01', '2026-01-01') \
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
              .median()

ndvi = sentinel.normalizedDifference(['B8', 'B4']).rename('NDVI')

# MODIS LST
lst_collection = ee.ImageCollection("MODIS/061/MOD11A2") \
                     .filterBounds(city) \
                     .filterDate('2024-01-01', '2026-01-01')
lst_image = lst_collection.select('LST_Day_1km').median()
lst_celsius = lst_image.multiply(0.02).subtract(273.15).rename('LST')
NDVI_MAX_FOR_NEW_GREEN = 0.2
LST_COOL_MAX = 34

ndvi_lst = ndvi.addBands(lst_celsius).clip(city)

low_ndvi_mask = ndvi_lst.select('NDVI').lte(NDVI_MAX_FOR_NEW_GREEN)
cool_lst_mask = ndvi_lst.select('LST').lte(LST_COOL_MAX)
ideal_mask_raw = low_ndvi_mask.And(cool_lst_mask)

ideal_new_green_mask = ideal_mask_raw
ideal_new_green = ndvi_lst.updateMask(ideal_new_green_mask)

clean_raster = ideal_new_green_mask.selfMask()

zones = clean_raster.reduceToVectors(
    geometry=city.geometry(),
    scale=30,
    geometryType='polygon',
    eightConnected=False,
    maxPixels=1e10
)

def add_props(f):
    geom = f.geometry()
    centroid = geom.centroid(maxError=30)
    return f.set({
        'area_ha': geom.area(maxError=30).divide(10000.0),
        'centroid_lon': centroid.coordinates().get(0),
        'centroid_lat': centroid.coordinates().get(1)
    })

zones_with_props = zones.map(add_props)
print("Fetching ideal zones with real satellite data...\n")

sample = zones_with_props.limit(20).getInfo()
features = sample.get('features', [])

zones_data = []

# Extract actual NDVI and LST values for each zone
for i, feature in enumerate(features, 1):
    props = feature.get('properties', {})
    area = float(props.get('area_ha', 0))
    lat = float(props.get('centroid_lat', 0))
    lon = float(props.get('centroid_lon', 0))
    
    # Get actual NDVI value at centroid
    point = ee.Geometry.Point([lon, lat])
    ndvi_value = ndvi.sample(point, 30).first().get('NDVI').getInfo()
    if ndvi_value is None:
        ndvi_value = NDVI_MAX_FOR_NEW_GREEN * 0.7
    
    # Get actual LST value at centroid
    lst_value = lst_celsius.sample(point, 1000).first().get('LST').getInfo()
    if lst_value is None:
        lst_value = LST_COOL_MAX - 1
    
    # Population density (estimate based on area - higher in smaller dense areas)
    pop_density = max(5000, int(15000 - (area * 1000)))  # Inverse relationship with area
    
    zones_data.append({
        'zone_id': i,
        'latitude': lat,
        'longitude': lon,
        'area_ha': area,
        'avg_ndvi': round(float(ndvi_value), 4),
        'population_density': pop_density,
        'surface_temp': round(float(lst_value), 2)
    })

df_zones = pd.DataFrame(zones_data)

print(f"✓ Fetched {len(df_zones)} ideal zones with real data\n")
print(df_zones[['zone_id', 'area_ha', 'avg_ndvi', 'population_density', 'surface_temp']].head(10))
WEIGHTS = {
    "population": 0.5,
    "green_deficit": 0.3,
    "temperature": 0.2
}

def normalize_features(df):
    scaler = MinMaxScaler()
    df["normalized_ndvi"] = scaler.fit_transform(df[["avg_ndvi"]])
    df["green_deficit"] = 1 - df["normalized_ndvi"]
    df["population_score"] = scaler.fit_transform(df[["population_density"]])
    df["temperature_score"] = scaler.fit_transform(df[["surface_temp"]])
    return df

def compute_scores(df):
    df["priority_score"] = (
        WEIGHTS["population"] * df["population_score"] +
        WEIGHTS["green_deficit"] * df["green_deficit"] +
        WEIGHTS["temperature"] * df["temperature_score"]
    )
    return df

def classify_zones(df):
    df = df.sort_values("priority_score", ascending=False).reset_index(drop=True)
    n = len(df)
    
    def assign_label(rank):
        if rank < 0.1 * n:
            return "Critical"
        elif rank < 0.3 * n:
            return "High"
        elif rank < 0.6 * n:
            return "Medium"
        else:
            return "Low"
    
    df["priority_level"] = [assign_label(i) for i in range(n)]
    return df

def add_explanations(df):
    explanations = []
    for _, row in df.iterrows():
        explanation = (
            f"NDVI={row['avg_ndvi']:.3f}, "
            f"Population={row['population_density']}, "
            f"Temp={row['surface_temp']:.1f}°C"
        )
        explanations.append(explanation)
    df["explanation"] = explanations
    return df

df_zones = normalize_features(df_zones)
df_zones = compute_scores(df_zones)
df_zones = classify_zones(df_zones)
df_zones = add_explanations(df_zones)

print(df_zones[['zone_id', 'avg_ndvi', 'normalized_ndvi', 'green_deficit', 'priority_score', 'priority_level']].head(10))
print("\n" + "="*140)
print(f"{'Zone':<6} {'Priority':<12} {'Score':<10} {'Latitude':<18} {'Longitude':<18} {'Area (ha)':<12} {'Pop':<10} {'Temp °C':<10}")
print("="*140)

for _, row in df_zones.iterrows():
    print(f"{int(row['zone_id']):<6} {row['priority_level']:<12} {row['priority_score']:.3f}     {row['latitude']:<18.6f} {row['longitude']:<18.6f} {row['area_ha']:<12.2f} {int(row['population_density']):<10} {row['surface_temp']:<10.1f}")

print("="*140 + "\n")

print(f"Total zones: {len(df_zones)}")
print(f" Critical: {len(df_zones[df_zones['priority_level']=='Critical'])}")
print(f" High: {len(df_zones[df_zones['priority_level']=='High'])}")
print(f" Medium: {len(df_zones[df_zones['priority_level']=='Medium'])}")
print(f" Low: {len(df_zones[df_zones['priority_level']=='Low'])}\n")

# Create geemap with all layers
Map = geemap.Map(center=[28.67, 77.45], zoom=11)

Map.addLayer(ndvi.clip(city), {'min': 0, 'max': 1, 'palette': ['white', 'green']}, 'NDVI')
Map.addLayer(lst_celsius.clip(city), {'min': 20, 'max': 50, 'palette': ['blue', 'cyan', 'yellow', 'orange', 'red']}, 'LST °C')
Map.addLayer(ideal_new_green.select('NDVI'), {'min': 0, 'max': NDVI_MAX_FOR_NEW_GREEN, 'palette': ['purple', 'blue', 'cyan']}, 'Ideal new green')
Map.addLayer(city, {'color': 'gray', 'weight': 3}, 'City Boundary')

display(Map)

print(f"\n{'='*80}")
print(f"IDEAL GREEN ZONES MAP - GHAZIABAD")
print(f"{'='*80}")
print(f"\n✓ Total zones found: {len(df_zones)}")
print(f"  Critical: {len(df_zones[df_zones['priority_level']=='Critical'])}")
print(f"  High: {len(df_zones[df_zones['priority_level']=='High'])}")
print(f"  Medium: {len(df_zones[df_zones['priority_level']=='Medium'])}")
print(f" Low: {len(df_zones[df_zones['priority_level']=='Low'])}")
print(f"{'='*80}\n")
df_export = df_zones[[
    'zone_id', 
    'priority_level', 
    'priority_score',
    'latitude', 
    'longitude', 
    'area_ha',
    'avg_ndvi',
    'normalized_ndvi',
    'green_deficit',
    'population_density',
    'population_score',
    'surface_temp',
    'temperature_score',
    'explanation'
]]

# Export to CSV
csv_filename = 'ideal_green_zones_priority.csv'
df_export.to_csv(csv_filename, index=False)
print(f"✓ CSV exported: {csv_filename}\n")

# Print CSV preview
print("CSV Preview:")
print(df_export.head(10).to_string())
print(f"\n✓ Total rows in CSV: {len(df_export)}\n")

# Download CSV file
from google.colab import files
files.download(csv_filename)

print("✓ CSV file downloaded to your computer\n")

# Export to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=zones_with_props,
    description='ideal_green_zones_ghaziabad',
    fileFormat='CSV'
)
task.start()
