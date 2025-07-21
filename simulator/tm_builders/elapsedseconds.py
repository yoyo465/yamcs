import struct

seq_counter = 0

def build(elapsed):
    global seq_counter

    version = 0      # 3 bits
    type_flag = 0    # TM
    sec_hdr_flag = 1 # present
    apid = 0x100     # 11 bits

    # Compose 16-bit packet ID: version(3) | type(1) | sec hdr(1) | apid(11)
    packet_id = ((version & 0x7) << 13) | ((type_flag & 0x1) << 12) | ((sec_hdr_flag & 0x1) << 11) | (apid & 0x7FF)

    # Sequence flags: 0b11 = standalone
    seq_flags = 0b11 << 14
    seq = seq_flags | (seq_counter & 0x3FFF)
    seq_counter = (seq_counter + 1) % 0x4000  # rollover at 14-bit

    length = 4 - 1  # payload size (4 bytes) - 1

    header = struct.pack(">HHH", packet_id, seq, length)
    payload = struct.pack(">I", elapsed)
    return header + payload
