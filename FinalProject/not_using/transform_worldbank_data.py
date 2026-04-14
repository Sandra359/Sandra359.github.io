"""
Transform World Bank Energy Import Data from Wide to Long Format
"""
import pandas as pd
import numpy as np

# Read the World Bank data (skip metadata at top)
df_raw = pd.read_csv(
    "/Users/sandrarune/Library/CloudStorage/OneDrive-DanmarksTekniskeUniversitet/8. sem/Social dataanalyse og vis/WEEKS_ny/Sandra359.github.io/FinalProject/datasæt/energy_imports_raw.csv",
    skiprows=4  # Skip the metadata rows
)

print(f"✓ Loaded {len(df_raw)} countries/regions")
print(f"  Columns: {df_raw.columns[:10].tolist()}... and {len(df_raw.columns) - 10} more years")

# Keep only relevant columns: Country Name, Code, Indicator, and years 1990-2023
years = [str(year) for year in range(1990, 2024)]
keep_cols = ['Country Name', 'Country Code'] + years

df_subset = df_raw[keep_cols].copy()

# Reshape from wide to long format
df_long = df_subset.melt(
    id_vars=['Country Name', 'Country Code'],
    var_name='Year',
    value_name='Import_Dependency_Pct'
)

# Convert Year to integer, Import to float
df_long['Year'] = pd.to_numeric(df_long['Year'])
df_long['Import_Dependency_Pct'] = pd.to_numeric(df_long['Import_Dependency_Pct'], errors='coerce')

# Remove rows with missing values
df_long = df_long.dropna(subset=['Import_Dependency_Pct'])

# Round to 1 decimal place
df_long['Import_Dependency_Pct'] = df_long['Import_Dependency_Pct'].round(1)

# Sort by year and country
df_long = df_long.sort_values(['Year', 'Country Name']).reset_index(drop=True)

# Save cleaned data
output_path = "/Users/sandrarune/Library/CloudStorage/OneDrive-DanmarksTekniskeUniversitet/8. sem/Social dataanalyse og vis/WEEKS_ny/Sandra359.github.io/FinalProject/datasæt/energy_imports_clean.csv"
df_long.to_csv(output_path, index=False)

print(f"\n✓ Transformed to long format:")
print(f"  {len(df_long)} rows (country × year combinations)")
print(f"  {df_long['Country Name'].nunique()} unique countries")
print(f"  {df_long['Year'].min()}-{df_long['Year'].max()} years")
print(f"\n✓ Saved to: {output_path}")

# Show sample
print("\n--- SAMPLE DATA ---")
print(df_long[df_long['Country Name'].str.contains('Denmark|Japan|China', regex=True)].head(12))

# Show top importers in 2023
print("\n--- TOP 15 IMPORTERS (2023) ---")
top_2023 = df_long[df_long['Year'] == 2023].nlargest(15, 'Import_Dependency_Pct')[['Country Name', 'Import_Dependency_Pct']]
print(top_2023.to_string(index=False))
