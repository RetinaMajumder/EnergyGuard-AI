# =========================================================
# EnergyGuard AI – 
# Author: Retina Majumder
# Purpose: Energy monitoring, continuous waste recovery,
# AI-based alerting and recommendations with visualization
# =========================================================

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


# ---------------- GRAPH MODULE ----------------
class EnergyGraph:
    @staticmethod
    def plot(history):
        if len(history.usage_log) < 2:
            return

        plt.figure()
        plt.plot(history.usage_log, label="Total Usage (kWh)")
        plt.plot(history.recovered_log, label="Recovered Energy (kWh)")
        plt.plot(history.remaining_log, label="Unrecovered Waste (kWh)")

        plt.xlabel("Monitoring Step")
        plt.ylabel("Energy (kWh)")
        plt.title("Continuous Waste Recovery Performance")
        plt.legend()
        plt.grid(True)
        plt.show()


# ---------------- DISPLAY ----------------
class AlertDisplay:
    @staticmethod
    def show(alert, score):
        print("\n========== ENERGY STATUS ==========")
        if alert == "CRITICAL":
            print("🔴 CRITICAL – Immediate optimization required")
        elif alert == "WARNING":
            print("🟡 WARNING – Efficiency dropping")
        else:
            print("🟢 NORMAL – System balanced")
        print(f"⚡ Efficiency Score: {score}/100")


# ---------------- MAIN PROGRAM ----------------
def main():
    history = EnergyHistory()
    analytics = EnergyAnalytics()
    ai = KeenAI()

    print("\n=== EnergyGuard AI – Keen Edition V4 ===\n")

    while True:
        try:
            usage = float(input("Energy usage (kWh): "))
            expected = float(input("Expected usage (kWh): "))
            sector = input("Sector (Home / Factory / Power Plant): ")
            time_of_day = input("Time (Day/Night): ")
            sunlight = input("Sunlight available? (yes/no): ").lower() == "yes"
            temperature = float(input("Temperature (°C): "))

            record = EnergyRecord(
                usage, expected, sector, time_of_day, sunlight, temperature
            )

            ratio = analytics.usage_ratio(record)
            anomaly = analytics.detect_anomaly(record, history)
            alert = analytics.alert_level(ratio, anomaly)
            score = analytics.efficiency_score(ratio)
            recovered = analytics.waste_recovery(record)

            history.add(record, recovered[0], recovered[1])

            AlertDisplay.show(alert, score)

            reasons, actions, confidence = ai.analyze(
                record, ratio, anomaly, alert, recovered
            )

            print("\n--- AI DIAGNOSIS ---")
            for r in reasons:
                print("•", r)

            print("\n--- AI ACTION PLAN ---")
            for level, act in actions:
                print(f"[{level}] {act}")

            print(f"\nAI Confidence Level: {confidence}%")

            EnergyGraph.plot(history)

            if input("\nAdd another entry? (yes/no): ").lower() != "yes":
                print("\nSystem shutdown complete. Energy optimized ⚡")
                break

        except ValueError:
            print("\n⚠️ Please enter valid numeric values.\n")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
