#!/usr/bin/env python3

import struct
import socket
import time

def build_ccsds_packet(elapsed_seconds, apid=100):
    # CCSDS Primary Header (6 bytes)
    version = 0b000         # 3 bits
    type_bit = 0b0          # 1 bit (TM)
    sec_hdr_flag = 0b0      # 1 bit
    apid = apid & 0x7FF     # 11 bits

    first_2_bytes = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | apid)
    packet_id = struct.pack(">H", first_2_bytes)

    seq_flags = 0b11  # Standalone
    seq_count = 0     # Fixed for testing
    packet_seq = struct.pack(">H", (seq_flags << 14) | seq_count)

    payload_length = 4  # ElapsedSeconds = 4 bytes
    pkt_len = struct.pack(">H", payload_length - 1)

    payload = struct.pack(">I", elapsed_seconds)

    return packet_id + packet_seq + pkt_len + payload

def send_elapsedseconds_packets(host="127.0.0.1", port=10015, count=20, delay=1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(count):
        packet = build_ccsds_packet(elapsed_seconds=i)
        sock.sendto(packet, (host, port))
        print(f"Sent ElapsedSeconds={i}")
        time.sleep(delay)
    sock.close()

if __name__ == "__main__":
    send_elapsedseconds_packets()
