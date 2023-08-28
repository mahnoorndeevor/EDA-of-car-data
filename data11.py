import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt

data2=pd.read_csv('C:/Users/USER/Dev/cfehome/data.csv')
#visulaize all the null values
null=data2.isna().any()
data2.isna().sum().plot(kind='bar', title='NaN values in all columns')
plt.show()
#fill all the data NAN with 0
data3=data2.fillna(0)
#subsetting and sorting/adding any new columns


data4=data3.sort_values("time_stamp", ascending=True)
#adding time colummn
oDtime=pd.to_datetime(data4['time_stamp'], format='%Y-%m-%d %H:%M:%S')
data4['time_stamp']=data4['time_stamp'].astype('datetime64[ns]')
data4['time_stampstr']=data4['time_stamp'].astype('string')
data4['Time_only']=data4['time_stamp'].dt.time
data4['Time_onlystr'] = data4['Time_only'].astype('string')
#Long-Term Trends: Consistent trends over time might indicate stable vehicle performance.
#plot time with vehicle speed
plt.plot(data4['time_stampstr'], data4['vehicle_speed'])
plt.grid(True)
plt.xticks(['2023-04-20 18:44:53', '2023-04-26 22:14:35', '2023-05-02 09:33:34'])
plt.title('Speed vs Timestamp plot')
plt.xlabel('Date Time')
plt.ylabel('Speed of Vehicle')
plt.xticks(rotation=10)
plt.show()
#time with engine rpm
plt.plot(data4['time_stampstr'], data4['engine_rpm'])
plt.grid(True)
plt.xticks(['2023-04-20 18:44:53', '2023-04-26 22:14:35', '2023-05-02 09:33:34'])
plt.title('rpm vs Timestamp')
plt.xlabel('Date Time')
plt.ylabel('RPM')
plt.xticks(rotation=10)
plt.show()


#Descriptive Statistics:
Description=data4.describe()
# First set of plots
fig, axes = plt.subplots(4, 2, figsize=(15, 15))

# Plot 1
sns.lineplot(x='vehicle_speed', y='ambient_air_temperature', data=data4, ax=axes[0, 0])

sns.lineplot(x='vehicle_speed', y='latitude', data=data4, ax=axes[0, 1])

sns.lineplot(x='vehicle_speed', y='longitude', data=data4, ax=axes[1, 0])

sns.lineplot(x='vehicle_speed', y='heading', data=data4, ax=axes[1, 1])

# Plot 2
sns.boxplot(data=data4, x='o_s2_b2_voltage', ax=axes[2, 0])

sns.lineplot(x='vehicle_speed', y='o_s2_b2_voltage', data=data4, ax=axes[2, 1])

sns.lineplot(x='vehicle_speed', y='o_s1_current', data=data4, ax=axes[3, 0])

sns.boxplot(data=data4, x='calculated_engine_load', ax=axes[3, 1])

plt.tight_layout()

# Second set of plots
fig, axes = plt.subplots(3, 2, figsize=(15, 15))

# Plot 3
sns.lineplot(x='vehicle_speed', y='engine_rpm', data=data4, ax=axes[0, 0])

sns.lineplot(x='vehicle_speed', y='spark_advance', data=data4, ax=axes[0, 1])

sns.lineplot(x='vehicle_speed', y='absolute_load_value', data=data4, ax=axes[1, 0])

sns.lineplot(x='vehicle_speed', y='throttle_position', data=data4, ax=axes[1, 1])

# Plot 4
sns.lineplot(x='vehicle_speed', y='relative_throttle_position', data=data4, ax=axes[2, 0])

sns.lineplot(x='vehicle_speed', y='absolute_throttle_position', data=data4, ax=axes[2, 1])

plt.tight_layout()

# Third set of plots
fig, axes = plt.subplots(2, 2, figsize=(15, 15))

# Plot 5
sns.lineplot(x='vehicle_speed', y='ap_pos_d', data=data4, ax=axes[0, 0])

sns.lineplot(x='vehicle_speed', y='ap_pos_e', data=data4, ax=axes[0, 1])

sns.lineplot(x='vehicle_speed', y='o_s1_current', data=data4, ax=axes[1, 0])

sns.boxplot(data=data4, x='calculated_engine_load', ax=axes[1, 1])

plt.tight_layout()

plt.show()

#Correlation (the points near zero are weakly correlated and points near 1 and minus 1 are strong correlation)
speedtemppressure=['vehicle_speed', 'engine_rpm', 'commanded_evaporative_purge', 'fuel_rail_pressure', 'absolute_load_value', 'calculated_engine_load', 'o_s1_b1_fuel_air_equivalence_ratio','mass_air_flow_rate', 'absolute_barometric_pressure', 'engine_coolant_temperature', 'intake_air_temperature', 'catalyst_temperature_b1_s1', 'catalyst_temperature_b1_s2', 'ambient_air_temperature', 'o_s2_b2_voltage']
correlation1=data4[speedtemppressure].corr()
plt.figure(figsize=(25, 15))
sns.heatmap(correlation1, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap of Speed/rpm, Temperature, Pressure values, engine load')
plt.show()
distancerotspeed=['vehicle_speed', 'engine_rpm', 'latitude', 'longitude','ap_pos_d', 'ap_pos_e', 'absolute_load_value', 'calculated_engine_load', 'throttle_position', 'relative_throttle_position', 'absolute_throttle_position', 'heading', 'altitude', 'short_term_fuel_trim_b1', 'long_term_fuel_trim_b1', 'o_s2_b2_voltage']
correlation2=data4[distancerotspeed].corr()
plt.figure(figsize=(25, 15))
sns.heatmap(correlation2, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap of Speed/rpm mechanical factors, distance factors')
plt.show()
#subsetting and sorting/adding any new columns
data4['estimated_mpg'] = data4['vehicle_speed'] / (data4['intake_air_temperature'] + 273.15)
sns.scatterplot(data=data4, x='vehicle_speed', y='estimated_mpg')
plt.title('Estimated mpg') 
plt.show()
#Engine Efficiency: Higher vehicle speed at lower engine RPM might indicate better efficiency.
sns.scatterplot(data=data4, x='vehicle_speed', y='engine_rpm', marker='o')
plt.title('engine efficiency')
plt.show()
#Consistency Analysis: Identify periods of consistent behavior versus periods with large fluctuations.
df=data4.agg({'vehicle_speed':'std', 'engine_rpm':'std'})
print("standard deviations for consitency: ", df)
data4['speed STD']=data4['vehicle_speed'].std()
data4['Rpm STD']=data4['engine_rpm'].std()

sns.scatterplot(data=data4, x='speed STD', y='Rpm STD')
plt.title('Consistency Analysis')
plt.show()
#Fuel Consumption Patterns: Look for patterns where higher speed or engine RPM corresponds to higher fuel consumption.
sns.scatterplot(data=data4, x='estimated_mpg', y='vehicle_speed', marker='o', color='green', label='Fuel consumption with speed')
plt.show()
sns.scatterplot(data=data4, x='estimated_mpg', y='engine_rpm', marker='o', color='blue', label='Fuel consumption with rpm')
plt.show()

#Engine Load and Efficiency Analysis: Higher engine load might indicate less efficient operation

# Scatter plot of engine load vs. vehicle speed
sns.scatterplot(data=data4, x='calculated_engine_load', y='vehicle_speed')
plt.title('Engine Load and Efficiency Analysis')
plt.xlabel('Calculated Engine Load')
plt.ylabel('Vehicle Speed')
plt.show()

# Scatter plot of engine load vs. fuel rail pressure
sns.scatterplot(data=data4, x='calculated_engine_load', y='fuel_rail_pressure')
plt.title('Engine Load and Efficiency Analysis')
plt.xlabel('Calculated Engine Load')
plt.ylabel('Fuel Rail Pressure')
plt.show()

# Scatter plot of engine load vs. engine RPM
sns.scatterplot(data=data4, x='calculated_engine_load', y='engine_rpm')
plt.title('Engine Load and Efficiency Analysis')
plt.xlabel('Calculated Engine Load')
plt.ylabel('Engine RPM')
plt.show()

#Environmental Impact Analysis: Changes in temperature could impact vehicle efficiency and consistency.
# Scatter plot of ambient air temperature vs. vehicle speed
sns.scatterplot(data=data4, x='ambient_air_temperature', y='vehicle_speed')
plt.title('Environmental Impact Analysis')
plt.xlabel('Ambient Air Temperature')
plt.ylabel('Vehicle Speed')
plt.show()

# Scatter plot of ambient air temperature vs. fuel rail pressure
sns.scatterplot(data=data4, x='ambient_air_temperature', y='fuel_rail_pressure')
plt.title('Environmental Impact Analysis')
plt.xlabel('Ambient Air Temperature')
plt.ylabel('Fuel Rail Pressure')
plt.show()

# Scatter plot of ambient air temperature vs. engine RPM
sns.scatterplot(data=data4, x='ambient_air_temperature', y='engine_rpm')
plt.title('Environmental Impact Analysis')
plt.xlabel('Ambient Air Temperature')
plt.ylabel('Engine RPM')
plt.show()
