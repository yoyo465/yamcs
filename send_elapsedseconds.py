#!/usr/bin/env python3

import struct
import socket
import time

def build_ccsds_packet(elapsed_seconds, apid=100):
    version = 0b000
    type_bit = 0b0
    sec_hdr_flag = 0b0
    apid = apid & 0x7FF

    first_2_bytes = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | apid)
    packet_id = struct.pack(">H", first_2_bytes)

    seq_flags = 0b11  # Standalone
    seq_count = 0
    packet_seq = struct.pack(">H", (seq_flags << 14) | seq_count)

    pkt_len = struct.pack(">H", 3)  # 4 bytes payload - 1
    payload = struct.pack(">I", elapsed_seconds)

    return packet_id + packet_seq + pkt_len + payload

def send_elapsedseconds_loop(host="127.0.0.1", port=10015, delay=1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i = 0
    try:
        while True:
            packet = build_ccsds_packet(elapsed_seconds=i)
            sock.sendto(packet, (host, port))
            print(f"Sent ElapsedSeconds={i}")
            i += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    send_elapsedseconds_loop()
