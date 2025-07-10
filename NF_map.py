import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from shapely.ops import unary_union
from shapely.geometry import MultiPolygon
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import numpy as np

# Source data
data_list = [
    {  # x = 0%
        "Africa": 41.0,
        "Asia": 54.7,
        "Europe": 58.4,
        "North America": 57.5,
        "Oceania": 40.0,
        "South America": 45.2,
        "Antarctica": 0,
        "Seven seas (open ocean)": np.nan
    },
    {  # x = 10%
        "Africa": 43.6,
        "Asia": 56.9,
        "Europe": 60.5,
        "North America": 59.4,
        "Oceania": 42.7,
        "South America": 47.5,
        "Antarctica": 0,
        "Seven seas (open ocean)": np.nan
    },
    {  # x = 30%
        "Africa": 49.1,
        "Asia": 61.3,
        "Europe": 64.7,
        "North America": 63.5,
        "Oceania": 48.6,
        "South America": 52.5,
        "Antarctica": 0,
        "Seven seas (open ocean)": np.nan
    },
    {  # x = 50%
        "Africa": 55.0,
        "Asia": 66.0,
        "Europe": 69.0,
        "North America": 67.7,
        "Oceania": 55.0,
        "South America": 57.8,
        "Antarctica": 0,
        "Seven seas (open ocean)": np.nan
    },
    {  # x = 80%
        "Africa": 64.7,
        "Asia": 73.3,
        "Europe": 76.0,
        "North America": 74.4,  # OCR had 'T4.4%', corrected to 74.4%
        "Oceania": 65.7,
        "South America": 66.3,
        "Antarctica": 0,
        "Seven seas (open ocean)": np.nan
    }
]

# Read map shapefile
reader = shpreader.Reader(shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries'))
records = list(reader.records())

# Unify continents
cmap = get_cmap('RdBu')
norm = Normalize(vmin=30, vmax=90)

# Plot
for i, continent_values in enumerate(data_list):
    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -60, 80], crs=ccrs.PlateCarree())
    ax.set_global()

    # Latitude and longitude gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = {'size': 15}
    gl.ylabel_style = {'size': 15}

    # Plot continents
    for rec in records:
        continent = rec.attributes['CONTINENT']
        geometry = rec.geometry

        if continent == "Antarctica":
            ax.add_geometries(
                [geometry], ccrs.PlateCarree(),
                facecolor='lightgray', edgecolor='lightgray', linewidth=0.4
            )
        elif continent in continent_values and not np.isnan(continent_values[continent]):
            color = cmap(norm(continent_values[continent]))
            ax.add_geometries(
                [geometry], ccrs.PlateCarree(),
                facecolor=color, edgecolor=color, linewidth=0.4
            )

    # Plot continent boundaries
    continents = {}
    for rec in records:
        continent = rec.attributes['CONTINENT']
        if continent in continent_values:
            geom = rec.geometry
            if continent not in continents:
                continents[continent] = []
            continents[continent].append(geom)

    for name, geoms in continents.items():
        merged = unary_union(geoms)
        if isinstance(merged, MultiPolygon):
            for part in merged.geoms:
                ax.add_geometries([part], ccrs.PlateCarree(), facecolor='none', edgecolor='black', linewidth=0.6)
        else:
            ax.add_geometries([merged], ccrs.PlateCarree(), facecolor='none', edgecolor='black', linewidth=0.6)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, orientation='horizontal', shrink=0.6, pad=0.3)
    cb.ax.tick_params(labelsize=9, labelcolor="black")
    for label in cb.ax.get_xticklabels():
        label.set_fontfamily("Times New Roman")

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12


    plt.show()

