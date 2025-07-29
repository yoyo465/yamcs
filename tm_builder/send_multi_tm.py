#!/usr/bin/env python3

import csv
import socket
import struct
import threading
import time

CSV_FILE = "tm_data.csv"
TM_HOST = "127.0.0.1"
TM_PORT = 10015
RESET_PORT = 12345
DELAY = 1.0  # seconds

sim_state = {
    "reset": False,
    "start_time": time.time()
}

def build_packet(seq, elapsed, voltage, enum_val, thruster_status, apid=100):
    version = 0b000
    type_bit = 0
    sec_hdr_flag = 0
    packet_id = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | (apid & 0x7FF))
    packet_seq = ((0b11 << 14) | (seq & 0x3FFF))
    payload = struct.pack(">IfBB", int(elapsed), voltage, enum_val,thruster_status)
    pkt_len = len(payload) - 1
    header = struct.pack(">HHH", packet_id, packet_seq, pkt_len)
    return header + payload

def listen_for_reset():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", RESET_PORT))
    print(f"[SIM] Listening for RESET on UDP port {RESET_PORT}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip().upper() == b"RESET":
            sim_state["reset"] = True
            sim_state["start_time"] = time.time()
            print("[SIM] RESET received — ElapsedSeconds restarted")

def main_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(CSV_FILE) as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    index = 0
    while True:
        row = rows[index % len(rows)]
        seq = int(row["seq"])
        voltage = float(row["BatteryVoltage"])
        enum_val = int(row["EnumPara1"])
        thr_stat = int(row["ThrusterStatus"])

        elapsed = time.time() - sim_state["start_time"]
        packet = build_packet(seq, elapsed, voltage, enum_val,thr_stat)
        sock.sendto(packet, (TM_HOST, TM_PORT))

        print(f"[SIM] Sent TM #{seq} -> Elapsed={int(elapsed)}, V={voltage}, Enum={enum_val}, Thr_stat={thr_stat}")

        index += 1
        time.sleep(DELAY)

if __name__ == "__main__":
    threading.Thread(target=listen_for_reset, daemon=True).start()
    main_loop()
