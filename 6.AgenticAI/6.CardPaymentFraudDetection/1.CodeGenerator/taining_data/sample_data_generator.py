"""
Rule-Book Compatible Fraud Data Generator
-----------------------------------------

Output:
    rule_compatible_fraud_data.csv

Purpose:
    - Rule engine testing
    - Rule backtesting
    - Fraud QA

Fraud rate:
    ~3%
"""

import random
import csv
from tqdm import tqdm

# ---------------- CONFIG ----------------

OUTPUT_FILE = "rule_compatible_fraud_data.csv"
TOTAL_ROWS = 1_000_000
FRAUD_RATE = 0.03

random.seed(42)

# ---------------- HELPERS ----------------

def rand_bool(p=0.5):
    return random.random() < p

# ---------------- GENUINE ROW ----------------

def generate_genuine(i):
    return {
        "transaction_id": f"txn_{i}",
        "time_since_block": random.randint(1000, 50000),
        "txn_velocity_5m": random.randint(0, 2),
        "geo_distance_km": random.randint(0, 10),
        "hour_of_day": random.randint(8, 21),
        "otp_result": True,
        "vpn_detected": False,
        "mcc_risk_score": random.randint(1, 4),
        "sim_swap_days": random.randint(90, 1000),
        "profile_change_recency": random.randint(30, 1000),
        "wallet_age_minutes": random.randint(5000, 50000),
        "txn_density": random.uniform(0.1, 0.5),
        "is_first_international": False,
        "time_gap": random.randint(60, 600),
        "wallets_per_card": random.randint(1, 2),
        "atm_risk_score": random.randint(1, 4),
        "pos_decline_then_atm": False,
        "cvv_fail_rate": random.randint(0, 1),
        "expiry_fail_pattern": random.randint(0, 1),
        "screen_overlay_detected": False,
        "keylogger_detected": False,
        "suspicious_app_usage": False,
        "refund_card_mismatch": False,
        "refund_without_sale": False,
        "refund_latency": random.randint(10, 500),
        "salary_cycle_deviation": random.uniform(0.5, 1.2),
        "mcc_entropy": random.uniform(0.1, 0.5),
        "app_inactive_days": random.randint(0, 3),
        "peer_spend_zscore": random.uniform(0.1, 1.5),
        "offline_contactless": False,
        "card_age_days": random.randint(100, 5000),
        "credit_history_length": random.randint(2, 20),
        "amount_spike_ratio": random.uniform(0.8, 1.2),
        "label": 0
    }

# ---------------- FRAUD ROW ----------------

def generate_fraud(i):
    rule_choice = random.choice([
        "stolen", "cnp", "identity", "velocity", "atm",
        "bin", "malware", "refund", "behavioral", "synthetic"
    ])

    row = generate_genuine(i)
    row["label"] = 1

    if rule_choice == "stolen":
        row["time_since_block"] = random.randint(0, 4)
        row["txn_velocity_5m"] = random.randint(5, 10)

    elif rule_choice == "cnp":
        row["otp_result"] = False
        row["vpn_detected"] = True
        row["mcc_risk_score"] = random.randint(8, 10)

    elif rule_choice == "identity":
        row["sim_swap_days"] = random.randint(0, 10)
        row["profile_change_recency"] = random.randint(0, 5)
        row["wallet_age_minutes"] = random.randint(0, 30)

    elif rule_choice == "velocity":
        row["hour_of_day"] = random.randint(22, 23)
        row["txn_density"] = random.uniform(1.5, 3.0)

    elif rule_choice == "atm":
        row["atm_risk_score"] = random.randint(8, 10)
        row["pos_decline_then_atm"] = True

    elif rule_choice == "bin":
        row["cvv_fail_rate"] = random.randint(4, 10)
        row["expiry_fail_pattern"] = random.randint(4, 10)

    elif rule_choice == "malware":
        row["screen_overlay_detected"] = True
        row["keylogger_detected"] = True

    elif rule_choice == "refund":
        row["refund_card_mismatch"] = True
        row["refund_without_sale"] = True
        row["refund_latency"] = random.randint(0, 1)

    elif rule_choice == "behavioral":
        row["salary_cycle_deviation"] = random.uniform(2.0, 4.0)
        row["mcc_entropy"] = random.uniform(0.8, 1.0)
        row["peer_spend_zscore"] = random.uniform(2.5, 5.0)

    elif rule_choice == "synthetic":
        row["card_age_days"] = random.randint(1, 20)
        row["credit_history_length"] = 0
        row["amount_spike_ratio"] = random.uniform(2.0, 6.0)

    return row

# ---------------- GENERATION ----------------

def generate_dataset():
    fraud_rows = int(TOTAL_ROWS * FRAUD_RATE)
    genuine_rows = TOTAL_ROWS - fraud_rows
    rows = []

    print(f"Generating {genuine_rows} genuine rows...")
    for i in tqdm(range(genuine_rows)):
        rows.append(generate_genuine(i))

    print(f"Generating {fraud_rows} fraud rows...")
    for i in tqdm(range(genuine_rows, TOTAL_ROWS)):
        rows.append(generate_fraud(i))

    random.shuffle(rows)
    return rows

# ---------------- WRITE CSV ----------------

def write_csv(rows):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Written: {OUTPUT_FILE}")
    print(f"📊 Total rows: {len(rows)}")
    print(f"🚨 Fraud rows: {sum(r['label'] for r in rows)}")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    data = generate_dataset()
    write_csv(data)
