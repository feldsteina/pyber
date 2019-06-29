# %%
import os.path as path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patches as mpatches
get_ipython().run_line_magic('matplotlib', 'inline')
# Dependencies and Setup

# File to Load (Remember to change these)
city_file = path.join("data", "city_data.csv")
ride_file = path.join("data", "ride_data.csv")

# Read the City and Ride Data
city_df = pd.read_csv(city_file)
ride_df = pd.read_csv(ride_file)

# Combine the data into a single dataset
pyber_df = pd.merge(city_df, ride_df, on="city", how="right")

# Display the data table for preview
pyber_df.head()

# %%
urban_cities = pyber_df[pyber_df.type == "Urban"]
urban_ride_count = urban_cities.groupby(["city"]).count()["ride_id"]
urban_driver_count = urban_cities.groupby(["city"]).mean()["driver_count"]
urban_fare = urban_cities.groupby(["city"]).mean()["fare"]

suburban_cities = pyber_df[pyber_df.type == "Suburban"]
suburban_ride_count = suburban_cities.groupby(["city"]).count()["ride_id"]
suburban_driver_count = suburban_cities.groupby(["city"]).mean()[
    "driver_count"]
suburban_fare = suburban_cities.groupby(["city"]).mean()["fare"]

rural_cities = pyber_df[pyber_df.type == "Rural"]
rural_ride_count = rural_cities.groupby(["city"]).count()["ride_id"]
rural_driver_count = rural_cities.groupby(["city"]).mean()["driver_count"]
rural_fare = rural_cities.groupby(["city"]).mean()["fare"]

# %% [markdown]
# ## Bubble Plot of Ride Sharing Data
# Build the scatter plots for each city types
plt.scatter(urban_ride_count,
            urban_fare,
            s=urban_driver_count**2, c="lightcoral",
            edgecolor="black", linewidths=1, marker="o",
            alpha=0.4, label="Urban")

plt.scatter(suburban_ride_count,
            suburban_fare,
            s=suburban_driver_count**2, c="lightskyblue",
            edgecolor="black", linewidths=1, marker="o",
            alpha=0.4, label="Suburban")

plt.scatter(rural_ride_count,
            rural_fare,
            s=rural_driver_count**2, c="gold",
            edgecolor="black", linewidths=1, marker="o",
            alpha=0.4, label="Rural")

# Incorporate the other graph properties
plt.xlabel("Number of Rides")
plt.ylabel("Average Fare ($)")
plt.title("Average Fare vs Number of Rides per City (2016)")
plt.grid(True)

# Create a legend
lgnd = plt.legend(fontsize="small", mode="Expanded",
                  numpoints=1, scatterpoints=1,
                  loc="best", title="City Types",
                  labelspacing=0.5)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]
lgnd.legendHandles[2]._sizes = [30]

# Incorporate a text label regarding circle size
plt.text(42, 40, "Bigger circle = more rides")

# Save Figure
plt.savefig("analysis/bubble.png")
plt.show()

# %%
# set up variables for next section
colors = ["gold", "lightskyblue", "lightcoral"]
labels = ["Rural", "Suburban", "Urban"]

# %% [markdown]
# ## Total Fares by City Type

# %%
# Calculate Type Percents
type_pct = 100 * \
    pyber_df.groupby(["type"]).sum()["fare"] / pyber_df["fare"].sum()

# %%
# Build Pie Chart
plt.pie(type_pct,
        labels=labels,
        colors=colors,
        explode=[0.0, 0.0, 0.1],
        autopct="%1.2f%%",
        shadow=True,
        startangle=-43
        )
plt.title("% of Total Fares by City Type")
plt.savefig("analysis/fares_pie.png")
plt.show()

# %% [markdown]
# ## Total Rides by City Type

# %%
# Calculate Ride Percents
type_pct = 100 * \
    pyber_df.groupby(["type"]).count()["ride_id"] / pyber_df["ride_id"].count()

# %%
# Build Pie Chart
plt.pie(type_pct,
        labels=labels,
        colors=colors,
        explode=[0.0, 0.0, 0.1],
        autopct="%1.2f%%",
        shadow=True,
        startangle=-23
        )
plt.title("% of Total Rides by City Type")
plt.savefig("analysis/rides_pie.png")
plt.show()

# %% [markdown]
# ## Total Rides by City Type

# %%
# Calculate Driver Percents

type_pct = 100 * \
    pyber_df.groupby(["type"]).sum()["driver_count"] / \
    pyber_df["driver_count"].sum()

# %%
# Build Pie Charts
plt.pie(type_pct,
        labels=labels,
        colors=colors,
        explode=[0.0, 0.0, 0.1],
        autopct="%1.2f%%",
        shadow=True,
        startangle=43
        )
plt.title("% of Total Drivers by City Type")
plt.savefig("analysis/drivers_pie.png")
plt.show()

# %% [markdown]
# ## Observations
# 1. Most of the drivers, rides, and fares are in Urban locations
# 2. Urban areas have a lower ratio of rides to drivers
# 3. Rural areas make up the lowest market share, and have almost no drivers
