import struct
import socket
import time
import threading
import csv
from pathlib import Path

# --- CONFIG ---
CSV_PATH = "tm_data.csv"
YAMCS_HOST = "127.0.0.1"
YAMCS_PORT = 10015
RESET_PORT = 12345
SEND_INTERVAL_SEC = 1.0

# --- State ---
sim_state = {
    "counter": 0,  # for ElapsedSeconds (auto)
    "csv_rows": []
}

# --- CCSDS packet builder ---
def build_ccsds_packet(fields: dict, seq_count: int, apid=100):
    version = 0b000
    type_bit = 0b0
    sec_hdr_flag = 0b0
    apid = apid & 0x7FF

    first_2_bytes = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | apid)
    packet_id = struct.pack(">H", first_2_bytes)
    packet_seq = struct.pack(">H", (0b11 << 14) | (seq_count & 0x3FFF))

    # Build payload based on order of keys
    payload = b""
    for key, val in fields.items():
        if key.lower() == "elapsedseconds":
            payload += struct.pack(">I", int(val))  # 4 bytes
        elif key.lower().startswith("enum"):
            payload += struct.pack("B", int(val) & 0xFF)  # 1 byte
        elif "voltage" in key.lower():
            payload += struct.pack(">f", float(val))  # 4 bytes float
        else:
            payload += struct.pack(">f", float(val))  # default as float

    pkt_len = struct.pack(">H", len(payload) - 1)
    return packet_id + packet_seq + pkt_len + payload

# --- Load CSV ---
def load_csv():
    path = Path(CSV_PATH)
    if not path.exists():
        print(f"❌ CSV not found: {CSV_PATH}")
        return

    with path.open() as f:
        reader = csv.DictReader(f)
        sim_state["csv_rows"] = list(reader)
    print(f"✅ Loaded {len(sim_state['csv_rows'])} rows from CSV")

# --- Reset listener ---
def listen_for_reset():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", RESET_PORT))
    print(f"[SIM] Listening for RESET on UDP port {RESET_PORT}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip() == b'RESET':
            print("[SIM] RESET received — counter reset to 0")
            sim_state["counter"] = 0

# --- Main loop ---
def main_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rows = sim_state["csv_rows"]
    if not rows:
        print("❌ No CSV data loaded. Exiting.")
        return

    try:
        while True:
            idx = sim_state["counter"] % len(rows)
            row = rows[idx].copy()

            # Replace 'auto' with current counter
            for key in row:
                if row[key].strip().lower() == 'auto' and key.lower() == 'elapsedseconds':
                    row[key] = str(sim_state["counter"])

            pkt = build_ccsds_packet(row, seq_count=sim_state["counter"])
            sock.sendto(pkt, (YAMCS_HOST, YAMCS_PORT))
            print(f"[SIM] Sent TM #{sim_state['counter']} -> {row}")

            sim_state["counter"] += 1
            time.sleep(SEND_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("[SIM] Stopped.")
    finally:
        sock.close()

# --- Entry Point ---
if __name__ == "__main__":
    load_csv()
    threading.Thread(target=listen_for_reset, daemon=True).start()
    main_loop()
