#!/usr/bin/env python3
import csv, socket, struct, threading, time

# ─── KONFIGURASI ─────────────────────────────────────────────────────────────
CSV_FILE   = "tm_data.csv"
TM_HOST    = "127.0.0.1"
TM_PORT    = 10015      # Yamcs TM ingestion port
TC_PORT    = 10025      # Yamcs TC dispatch port
RESET_PORT = 12345      # simulasi RESET
DELAY      = 1.0        # detik per TM
CMD_APID   = 101        # APID untuk semua perintah MyProjectPacket
# ────────────────────────────────────────────────────────────────────────────

sim_state = {
    "start_time": time.time(),
    "thruster_status": 0,
    "custom_value": 0.0,      # nilai yang di-set lewat command SetCustomValue
}

def listen_for_reset():
    """UDP RESET handler: kirim 'RESET' untuk restart elapsed."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", RESET_PORT))
    print(f"[SIM] Listening for RESET on UDP port {RESET_PORT}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip().upper() == b"RESET":
            sim_state["start_time"] = time.time()
            print("[SIM] RESET received — ElapsedSeconds restarted")

def listen_for_tc():
    """
    UDP TC handler:
      - payload_len == 1  → Enable/DisableThruster
      - payload_len == 6  → SetCustomValue (2B Packet_ID + 4B float)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", TC_PORT))
    print(f"[SIM] Listening for TC on UDP port {TC_PORT}")
    while True:
        data, _ = sock.recvfrom(1024)
        if len(data) < 6:
            continue

        # unpack primary header (6 bytes)
        packet_id, seq, length = struct.unpack(">HHH", data[:6])
        apid = packet_id & 0x07FF
        if apid != CMD_APID:
            continue

        # hitung dan slice payload
        payload_len = length + 1
        payload = data[6:6 + payload_len]

        # -------------------------
        # 1) Thruster command (1B)
        # -------------------------
        if payload_len == 1:
            thr_arg = payload[0]
            sim_state["thruster_status"] = 1 if thr_arg != 0 else 0
            state_str = "ON" if thr_arg != 0 else "OFF"
            print(f"[SIM] TC Thruster → status={state_str}")

        # -------------------------------------
        # 2) SetCustomValue command (6B total)
        #    [0:2] = Packet_ID (uint16)
        #    [2: ] = CustomValue (float32)
        # -------------------------------------
        elif payload_len == 6:
            pkt_arg, = struct.unpack(">H", payload[:2])
            custom_f, = struct.unpack(">f", payload[2:])
            # packet ID 20 = SetCustomValue
            if pkt_arg == 20:
                sim_state["custom_value"] = custom_f
                print(f"[SIM] TC CustomValue → custom_value={custom_f:.2f}")

def build_packet(seq, elapsed, voltage, enum_val, thruster, custom_value, apid=100):
    """
    Bikin CCSDS TM:
      - uint32 ElapsedSeconds
      - float  Battery1_Voltage
      - uint8  Enum_Para_1
      - uint8  Thruster_Status
      - float  Custom_Value
    """
    version, type_bit, sec_hdr = 0, 0, 0
    packet_id  = (version<<13)|(type_bit<<12)|(sec_hdr<<11)|(apid & 0x07FF)
    packet_seq = (0b11<<14)|(seq & 0x3FFF)

    # payload: 4B uint32, 4B float, 1B enum, 1B thruster, 4B float custom
    payload = struct.pack(
        ">IfBBf",
        int(elapsed),
        voltage,
        enum_val,
        thruster,
        custom_value
    )

    pkt_len = len(payload) - 1
    header  = struct.pack(">HHH", packet_id, packet_seq, pkt_len)
    return header + payload

def main():
    # start background listeners
    threading.Thread(target=listen_for_reset, daemon=True).start()
    threading.Thread(target=listen_for_tc,    daemon=True).start()

    # load CSV sekali saja
    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))

    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    index = 0
    while True:
        row      = rows[index % len(rows)]
        seq      = int(row["seq"])
        voltage  = float(row["BatteryVoltage"])
        enum_val = int(row["EnumPara1"])
        thr_stat = sim_state["thruster_status"]
        custom_v = sim_state["custom_value"]
        elapsed  = time.time() - sim_state["start_time"]

        pkt = build_packet(
            seq,
            elapsed,
            voltage,
            enum_val,
            thr_stat,
            custom_v,
            apid=100
        )
        sock.sendto(pkt, (TM_HOST, TM_PORT))

        print(f"[SIM] Sent TM#{seq} → "
              f"Elapsed={int(elapsed)}, "
              f"V={voltage:.2f}, "
              f"Enum={enum_val}, "
              f"Thr={thr_stat}, "
              f"Custom={custom_v:.2f}")

        index += 1
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
