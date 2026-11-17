import requests
import time
BLYNK_SERVER = "https://blr1.blynk.cloud"
BLYNK_TOKEN = os.getenv("BLYNK_AUTH_TOKEN", "")

def update_blynk(pin, value):
    url = f"{BLYNK_SERVER}/external/api/update"

    response = requests.get(
        url,
        params={
            "token": BLYNK_TOKEN,
            pin: value
        },
        timeout=15
    )

    response.raise_for_status()
    
print("Testing Blynk connection...")

update_blynk("V0", 37.7)

print("Blynk connection successful!")


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
10:00:00,24.0,45,800,0,0,None,12.0,0.10
10:00:05,25.0,46,100,1,0,None,12.0,0.15
10:00:10,32.0,55,500,0,0,None,12.0,0.30
10:00:15,31.0,58,100,1,0,None,12.0,0.35
10:00:20,26.0,48,450,1,1,A1B2C3,12.0,0.12
10:00:25,27.0,49,450,1,1,A2B4C3,12.0,0.15
10:00:30,26.5,50,450,1,1,None,12.0,0.10"""

# Convert raw data into a table using Pandas DataFrame
data = pd.read_csv(StringIO(raw_data))

# Make RFID values strings
data["rfid_id"] = data["rfid_id"].fillna("None").astype(str)

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

# ============================================================
# AUTOMATED TEST CASES
# ============================================================

print("\n==============================================")
print("             AUTOMATED TESTING")
print("==============================================")


# TC1: Check Fan Control
# Expected: If temperature >= 30°C, fan should be ON

tc1_pass = True

for i in range(len(data)):

    if data.loc[i, "temperature"] >= FAN_THRESHOLD:

        if data.loc[i, "fan_output"] != 1:
            tc1_pass = False


# TC2: Check Automatic Lighting
# Expected: If it is dark AND motion is detected,
# the light should be ON

tc2_pass = True

for i in range(len(data)):

    if (
        data.loc[i, "light"] < LIGHT_THRESHOLD
        and data.loc[i, "motion"] == 1
    ):

        if data.loc[i, "light_output"] != 1:
            tc2_pass = False


# TC3: Check Authorized RFID
# Expected: Authorized RFID + open door = alarm OFF

tc3_pass = True

for i in range(len(data)):

    if data.loc[i, "door"] == 1:

        if data.loc[i, "rfid_id"] in known_ids:

            if data.loc[i, "alarm"] != 0:
                tc3_pass = False


# TC4: Check Unauthorized RFID
# Expected: Unauthorized RFID + open door = alarm ON

tc4_pass = True

for i in range(len(data)):

    if data.loc[i, "door"] == 1:

        if data.loc[i, "rfid_id"] not in known_ids:

            if data.loc[i, "alarm"] != 1:
                tc4_pass = False


# Overall result

all_tests_pass = (
    tc1_pass
    and tc2_pass
    and tc3_pass
    and tc4_pass
)


# Display results

print(
    "TC1 - Temperature/Fan Control :",
    "PASS" if tc1_pass else "FAIL"
)

print(
    "TC2 - Automatic Lighting :",
    "PASS" if tc2_pass else "FAIL"
)

print(
    "TC3 - Authorized RFID :",
    "PASS" if tc3_pass else "FAIL"
)

print(
    "TC4 - Unauthorized RFID :",
    "PASS" if tc4_pass else "FAIL"
)

print("----------------------------------------------")

print(
    "Overall Status :",
    "PASS" if all_tests_pass else "FAIL"
)

print("==============================================")

# ============================================================
# SEND TEST RESULTS TO BLYNK
# ============================================================

print("\nSending test results to Blynk...")

update_blynk("V12", "PASS" if tc1_pass else "FAIL")
update_blynk("V13", "PASS" if tc2_pass else "FAIL")
update_blynk("V14", "PASS" if tc3_pass else "FAIL")
update_blynk("V15", "PASS" if tc4_pass else "FAIL")
update_blynk("V16", "PASS" if all_tests_pass else "FAIL")

print("Test results sent to Blynk.")

# ============================================================
# SEND DATA TO BLYNK
# ============================================================

print("\nSending data to Blynk...")


for i in range(len(data)):

    # ---------------- SENSOR DATA ----------------

    update_blynk("V0", data.loc[i, "temperature"])
    update_blynk("V1", data.loc[i, "humidity"])
    update_blynk("V2", data.loc[i, "light"])
    update_blynk("V3", data.loc[i, "motion"])
    update_blynk("V4", data.loc[i, "door"])
    update_blynk("V5", data.loc[i, "rfid_id"])
    update_blynk("V6", data.loc[i, "voltage"])
    update_blynk("V7", data.loc[i, "current"])
    update_blynk("V8", data.loc[i, "power"])

    # ---------------- AUTOMATION OUTPUTS ----------------

    update_blynk("V9", data.loc[i, "light_output"])
    update_blynk("V10", data.loc[i, "fan_output"])
    update_blynk("V11", data.loc[i, "alarm"])

    print(
        "Sent:",
        data.loc[i, "timestamp"],
        "| Temperature:",
        data.loc[i, "temperature"],
        "| Light:",
        data.loc[i, "light"],
        "| Fan:",
        data.loc[i, "fan_output"],
        "| Light Output:",
        data.loc[i, "light_output"],
        "| Alarm:",
        data.loc[i, "alarm"]
    )

    # Wait 2 seconds before sending the next row
    time.sleep(2)


print("\nAll data sent to Blynk.")



# Charts using matplotlib
# Matplotlib is used to create graphs from our sensor data
import matplotlib.pyplot as plt

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