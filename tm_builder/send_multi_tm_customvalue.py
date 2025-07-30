def listen_for_tc():
    """
    UDP TC handler:
      - payload_len == 3 → Enable/DisableThruster (2B Packet_ID + 1B thruster)
      - payload_len == 6 → SetCustomValue (2B Packet_ID + 4B float)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", TC_PORT))
    print(f"[SIM] Listening for TC on UDP port {TC_PORT}")
    while True:
        data, _ = sock.recvfrom(1024)
        if len(data) < 6:
            continue
        # header
        packet_id, seq, length = struct.unpack(">HHH", data[:6])
        apid = packet_id & 0x07FF
        if apid != CMD_APID:
            continue

        payload_len = length + 1
        payload = data[6:6 + payload_len]

        # ambil Packet_ID (2 byte)
        if payload_len >= 2:
            pkt_arg, = struct.unpack(">H", payload[:2])
        else:
            continue

        # ---- thruster command ----
        if payload_len == 3 and pkt_arg in (10, 11):
            thr_id = payload[2]
            # treat EnableThruster (10) and DisableThruster (11) the same:
            sim_state["thruster_status"] = 1 if thr_id != 0 else 0
            verb = "Enable" if pkt_arg == 10 else "Disable"
            state_str = "ON" if sim_state["thruster_status"] else "OFF"
            print(f"[SIM] TC {verb}Thruster (ID={thr_id}) → status={state_str}")

        # ---- custom value command ----
        elif payload_len == 6 and pkt_arg == 20:
            custom_f, = struct.unpack(">f", payload[2:])
            sim_state["custom_value"] = custom_f
            print(f"[SIM] TC SetCustomValue → custom_value={custom_f:.2f}")

        # lainnya ignore
