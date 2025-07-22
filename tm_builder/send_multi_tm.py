#!/usr/bin/env python3

import csv
import socket
import struct
import time

def build_packet(seq, elapsed, voltage, enum_val, apid=100):
    version = 0b000
    type_bit = 0
    sec_hdr_flag = 0
    packet_id = ((version << 13) | (type_bit << 12) | (sec_hdr_flag << 11) | (apid & 0x7FF))
    packet_seq = ((0b11 << 14) | (seq & 0x3FFF))
    payload = struct.pack(">IfB", elapsed, voltage, enum_val)  # 4+4+1 bytes
    pkt_len = len(payload) - 1
    header = struct.pack(">HHH", packet_id, packet_seq, pkt_len)
    return header + payload

def main():
    with open("tm_data.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("127.0.0.1", 10015)

    for row in rows:
        seq = int(row["seq"])
        elapsed = int(row["ElapsedSe"])
        voltage = float(row["BatteryVol"])
        enum_val = int(row["EnumPara1"])

        packet = build_packet(seq, elapsed, voltage, enum_val)
        sock.sendto(packet, addr)
        print(f"[SIM] Sent TM #{seq} -> {row}")
        time.sleep(1)

if __name__ == "__main__":
    main()
