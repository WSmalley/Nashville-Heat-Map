import pandas as pd
import folium
from folium.plugins import HeatMap

# Load your data
df = pd.read_csv("NashvilleDavidsonMurfreesboroFranklinTN - Rent Growthclean.csv", skiprows=3)

# Clean and prepare rent growth column (choose 1 Year as an example)
rent_growth_col = df.columns[-1]  # Assumes last column is '1 Year'
df[rent_growth_col] = (
    df[rent_growth_col]
    .astype(str)
    .str.replace('%', '')
    .str.strip()
    .replace('', '0')
    .astype(float)
)

# Ensure latitude and longitude columns exist
# Replace 'Latitude' and 'Longitude' with actual column names if needed
lat_col = 'Latitude'
lon_col = 'Longitude'

# Drop rows without valid coordinates
df = df.dropna(subset=[lat_col, lon_col])

# Prepare data for HeatMap: [lat, lon, weight]
heat_data = [
    [row[lat_col], row[lon_col], row[rent_growth_col]]
    for _, row in df.iterrows()
    if row[rent_growth_col] > 0  # Optional: only positive growth
]

# Create map centered on Nashville
m = folium.Map(location=[36.1627, -86.7816], zoom_start=10)

# Add heatmap layer
HeatMap(heat_data, radius=12, max_zoom=16).add_to(m)

# Save map to HTML
m.save("rent_growth_heatmap.html")