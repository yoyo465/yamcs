#!/usr/bin/env python3
import csv, socket, struct, threading, time

# ─── KONFIGURASI ─────────────────────────────────────────────────────────────
CSV_FILE      = "tm_data.csv"
TM_HOST       = "127.0.0.1"
TM_PORT       = 10015    # Yamcs TM ingestion port
TC_PORT       = 10025    # Yamcs TC dispatch port
RESET_PORT    = 12345    # simulasi RESET
DELAY         = 1.0      # detik per TM
CMD_APID      = 101      # APID untuk semua TC MyProjectPacket
# ────────────────────────────────────────────────────────────────────────────

sim_state = {
    "start_time": time.time(),
    "thruster_status": 0,
    "custom_value": 0.0,    # ← nilai float yang di-set via command
}

def listen_for_reset():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", RESET_PORT))
    print(f"[SIM] Listening for RESET on UDP port {RESET_PORT}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip().upper() == b"RESET":
            sim_state["start_time"] = time.time()
            print("[SIM] RESET received — ElapsedSeconds restarted")

def listen_for_tc():
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

        # ambil payload: panjang = length+1
        payload = data[6 : 6 + (length + 1)]
        # TC 1-byte → thruster; TC 4-byte → custom float
        if len(payload) == 1:
            thr_arg = payload[0]
            sim_state["thruster_status"] = 1 if thr_arg != 0 else 0
            state_str = "ON" if sim_state["thruster_status"] else "OFF"
            print(f"[SIM] TC Thruster (APID=0x{apid:03X}) → status={state_str}")

        elif len(payload) == 4:
            custom_f, = struct.unpack(">f", payload)
            sim_state["custom_value"] = custom_f
            print(f"[SIM] TC CustomValue (APID=0x{apid:03X}) → custom_value={custom_f:.2f}")

def build_packet(seq, elapsed, voltage, enum_val, thruster, custom_value, apid=100):
    """
    Bikin CCSDS TM:
    - uint32 elapsed
    - float  voltage
    - uint8  enum_val
    - uint8  thruster
    - float  custom_value
    """
    # primary header
    version, type_bit, sec_hdr = 0, 0, 0
    packet_id  = (version<<13)|(type_bit<<12)|(sec_hdr<<11)|(apid&0x7FF)
    packet_seq = (0b11<<14)|(seq&0x3FFF)

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
    # start listeners
    threading.Thread(target=listen_for_reset, daemon=True).start()
    threading.Thread(target=listen_for_tc,    daemon=True).start()

    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))

    sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    index = 0
    while True:
        row       = rows[index % len(rows)]
        seq       = int(row["seq"])
        voltage   = float(row["BatteryVoltage"])
        enum_val  = int(row["EnumPara1"])
        thr_stat  = sim_state["thruster_status"]
        elapsed   = time.time() - sim_state["start_time"]
        custom_v  = sim_state["custom_value"]

        pkt = build_packet(
            seq, elapsed,
            voltage,
            enum_val,
            thr_stat,
            custom_v,
            apid=100
        )
        sock.sendto(pkt, (TM_HOST, TM_PORT))

        print(f"[SIM] Sent TM#{seq} → Elapsed={int(elapsed)}, "
              f"V={voltage:.2f}, Enum={enum_val}, Thr={thr_stat}, "
              f"Custom={custom_v:.2f}")

        index += 1
        time.sleep(DELAY)

if __name__ == "__main__":
    main()
