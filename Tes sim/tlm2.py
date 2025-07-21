#!/usr/bin/env python3

import struct
import socket
import time
import threading

# Function to build the CCSDS packet with dynamic parameters
def build_ccsds_packet(parameters, apid=100, seq_count=0):
    version = 0b000
    type_bit = 0b0
    sec_hdr_flag = 0b0
    apid = apid & 0x7FF

    # Construct packet header
    first_2_bytes = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | apid)
    packet_id = struct.pack(">H", first_2_bytes)
    packet_seq = struct.pack(">H", (0b11 << 14) | (seq_count & 0x3FFF))
    
    # Dynamically calculate packet length (header + payload)
    payload = b''
    for param, value in parameters.items():
        if isinstance(value, int):
            payload += struct.pack(">I", value)
        elif isinstance(value, float):
            payload += struct.pack(">f", value)
        elif isinstance(value, bool):
            payload += struct.pack("?", value)

    pkt_len = struct.pack(">H", len(payload) + 3)  # Header size + payload size
    return packet_id + packet_seq + pkt_len + payload

# Function to send telemetry in a loop
def send_telemetry_loop(sim_state, host="127.0.0.1", port=10015, delay=1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while True:
            i = sim_state["counter"]
            # Dynamically create a dictionary of parameters to send
            parameters = {
                "ElapsedSeconds": i,
                "Temperature": 25.0 + (i % 10),  # Just an example for temperature
                "Altitude": 500 + (i % 100),     # Example altitude
                "Velocity": 7.5 + (i % 5),       # Example velocity
                # Add more parameters as needed...
            }
            packet = build_ccsds_packet(parameters, seq_count=i)
            sock.sendto(packet, (host, port))
            print(f"Sent telemetry with ElapsedSeconds={i}, Temperature={parameters['Temperature']}")
            sim_state["counter"] += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        sock.close()

# Function to listen for reset command
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
    send_telemetry_loop(sim_state)
