
#%%
import os.path as path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# Display the data table for preview
pyber_df.head()

#%%
averages_df = pyber_df.groupby(["city"], as_index=False).mean()

averages_df["ride_count"] = pyber_df.groupby(["city"])\
    .count()["ride_id"].tolist()

averages_df["driver_count"] = pyber_df.groupby(["city"])\
    .median()["driver_count"].tolist()

averages_df["city_type"] = pyber_df.groupby(["city"])\
    .first()["type"].tolist()

averages_df["city_type"].replace(to_replace=["Urban", "Suburban", "Rural"],
                                 inplace=True,
                                 value=[0, 1, 2])

averages_df.drop(labels=["ride_id"], axis=1, inplace=True)

averages_df["fare"] = averages_df["fare"].round(2)

averages_df.head()

#%% [markdown]
# ## Bubble Plot of Ride Sharing Data

#%%
# Obtain the x and y coordinates for each of the three city types
x = averages_df["driver_count"]
y = averages_df["fare"]
s = [n**2 for n in averages_df["ride_count"]]
city_pop = averages_df["city_type"]
# Build the scatter plots for each city types


# Incorporate the other graph properties

# Create a legend
# plt.legend(handles=1, loc=[1.05, 0])

# Incorporate a text label regarding circle size
# plt.labels("Bigger circle = more fares")
plt.xlabel("Number of fares per city")
plt.ylabel("Income per city")

# Save Figure
plt.scatter(x, y, s=s, c=city_pop, alpha=0.4, cmap="tab10")
plt.savefig("bubble.png")
plt.show()

#%% [markdown]
# ## Total Fares by City Type


#%%
# Calculate Type Percents

# Build Pie Chart

# Save Figure


#%%
# Show Figure
plt.show()

#%% [markdown]
# ## Total Rides by City Type

#%%
# Calculate Ride Percents

# Build Pie Chart

# Save Figure


#%%
# Show Figure
plt.show()

#%% [markdown]
# ## Total Drivers by City Type

#%%
# Calculate Driver Percents

# Build Pie Charts

# Save Figure


#%%
# Show Figure
plt.show()


#%%
