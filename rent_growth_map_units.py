import pandas as pd
import folium
import branca.colormap as cm
from folium import FeatureGroup

# Load and clean the data
file_path = "NashvilleDavidsonMurfreesboroFranklinTN - Rent Growth.csv"
df = pd.read_csv(file_path, skiprows=3)

# Extract and rename relevant columns
df = df[['Name', 'Latitude', 'Longitude', '5 Years', '3 Years ', '1 Year', 'Total Units']].copy()
df.columns = ['Name', 'Latitude', 'Longitude', '5Y', '3Y', '1Y', 'Units']

# Convert percentage strings to numeric
for col in ['5Y', '3Y', '1Y']:
    df[col] = df[col].astype(str).str.replace('%', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Units'] = pd.to_numeric(df['Units'], errors='coerce')

# Drop rows with missing values
df.dropna(subset=['Latitude', 'Longitude', '5Y', '3Y', '1Y', 'Units'], inplace=True)

# Normalize unit size for radius (range: 4 to 20)
unit_min = df['Units'].min()
unit_max = df['Units'].max()
df['Radius'] = df['Units'].apply(lambda x: 4 + (16 * (x - unit_min) / (unit_max - unit_min)))

# Define base map
nashville_coords = [36.1627, -86.7816]
base_map = folium.Map(location=nashville_coords, zoom_start=10, tiles="OpenStreetMap")

# Create colormaps for each growth metric
color_1y = cm.linear.Greens_09.scale(df['1Y'].min(), df['1Y'].max())
color_3y = cm.linear.Blues_09.scale(df['3Y'].min(), df['3Y'].max())
color_5y = cm.linear.Reds_09.scale(df['5Y'].min(), df['5Y'].max())

# Layer for 1-Year Growth
layer_1y = FeatureGroup(name="1-Year Rent Growth", show=True)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Radius'],
        color=color_1y(row['1Y']),
        fill=True,
        fill_opacity=0.8,
        tooltip=f"{row['Name']}<br>1-Year Growth: {row['1Y']}%<br>Units: {int(row['Units'])}"
    ).add_to(layer_1y)
layer_1y.add_to(base_map)

# Layer for 3-Year Growth
layer_3y = FeatureGroup(name="3-Year Rent Growth", show=False)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Radius'],
        color=color_3y(row['3Y']),
        fill=True,
        fill_opacity=0.8,
        tooltip=f"{row['Name']}<br>3-Year Growth: {row['3Y']}%<br>Units: {int(row['Units'])}"
    ).add_to(layer_3y)
layer_3y.add_to(base_map)

# Layer for 5-Year Growth
layer_5y = FeatureGroup(name="5-Year Rent Growth", show=False)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Radius'],
        color=color_5y(row['5Y']),
        fill=True,
        fill_opacity=0.8,
        tooltip=f"{row['Name']}<br>5-Year Growth: {row['5Y']}%<br>Units: {int(row['Units'])}"
    ).add_to(layer_5y)
layer_5y.add_to(base_map)

# Add layer toggle and save
folium.LayerControl(collapsed=False).add_to(base_map)
base_map.save("nashville_rent_growth_scaled_by_units.html")
