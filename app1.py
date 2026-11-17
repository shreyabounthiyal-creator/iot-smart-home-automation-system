import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Home Automation",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# LOAD TEST DATA
# ============================================================

data = pd.read_csv("processed_smart_home_data.csv")

data["rfid_id"] = data["rfid_id"].fillna("None").astype(str)

# ============================================================
# TITLE
# ============================================================

st.title("🏠 Smart Home Automation System")
st.caption("IoT Monitoring • Automation • Security • Testing")

# ============================================================
# MODE SELECTION
# ============================================================

mode = st.radio(
    "Select Dashboard Mode",
    ["🧪 TEST MODE", "📡 LIVE MODE"],
    horizontal=True
)

st.divider()

# ============================================================
# TEST MODE
# ============================================================

if mode == "🧪 TEST MODE":

    st.header("🧪 TEST MODE")
    st.write(
        "This mode uses simulated sensor data to test the "
        "automation and security logic."
    )

    # --------------------------------------------------------
    # LATEST TEST READING
    # --------------------------------------------------------

    latest = data.iloc[-1]

    st.subheader("Current Test Reading")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Temperature",
            f"{latest['temperature']} °C"
        )

    with col2:
        st.metric(
            "💧 Humidity",
            f"{latest['humidity']} %"
        )

    with col3:
        st.metric(
            "💡 Light",
            f"{latest['light']}"
        )

    with col4:
        st.metric(
            "⚡ Power",
            f"{latest['power']:.2f} W"
        )

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    st.subheader("Security & Room Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        motion = "DETECTED" if latest["motion"] == 1 else "NO MOTION"
        st.metric("🚶 Motion", motion)

    with col2:
        door = "OPEN" if latest["door"] == 1 else "CLOSED"
        st.metric("🚪 Door", door)

    with col3:
        st.metric("🪪 RFID", latest["rfid_id"])

    with col4:
        st.metric(
            "🔌 Voltage",
            f"{latest['voltage']} V"
        )

    # --------------------------------------------------------
    # AUTOMATION OUTPUTS
    # --------------------------------------------------------

    st.subheader("Automatic Control")

    col1, col2, col3 = st.columns(3)

    with col1:
        if latest["light_output"] == 1:
            st.success("💡 LIGHT: ON")
        else:
            st.info("💡 LIGHT: OFF")

    with col2:
        if latest["fan_output"] == 1:
            st.success("🌀 FAN: ON")
        else:
            st.info("🌀 FAN: OFF")

    with col3:
        if latest["alarm"] == 1:
            st.error("🚨 ALARM: ON")
        else:
            st.success("🔔 ALARM: SAFE")

    # ========================================================
    # TEST CASE LOGIC
    # ========================================================

    known_ids = ["A1B2C3", "D4E5F6"]

    # TC1 — Fan
    fan_cases = data[data["temperature"] >= 30]

    if len(fan_cases) > 0:
        tc1 = (fan_cases["fan_output"] == 1).all()
    else:
        tc1 = False

    # TC2 — Light
    light_cases = data[
        (data["light"] < 200) &
        (data["motion"] == 1)
    ]

    if len(light_cases) > 0:
        tc2 = (light_cases["light_output"] == 1).all()
    else:
        tc2 = False

    # TC3 — Authorized RFID
    authorized_cases = data[
        (data["door"] == 1) &
        (data["rfid_id"].isin(known_ids))
    ]

    if len(authorized_cases) > 0:
        tc3 = (authorized_cases["alarm"] == 0).all()
    else:
        tc3 = False

    # TC4 — Unauthorized RFID
    unauthorized_cases = data[
        (data["door"] == 1) &
        (~data["rfid_id"].isin(known_ids)) &
        (data["rfid_id"] != "None")
    ]

    if len(unauthorized_cases) > 0:
        tc4 = (unauthorized_cases["alarm"] == 1).all()
    else:
        tc4 = False

    # ========================================================
    # TEST RESULTS
    # ========================================================

    st.subheader("Automated Test Results")

    col1, col2 = st.columns(2)

    with col1:

        if tc1:
            st.success("✅ TC1 — FAN CONTROL : PASS")
        else:
            st.error("❌ TC1 — FAN CONTROL : FAIL")

        st.caption(
            "Temperature ≥ 30°C → Fan should turn ON"
        )

    with col2:

        if tc2:
            st.success("✅ TC2 — AUTOMATIC LIGHTING : PASS")
        else:
            st.error("❌ TC2 — AUTOMATIC LIGHTING : FAIL")

        st.caption(
            "Light < 200 + Motion → Light should turn ON"
        )

    col1, col2 = st.columns(2)

    with col1:

        if tc3:
            st.success("✅ TC3 — AUTHORIZED RFID : PASS")
        else:
            st.error("❌ TC3 — AUTHORIZED RFID : FAIL")

        st.caption(
            "Authorized RFID + Door Open → Alarm OFF"
        )

    with col2:

        if tc4:
            st.success("✅ TC4 — UNAUTHORIZED RFID : PASS")
        else:
            st.error("❌ TC4 — UNAUTHORIZED RFID : FAIL")

        st.caption(
            "Unauthorized RFID + Door Open → Alarm ON"
        )

    # ========================================================
    # OVERALL STATUS
    # ========================================================

    st.subheader("Overall System Status")

    overall = tc1 and tc2 and tc3 and tc4

    if overall:
        st.success("🟢 ALL TEST CASES PASSED")
    else:
        st.error("🔴 ONE OR MORE TEST CASES FAILED")

    # ========================================================
    # TEST CASE INSPECTION
    # ========================================================

    st.subheader("🔎 Inspect Individual Test Case")

    selected_test = st.selectbox(
        "Choose a test case",
        [
            "TC1 — Fan Control",
            "TC2 — Automatic Lighting",
            "TC3 — Authorized RFID",
            "TC4 — Unauthorized RFID"
        ]
    )

    if selected_test == "TC1 — Fan Control":

        st.write(
            "Cases where temperature reached or exceeded 30°C:"
        )

        st.dataframe(
            fan_cases[
                [
                    "timestamp",
                    "temperature",
                    "fan_output"
                ]
            ],
            use_container_width=True
        )

    elif selected_test == "TC2 — Automatic Lighting":

        st.write(
            "Cases where the room was dark and motion was detected:"
        )

        st.dataframe(
            light_cases[
                [
                    "timestamp",
                    "light",
                    "motion",
                    "light_output"
                ]
            ],
            use_container_width=True
        )

    elif selected_test == "TC3 — Authorized RFID":

        st.write(
            "Authorized RFID access attempts:"
        )

        st.dataframe(
            authorized_cases[
                [
                    "timestamp",
                    "door",
                    "rfid_id",
                    "alarm"
                ]
            ],
            use_container_width=True
        )

    elif selected_test == "TC4 — Unauthorized RFID":

        st.write(
            "Unauthorized RFID access attempts:"
        )

        st.dataframe(
            unauthorized_cases[
                [
                    "timestamp",
                    "door",
                    "rfid_id",
                    "alarm"
                ]
            ],
            use_container_width=True
        )

    # ========================================================
    # GRAPHS
    # ========================================================

    st.subheader("📊 Test Data Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🌡️ Temperature")

        st.line_chart(
            data.set_index("timestamp")["temperature"]
        )

    with col2:

        st.write("💡 Light Level")

        st.line_chart(
            data.set_index("timestamp")["light"]
        )

    col1, col2 = st.columns(2)

    with col1:

        st.write("⚡ Power Consumption")

        st.line_chart(
            data.set_index("timestamp")["power"]
        )

    with col2:

        st.write("🌀 Fan Output")

        st.line_chart(
            data.set_index("timestamp")["fan_output"]
        )

    # ========================================================
    # COMPLETE DATA
    # ========================================================

    with st.expander("View Complete Test Data"):

        st.dataframe(
            data,
            use_container_width=True
        )

# ============================================================
# LIVE MODE
# ============================================================

else:

    st.header("📡 LIVE MODE")

    st.info(
        "Live sensor connection is not connected yet. "
        "This section is ready for the ESP8266/hardware connection."
    )

    st.subheader("Live Sensor Readings")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌡️ Temperature", "-- °C")

    with col2:
        st.metric("💧 Humidity", "-- %")

    with col3:
        st.metric("💡 Light", "--")

    with col4:
        st.metric("⚡ Power", "-- W")

    st.subheader("Security Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🚶 Motion", "--")

    with col2:
        st.metric("🚪 Door", "--")

    with col3:
        st.metric("🪪 RFID", "--")

    with col4:
        st.metric("🔌 Voltage", "-- V")

    st.subheader("Automatic Control")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("💡 LIGHT: Waiting for sensor")

    with col2:
        st.info("🌀 FAN: Waiting for sensor")

    with col3:
        st.info("🚨 ALARM: Waiting for sensor")

    st.warning(
        "Hardware integration will be added later. "
        "Your TEST MODE is already working with the simulated data."
    )