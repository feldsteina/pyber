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
pyber_df = pd.merge(city_df, ride_df, on="city", how="inner")

# Change city type to number, add city type name column
pyber_df["city_type_name"] = pyber_df["type"]

city_type_names = []

for items in pyber_df.city_type_name.unique():
    city_type_names.append(items)
    print(items)

city_type_cnt = pyber_df["city_type_name"].nunique()

value_list = []

for i in range(city_type_cnt):
    value_list.append(i)
    print(i)

pyber_df["type"].replace(to_replace=city_type_names,
                         inplace=True,
                         value=value_list)

# Display the data table for preview
pyber_df.head()

# %%
averages_df = pyber_df.groupby(["city"], as_index=False).mean()

averages_df["ride_count"] = pyber_df.groupby(["city"])\
    .count()["ride_id"].tolist()

averages_df["driver_count"] = pyber_df.groupby(["city"])\
    .median()["driver_count"].tolist()

averages_df["city_type"] = pyber_df.groupby(["city"])\
    .first()["type"].tolist()

averages_df["city_type_name"] = pyber_df.groupby(["city"])\
    .first()["city_type_name"].tolist()

averages_df.drop(labels=["ride_id"], axis=1, inplace=True)

averages_df["fare"] = averages_df["fare"].round(2)

averages_df.head()


# %% [markdown]
# ## Bubble Plot of Ride Sharing Data

# %%
# Build a colormap

cmap = ["gold", "lightblue", "coral"]

cmapList = [cmap[i] for i in range(city_type_cnt)]

cmap = colors.LinearSegmentedColormap.from_list(
    "customCmap", cmapList, city_type_cnt)

cmapList = [cmap(i) for i in range(city_type_cnt)]

patch_data = []

for i in range(city_type_cnt):
    for items in city_type_names:
        patch_data.append(
            mpatches.Patch(
                color=cmapList[i], label=city_type_names[i]
            )
        )
        break

# %%
# Obtain the x and y coordinates for each of the three city types
x = averages_df["driver_count"]
y = averages_df["fare"]
s = [n**2 for n in averages_df["ride_count"]]
city_pop = averages_df["city_type"]

# Build the scatter plots for each city types
plt.scatter(x, y, s=s, c=city_pop, alpha=0.3, cmap=cmap)

# Incorporate the other graph properties

# Create a legend

# Incorporate a text label regarding circle size
# plt.labels("Bigger circle = more fares")
plt.xlabel("Number of drivers per city")
plt.ylabel("Average fare per city")
plt.title("Average fare vs number of drivers per city")
plt.text(20, 41, "Bigger circle = more fares")
plt.legend(handles=patch_data)

# Save Figure
plt.savefig("bubble.png")
plt.show()

# %% [markdown]
# ## Total Fares by City Type


# %%
# Calculate Type Percents
city_fare_pct = []

for i in range(city_type_cnt):
    city_fare_pct.append(
        int(
            round(
                pyber_df.loc[
                    pyber_df.type == i, ["fare"]
                ].sum() /
                pyber_df.fare.sum(), 2
            ) * 100
        )
    )

for items in city_fare_pct:
    print(items)

# %%
# Build Pie Chart
x = city_fare_pct

plt.pie(x, labels=city_type_names, colors=cmapList, autopct="%.2f")

plt.xlabel("% Fares by City Type")
plt.legend()

plt.savefig("fares_pie.png")
plt.show()

# %% [markdown]
# ## Total Rides by City Type

# %%
# Calculate Ride Percents
city_total_rides_pct = []

for i in range(city_type_cnt):
    city_total_rides_pct.append(
        int(
            round(
                averages_df.loc[
                    averages_df.city_type == i, ["ride_count"]
                ].sum() / averages_df["ride_count"].sum(), 2
            ) * 100
        )
    )

for items in city_total_rides_pct:
    print(items)

# %%
# Build Pie Chart
x = city_total_rides_pct

plt.pie(x, labels=city_type_names, colors=cmapList, autopct="%.2f")
plt.xlabel("% Rides by City Type")

plt.legend()

plt.savefig("rides_pie.png")
plt.show()

# %% [markdown]
# ## Total Drivers by City Type

# %%
# Calculate Driver Percents
city_driver_pct = []

for i in range(city_type_cnt):
    city_driver_pct.append(
        int(
            round(
                averages_df.loc[
                    averages_df["city_type"] == i, ["driver_count"]
                ].sum() / averages_df["driver_count"].sum(), 2
            ) * 100
        )
    )

for items in city_driver_pct:
    print(items)

# %%
# Build Pie Charts
x = city_driver_pct

plt.pie(x, labels=city_type_names, colors=cmapList, autopct="%.2f")
plt.xlabel("% Drivers by City Type")
plt.legend()

plt.savefig("drivers_pie.png")
plt.show()

# %% [markdown]
# ## Observations
# 1. Most of the drivers, rides, and fares are in Urban locations
# 2. Urban areas have more drivers than they have rides
# 3. Suburban areas have more rides than they have drivers
