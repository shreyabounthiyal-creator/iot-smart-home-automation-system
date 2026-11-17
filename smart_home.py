print("Smart Home Automation System")
print("Python implementation started")

# Pandas is used to store sensor data in rows and columns
import pandas as pd
# Display all columns of the sensor data
pd.set_option("display.max_columns", None)

# StringIO is used to read our raw text data like a CSV file
from io import StringIO

# Sample raw sensor data collected from different sensors
raw_data = """timestamp,temperature,humidity,light,motion,door,rfid_id,voltage,current
10:00:00,24.5,45,850,0,0,None,12.0,0.10
10:00:05,24.7,46,820,1,0,None,12.0,0.12
10:00:10,25.1,46,700,1,0,None,12.0,0.15
10:00:15,26.0,47,180,1,0,None,12.0,0.20
10:00:20,27.2,48,120,1,0,None,12.0,0.22
10:00:25,29.0,50,100,1,0,None,12.0,0.25
10:00:30,31.0,53,90,1,0,None,12.0,0.30
10:00:35,32.5,55,80,1,0,None,12.0,0.35
10:00:40,31.8,54,75,0,0,None,12.0,0.18
10:00:45,30.5,52,70,0,0,None,12.0,0.15
10:00:50,29.5,50,60,1,1,A1B2C3,12.0,0.10
10:00:55,28.5,49,50,1,1,A2B4C3,12.0,0.12
11:00:00,27.5,48,55,1,1,None,12.0,0.10"""

# Convert raw data into a table using Pandas DataFrame
data = pd.read_csv(StringIO(raw_data))

# Display the raw sensor data
print(data)

# Calculate average, maximum and minimum temperature
average_temperature = data["temperature"].mean()
maximum_temperature = data["temperature"].max()
minimum_temperature = data["temperature"].min()
 
# Display the temperature results
print("Average temperature:", round(average_temperature, 2))
print("Maximum temperature:", maximum_temperature)
print("Minimum temperature:", minimum_temperature)

# Calculate power from voltage and current
# Power = Voltage × Current
data["power"] = data["voltage"] * data["current"]
print(data["power"])


# Set light threshold to detect a dark room
LIGHT_THRESHOLD = 200

# Store light control output: 0 = OFF, 1 = ON
data["light_output"] = 0

# Turn ON light when it is dark and motion is detected
for i in range(len(data)):
    if data.loc[i, "light"] < LIGHT_THRESHOLD and data.loc[i, "motion"] == 1:
        data.loc[i, "light_output"] = 1


# Set temperature threshold for fan control
FAN_THRESHOLD = 30

# Store fan control output: 0 = OFF, 1 = ON
data["fan_output"] = 0

# Turn ON fan when temperature reaches the threshold
for i in range(len(data)):
    if data.loc[i, "temperature"] >= FAN_THRESHOLD:
        data.loc[i, "fan_output"] = 1
        
# Enable security monitoring
SECURITY_MODE = True

# Store RFID IDs of authorized people
known_ids = ["A1B2C3", "D4E5F6"]

# Store alarm output: 0 = OFF, 1 = ON
data["alarm"] = 0

# Check the RFID card only when the door is open
for i in range(len(data)):
    if SECURITY_MODE and data.loc[i, "door"] == 1:

        # Check whether the scanned RFID belongs to a known person
        if data.loc[i, "rfid_id"] in known_ids:
            data.loc[i, "alarm"] = 0
        else:
            data.loc[i, "alarm"] = 1



# Display final sensor inputs and automation outputs
print(data)


# Save processed data for further analysis
data.to_csv("processed_smart_home_data.csv", index=False)


# Charts using matplotlib
# Matplotlib is used to create graphs from our sensor data
import matplotlib.pyplot as plt
# Plot temperature against time to see how the room temperature changes
plt.plot(data["timestamp"], data["temperature"])

# Add a title to explain what the graph represents
plt.title("Temperature vs Time")

# Label the X-axis with the type of data it contains
plt.xlabel("Time")

# Label the Y-axis with the measurement being displayed
plt.ylabel("Temperature (°C)")

# Add a grid to make the temperature values easier to read
plt.grid(True)

# Display the graph
plt.show()

# Plot light level against time to see how the room brightness changes
plt.plot(data["timestamp"], data["light"])

# Add a title to explain what the graph represents
plt.title("Light Level vs Time")

# Label the X-axis with the type of data it contains
plt.xlabel("Time")

# Label the Y-axis with the sensor measurement
plt.ylabel("Light Level")

# Add a grid to make the values easier to read
plt.grid(True)

# Display the graph
plt.show()

# Plot calculated power consumption against time
plt.plot(data["timestamp"], data["power"])

# Add a title to explain what the graph represents
plt.title("Power Consumption vs Time")

# Label the X-axis with the time of each reading
plt.xlabel("Time")

# Label the Y-axis with the calculated power
plt.ylabel("Power (W)")

# Add a grid to make the power values easier to read
plt.grid(True)

# Display the graph
plt.show()

# Plot the automatic light control output against time
plt.step(data["timestamp"], data["light_output"])

# Add a title to explain what the graph represents
plt.title("Automatic Light Output vs Time")

# Label the X-axis with time
plt.xlabel("Time")

# Label the Y-axis with the light control state
plt.ylabel("Light Output (0 = OFF, 1 = ON)")

# Add a grid to make the ON/OFF states easier to see
plt.grid(True)

# Display the graph
plt.show()

# Plot the automatic fan control output against time
plt.step(data["timestamp"], data["fan_output"])

# Add a title to explain what the graph represents
plt.title("Automatic Fan Output vs Time")

# Label the X-axis with time
plt.xlabel("Time")

# Label the Y-axis with the fan control state
plt.ylabel("Fan Output (0 = OFF, 1 = ON)")

# Add a grid to make the ON/OFF states easier to see
plt.grid(True)

# Display the graph
plt.show()

# Plot the security alarm output against time
plt.step(data["timestamp"], data["alarm"])

# Add a title to explain what the graph represents
plt.title("Security Alarm Output vs Time")

# Label the X-axis with time
plt.xlabel("Time")

# Label the Y-axis with the alarm state
plt.ylabel("Alarm Output (0 = OFF, 1 = ON)")

# Add a grid to make the ON/OFF states easier to see
plt.grid(True)

# Display the graph
plt.show()

# Create one figure containing 6 graphs arranged in 3 rows and 2 columns
# Set the overall size of the figure (width, height) in inches
fig, axes = plt.subplots(3, 2, figsize=(14, 10))


# ---------------- TEMPERATURE ----------------

# Plot temperature against time
axes[0, 0].plot(data["timestamp"], data["temperature"])

# Add a title to the temperature graph
axes[0, 0].set_title("Temperature vs Time")

# Label the X-axis
axes[0, 0].set_xlabel("Time")

# Label the Y-axis
axes[0, 0].set_ylabel("Temperature (°C)")

# Add a grid
axes[0, 0].grid(True)


# ---------------- LIGHT LEVEL ----------------

# Plot light level against time
axes[0, 1].plot(data["timestamp"], data["light"])

# Add a title to the light graph
axes[0, 1].set_title("Light Level vs Time")

# Label the X-axis
axes[0, 1].set_xlabel("Time")

# Label the Y-axis
axes[0, 1].set_ylabel("Light Level")

# Add a grid
axes[0, 1].grid(True)


# ---------------- POWER ----------------

# Plot calculated power against time
axes[1, 0].plot(data["timestamp"], data["power"])

# Add a title to the power graph
axes[1, 0].set_title("Power Consumption vs Time")

# Label the X-axis
axes[1, 0].set_xlabel("Time")

# Label the Y-axis
axes[1, 0].set_ylabel("Power (W)")

# Add a grid
axes[1, 0].grid(True)


# ---------------- LIGHT OUTPUT ----------------

# Plot automatic light output against time
axes[1, 1].step(data["timestamp"], data["light_output"])

# Add a title to the light output graph
axes[1, 1].set_title("Automatic Light Output")

# Label the X-axis
axes[1, 1].set_xlabel("Time")

# Label the Y-axis
axes[1, 1].set_ylabel("Output (0 = OFF, 1 = ON)")

# Add a grid
axes[1, 1].grid(True)


# ---------------- FAN OUTPUT ----------------

# Plot automatic fan output against time
axes[2, 0].step(data["timestamp"], data["fan_output"])

# Add a title to the fan output graph
axes[2, 0].set_title("Automatic Fan Output")

# Label the X-axis
axes[2, 0].set_xlabel("Time")

# Label the Y-axis
axes[2, 0].set_ylabel("Output (0 = OFF, 1 = ON)")

# Add a grid
axes[2, 0].grid(True)


# ---------------- ALARM OUTPUT ----------------

# Plot security alarm output against time
axes[2, 1].step(data["timestamp"], data["alarm"])

# Add a title to the alarm graph
axes[2, 1].set_title("Security Alarm Output")

# Label the X-axis
axes[2, 1].set_xlabel("Time")

# Label the Y-axis
axes[2, 1].set_ylabel("Alarm (0 = OFF, 1 = ON)")

# Add a grid
axes[2, 1].grid(True)


# Automatically adjust spacing between the graphs
plt.tight_layout()

#for saving the figure as a PNG file
#plt.savefig("smart_home_dashboard.png", dpi=300, bbox_inches="tight")

# Display the complete figure
plt.show()