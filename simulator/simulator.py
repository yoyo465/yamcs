import json
import time
import threading
import socket
from tm_builders import elapsedseconds

DATA_FILE = "data/tm_snapshot.json"
YAMCS_HOST = "127.0.0.1"
YAMCS_PORT = 10015
UDP_RESET_PORT = 12345

def send(packet):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(packet, (YAMCS_HOST, YAMCS_PORT))

def listen_for_reset(state):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_RESET_PORT))
    print(f"[SIM] Listening for RESET on port {UDP_RESET_PORT}")
    while True:
        msg, _ = sock.recvfrom(1024)
        if msg.strip().upper() == b'RESET':
            print("[SIM] RESET received — resetting ElapsedSeconds")
            state["elapsed"] = 0

def main_loop():
    state = {"elapsed": 0}
    threading.Thread(target=listen_for_reset, args=(state,), daemon=True).start()

    while True:
        # update data file
        with open(DATA_FILE, "w") as f:
            json.dump({"ElapsedSeconds": state["elapsed"]}, f, indent=4)

        # build and send telemetry
        packet = elapsedseconds.build(state["elapsed"])
        send(packet)
        print(f"[SIM] Sent ElapsedSeconds={{state['elapsed']}}")
        state["elapsed"] += 1
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
