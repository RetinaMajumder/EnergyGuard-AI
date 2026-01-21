import streamlit as st
import matplotlib.pyplot as plt

# ---------------- ENERGY RECORD ----------------
class EnergyRecord:
    def __init__(self, usage, expected, sector, time_of_day, sunlight, temperature):
        self.usage = usage              # kWh
        self.expected = expected        # kWh
        self.sector = sector            # Home / Factory / Power Plant
        self.time_of_day = time_of_day  # Day / Night
        self.sunlight = sunlight        # Boolean
        self.temperature = temperature  # Celsius

# ---------------- HISTORY MODULE ----------------
class EnergyHistory:
    def __init__(self):
        self.records = []
        self.usage_log = []
        self.recovered_log = []
        self.remaining_log = []

    def add(self, record, recovered, remaining):
        self.records.append(record)
        self.usage_log.append(record.usage)
        self.recovered_log.append(recovered)
        self.remaining_log.append(remaining)

    def last_usage(self):
        if not self.records:
            return None
        return self.records[-1].usage

# ---------------- ANALYTICS MODULE ----------------
class EnergyAnalytics:

    @staticmethod
    def usage_ratio(record):
        return record.usage / record.expected

    @staticmethod
    def detect_anomaly(record, history):
        last = history.last_usage()
        if last is None:
            return False
        return record.usage > last * 1.25  # 25% spike

    @staticmethod
    def alert_level(ratio, anomaly):
        if ratio >= 1.35 or anomaly:
            return "CRITICAL"
        elif ratio >= 1.15:
            return "WARNING"
        return "NORMAL"

    @staticmethod
    def efficiency_score(ratio):
        score = 100 - abs(ratio - 1) * 75
        return round(max(0, min(100, score)), 1)

    @staticmethod
    def waste_recovery(record):
        wasted = 0.30 * record.usage
        recovered = 0.80 * wasted          # Always ON
        remaining = wasted - recovered     # System efficiency
        return round(recovered, 2), round(remaining, 2)

# ---------------- AI DECISION ENGINE ----------------
class KeenAI:
    def analyze(self, record, ratio, anomaly, alert, recovered):
        reasons = []
        actions = []
        confidence = 30

        reasons.append(f"Energy usage is {ratio:.2f}× expected")

        if anomaly:
            reasons.append("Sudden abnormal spike detected")
            confidence += 15

        if record.temperature > 30:
            reasons.append("High temperature increased cooling demand")
            confidence += 10

        if record.sunlight and record.time_of_day.lower() == "day":
            reasons.append("Sunlight available but underutilized")
            confidence += 15

        if record.sector.lower() in ["factory", "power plant"]:
            reasons.append("High recoverable industrial losses")
            confidence += 15

        # Continuous recovery (Second Line)
        actions.append(("HIGH", f"Recover wasted electricity continuously (~{recovered[0]} kWh)"))
        actions.append(("HIGH", f"Reserved for system stability (~{recovered[1]} kWh)"))

        # Null Line (only on anomaly)
        if anomaly:
            actions.append(("IMMEDIATE", "Activate Null Line to capture leakage"))

        if alert == "CRITICAL":
            actions.append(("IMMEDIATE", "Reduce non-essential loads"))
            actions.append(("HIGH", "Shift base load to geothermal / renewable"))
            if record.sunlight:
                actions.append(("IMMEDIATE", "Activate Smart Daylight-Mirroring System"))

        elif alert == "WARNING":
            actions.append(("MEDIUM", "Optimize operating schedule"))

        else:
            actions.append(("LOW", "System operating optimally"))

        return reasons, actions, min(100, confidence)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="EnergyGuard AI – Keen Edition V4", page_icon="⚡", layout="wide")
st.title("⚡ EnergyGuard AI – Keen Edition V4")
st.write("Monitor and optimize energy usage with AI-driven insights.")

# Persist history between entries
if "history" not in st.session_state:
    st.session_state.history = EnergyHistory()

analytics = EnergyAnalytics()
ai = KeenAI()

# ---------------- INPUT FORM ----------------
with st.form("energy_input"):
    st.subheader("Enter Energy Data")
    usage = st.number_input("Energy usage (kWh):", min_value=0.0, step=0.1)
    expected = st.number_input("Expected usage (kWh):", min_value=0.0, step=0.1)
    sector = st.selectbox("Sector:", ["Home", "Factory", "Power Plant"])
    time_of_day = st.selectbox("Time of Day:", ["Day", "Night"])
    sunlight = st.checkbox("Sunlight available?")
    temperature = st.number_input("Temperature (°C):", step=0.1)
    submitted = st.form_submit_button("Analyze Energy")

if submitted:
    record = EnergyRecord(usage, expected, sector, time_of_day, sunlight, temperature)

    ratio = analytics.usage_ratio(record)
    anomaly = analytics.detect_anomaly(record, st.session_state.history)
    alert = analytics.alert_level(ratio, anomaly)
    score = analytics.efficiency_score(ratio)
    recovered = analytics.waste_recovery(record)

    st.session_state.history.add(record, recovered[0], recovered[1])

    # ---------------- DISPLAY ALERT ----------------
    st.subheader("🔔 Energy Status")
    if alert == "CRITICAL":
        st.error("🔴 CRITICAL – Immediate optimization required")
    elif alert == "WARNING":
        st.warning("🟡 WARNING – Efficiency dropping")
    else:
        st.success("🟢 NORMAL – System balanced")

    st.write(f"⚡ Efficiency Score: {score}/100")

    # ---------------- AI DIAGNOSIS ----------------
    reasons, actions, confidence = ai.analyze(record, ratio, anomaly, alert, recovered)

    st.subheader("🤖 AI Diagnosis")
    for r in reasons:
        st.write("•", r)

    st.subheader("🛠️ AI Action Plan")
    for level, act in actions:
        st.write(f"[{level}] {act}")

    st.write(f"AI Confidence Level: {confidence}%")

    # ---------------- PLOT ----------------
    if len(st.session_state.history.usage_log) >= 2:
        st.subheader("📈 Continuous Waste Recovery Performance")
        fig, ax = plt.subplots()
        ax.plot(st.session_state.history.usage_log, label="Total Usage (kWh)")
        ax.plot(st.session_state.history.recovered_log, label="Recovered Energy (kWh)")
        ax.plot(st.session_state.history.remaining_log, label="Unrecovered Waste (kWh)")
        ax.set_xlabel("Monitoring Step")
        ax.set_ylabel("Energy (kWh)")
        ax.set_title("Continuous Waste Recovery Performance")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
