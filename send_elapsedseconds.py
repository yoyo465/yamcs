#!/usr/bin/env python3

import struct
import socket
import time
import threading

def build_ccsds_packet(elapsed_seconds, apid=100, seq_count=0):
    version = 0b000
    type_bit = 0b0
    sec_hdr_flag = 0b0
    apid = apid & 0x7FF

    first_2_bytes = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | apid)
    packet_id = struct.pack(">H", first_2_bytes)
    packet_seq = struct.pack(">H", (0b11 << 14) | (seq_count & 0x3FFF))
    pkt_len = struct.pack(">H", 3)  # 4-byte payload minus 1
    payload = struct.pack(">I", elapsed_seconds)
    return packet_id + packet_seq + pkt_len + payload

def send_elapsedseconds_loop(sim_state, host="127.0.0.1", port=10015, delay=1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while True:
            i = sim_state["counter"]
            packet = build_ccsds_packet(elapsed_seconds=i, seq_count=i)
            sock.sendto(packet, (host, port))
            print(f"Sent ElapsedSeconds={i}")
            sim_state["counter"] += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        sock.close()

def listen_for_reset(sim_state, udp_port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", udp_port))
    print(f"[SIM] Listening for RESET on UDP port {udp_port}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip() == b'RESET':
            print("[SIM] RESET received — counter reset to 0")
            sim_state["counter"] = 0

if __name__ == "__main__":
    sim_state = {"counter": 0}
    threading.Thread(target=listen_for_reset, args=(sim_state,), daemon=True).start()
    send_elapsedseconds_loop(sim_state)
