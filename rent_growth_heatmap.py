import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv("NashvilleDavidsonMurfreesboroFranklinTN - Rent Growthclean.csv", skiprows=3)

# Select columns: Name, Address, Submarket, County, and the last three columns
cols = ["Name", "Address", "Submarket", "County"]
# The last three columns are usually: '5 Years', '3 Years ', '1 Year'
rent_growth_cols = df.columns[-3:]

df_heatmap = df[cols + list(rent_growth_cols)].copy()

# Clean rent growth values (remove % and convert to float)
for col in rent_growth_cols:
    df_heatmap[col] = df_heatmap[col].str.replace('%','').str.replace(' ','').replace('', '0').astype(float)

# Choose which metric to display (e.g., 1 Year)
metric = '1 Year'
df_heatmap['Heat'] = df_heatmap[metric]

# Option 1: Aggregate by Submarket
submarket_heat = df_heatmap.groupby("Submarket")['Heat'].mean().reset_index()

# Plot
plt.figure(figsize=(12,6))
heatmap_data = submarket_heat.pivot_table(index="Submarket", values="Heat")
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", center=0)
plt.title(f"Rent Growth Heatmap by Submarket ({metric})")
plt.ylabel("Submarket")
plt.xlabel("Rent Growth (%)")
plt.tight_layout()
plt.show()