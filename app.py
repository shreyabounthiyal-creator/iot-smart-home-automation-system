import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Home Control Center",
    page_icon="🏠",
    layout="wide"
)

# =========================================================
# DARK UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b0f14;
    color: #f5f7fa;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

.title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    color: #8b949e;
}

.card {
    background: #151b23;
    border: 1px solid #29313d;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}

.card-title {
    color: #8b949e;
    font-size: 14px;
}

.card-value {
    font-size: 28px;
    font-weight: 700;
}

.event {
    background: #151b23;
    border-left: 4px solid #4ade80;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 8px;
}

.alert {
    background: #35151a;
    border-left: 4px solid #ff4d5a;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 8px;
}

.safe {
    background: #12351f;
    border-left: 4px solid #4ade80;
    padding: 14px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# RAW DATA
# =========================================================

raw_data = [
    ["10:00:00", 24.5, 45, 850, 0, 0, None,     12.0, 0.10],
    ["10:00:05", 24.7, 46, 820, 1, 0, None,     12.0, 0.12],
    ["10:00:10", 25.1, 46, 700, 1, 0, None,     12.0, 0.15],

    ["10:00:15", 26.0, 47, 180, 1, 0, None,     12.0, 0.20],
    ["10:00:20", 27.2, 48, 120, 1, 0, None,     12.0, 0.22],
    ["10:00:25", 29.0, 50, 100, 1, 0, None,     12.0, 0.25],

    ["10:00:30", 31.0, 53, 90,  1, 0, None,     12.0, 0.30],
    ["10:00:35", 32.5, 55, 80,  1, 0, None,     12.0, 0.35],

    ["10:00:40", 31.8, 54, 75,  0, 0, None,     12.0, 0.18],
    ["10:00:45", 30.5, 52, 70,  0, 0, None,     12.0, 0.15],

    ["10:00:50", 29.5, 50, 60,  1, 1, "A1B2C3", 12.0, 0.10],

    ["10:00:55", 28.5, 49, 50,  1, 1, "A2B4C3", 12.0, 0.12],

    ["11:00:00", 27.5, 48, 55,  1, 1, None,     12.0, 0.10],
]

columns = [
    "timestamp",
    "temperature",
    "humidity",
    "light",
    "motion",
    "door",
    "rfid_id",
    "voltage",
    "current"
]

df = pd.DataFrame(raw_data, columns=columns)


# =========================================================
# AUTOMATION LOGIC
# =========================================================

KNOWN_IDS = ["A1B2C3", "D4E5F6"]


def calculate_outputs(row):

    light_output = (
        1 if row["light"] < 200 and row["motion"] == 1 else 0
    )

    fan_output = (
        1 if row["temperature"] >= 30 else 0
    )

    alarm = 0

    if row["door"] == 1:

        if row["rfid_id"] is None:
            alarm = 1

        elif row["rfid_id"] not in KNOWN_IDS:
            alarm = 1

    power = row["voltage"] * row["current"]

    return light_output, fan_output, alarm, power


outputs = df.apply(calculate_outputs, axis=1)

df["light_output"] = outputs.apply(lambda x: x[0])
df["fan_output"] = outputs.apply(lambda x: x[1])
df["alarm"] = outputs.apply(lambda x: x[2])
df["power"] = outputs.apply(lambda x: x[3])


# =========================================================
# EVENT DETECTION
# =========================================================

def get_event(row):

    if row["rfid_id"] == "A2B4C3":
        return "🚨 Unauthorized RFID → Alarm ON"

    if row["door"] == 1 and row["rfid_id"] is None:
        return "🚪 Door opened without RFID → Alarm ON"

    if row["rfid_id"] in KNOWN_IDS:
        return "🪪 Authorized RFID → Access allowed"

    if row["temperature"] >= 30:
        return "🌡 High temperature → Fan ON"

    if row["light"] < 200 and row["motion"] == 1:
        return "🌙 Dark + motion → Light ON"

    return "Normal sensor reading"


df["event"] = df.apply(get_event, axis=1)


# =========================================================
# TEST CASES
# =========================================================

def test_fan():

    rows = df[df["temperature"] >= 30]

    return all(rows["fan_output"] == 1)


def test_light():

    rows = df[
        (df["light"] < 200) &
        (df["motion"] == 1)
    ]

    return all(rows["light_output"] == 1)


def test_authorized():

    row = df[df["rfid_id"] == "A1B2C3"].iloc[0]

    return row["alarm"] == 0


def test_unauthorized():

    row = df[df["rfid_id"] == "A2B4C3"].iloc[0]

    return row["alarm"] == 1


tests = [
    ("TC1", "Temperature / Fan Control", test_fan()),
    ("TC2", "Automatic Lighting", test_light()),
    ("TC3", "Authorized RFID", test_authorized()),
    ("TC4", "Unauthorized RFID", test_unauthorized())
]

overall_pass = all(x[2] for x in tests)


# =========================================================
# SESSION STATE
# =========================================================

if "current_index" not in st.session_state:
    st.session_state.current_index = 0


# =========================================================
# HEADER
# =========================================================

h1, h2 = st.columns([5, 1])

with h1:

    st.markdown(
        '<div class="title">🏠 Smart Home Control Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'IoT Monitoring • Automation • Security • Testing'
        '</div>',
        unsafe_allow_html=True
    )

with h2:

    st.success("● SYSTEM ONLINE")

st.divider()


# =========================================================
# SUMMARY
# =========================================================

st.subheader("📊 SYSTEM SUMMARY")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sensor Readings", len(df))

c2.metric(
    "Tests Passed",
    f"{sum(x[2] for x in tests)}/{len(tests)}"
)

c3.metric(
    "Automation Events",
    int(
        df["light_output"].sum()
        + df["fan_output"].sum()
    )
)

c4.metric(
    "Security Alerts",
    int(df["alarm"].sum())
)

c5.metric(
    "Peak Temperature",
    f"{df['temperature'].max()} °C"
)

st.divider()


# =========================================================
# NAVIGATION
# =========================================================

mode = st.radio(
    "View",
    [
        "📊 Live Dashboard",
        "📈 Sensor Trends",
        "🧪 Test Cases",
        "📜 Event Timeline",
        "📡 Raw Data"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# =========================================================
# LIVE DASHBOARD
# =========================================================

if mode == "📊 Live Dashboard":

    row = df.iloc[st.session_state.current_index]

    st.subheader("📡 CURRENT SENSOR READINGS")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🌡 Temperature",
        f"{row['temperature']} °C"
    )

    c2.metric(
        "💧 Humidity",
        f"{row['humidity']} %"
    )

    c3.metric(
        "💡 Light Level",
        row["light"]
    )

    c4.metric(
        "⚡ Power",
        f"{row['power']:.2f} W"
    )

    st.subheader("🏠 ROOM STATUS")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🚶 Motion",
        "DETECTED" if row["motion"] else "NO MOTION"
    )

    c2.metric(
        "🚪 Door",
        "OPEN" if row["door"] else "CLOSED"
    )

    c3.metric(
        "🪪 RFID",
        row["rfid_id"] if row["rfid_id"] else "NONE"
    )

    st.subheader("⚙️ AUTOMATION")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💡 Light",
        "ON" if row["light_output"] else "OFF"
    )

    c2.metric(
        "🌀 Fan",
        "ON" if row["fan_output"] else "OFF"
    )

    c3.metric(
        "🚨 Alarm",
        "ACTIVE" if row["alarm"] else "SAFE"
    )

    st.subheader("🔎 CURRENT EVENT")

    if row["alarm"]:

        st.markdown(
            f'<div class="alert">{row["event"]}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="event">{row["event"]}</div>',
            unsafe_allow_html=True
        )

    st.caption(
        f"Reading {st.session_state.current_index + 1} "
        f"of {len(df)} • {row['timestamp']}"
    )

    st.progress(
        (st.session_state.current_index + 1) / len(df)
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "⬅️ Previous",
            use_container_width=True
        ):

            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.rerun()

    with c2:

        if st.button(
            "Next ➡️",
            use_container_width=True
        ):

            if st.session_state.current_index < len(df) - 1:
                st.session_state.current_index += 1
                st.rerun()


# =========================================================
# SENSOR TRENDS
# =========================================================

elif mode == "📈 Sensor Trends":

    st.header("📈 Sensor Trends")

    st.subheader("🌡 Temperature")

    st.line_chart(
        df.set_index("timestamp")["temperature"]
    )

    st.subheader("💧 Humidity")

    st.line_chart(
        df.set_index("timestamp")["humidity"]
    )

    st.subheader("💡 Light Level")

    st.line_chart(
        df.set_index("timestamp")["light"]
    )

    st.subheader("⚡ Power Consumption")

    st.line_chart(
        df.set_index("timestamp")["power"]
    )


# =========================================================
# TEST CASES
# =========================================================

elif mode == "🧪 Test Cases":

    st.header("🧪 Automated Test Cases")

    for test_id, name, result in tests:

        if result:

            st.success(
                f"✅ {test_id} — {name} — PASS"
            )

        else:

            st.error(
                f"❌ {test_id} — {name} — FAIL"
            )

    st.divider()

    if overall_pass:

        st.success(
            "🎯 OVERALL SYSTEM STATUS: ALL TESTS PASSED"
        )

    else:

        st.error(
            "❌ OVERALL SYSTEM STATUS: SOME TESTS FAILED"
        )


# =========================================================
# EVENT TIMELINE
# =========================================================

elif mode == "📜 Event Timeline":

    st.header("📜 System Event Timeline")

    st.write(
        "Important automation and security events detected "
        "during the complete sensor run."
    )

    important_events = df[
        df["event"] != "Normal sensor reading"
    ]

    for _, row in important_events.iterrows():

        if row["alarm"]:

            st.markdown(
                f"""
                <div class="alert">
                    <b>{row['timestamp']}</b><br>
                    {row['event']}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="event">
                    <b>{row['timestamp']}</b><br>
                    {row['event']}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# RAW DATA
# =========================================================

elif mode == "📡 Raw Data":

    st.header("📡 Raw Sensor Data")

    st.dataframe(
        df[
            [
                "timestamp",
                "temperature",
                "humidity",
                "light",
                "motion",
                "door",
                "rfid_id",
                "voltage",
                "current"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )