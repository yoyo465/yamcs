import socket
import struct
import time
import os
import random
from threading import Thread
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Config ---
TM_HOST = "127.0.0.1"
TM_PORT = 10055
TC_HOST = "127.0.0.1"
TC_PORT = 10065

tm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tc_socket.bind((TC_HOST, TC_PORT))

# --- Build CCSDS-like packet ---
def build_tm_packet(version, type_, sec_hdr_flag, apid, group_flags, seq_count,
                    mode_adcs, mode_obsw, mode_fdir,
                    v_bat, i_bat, temp1, temp2, temp3, temp4,
                    roll, pitch, yaw):

    primary_header_1 = ((version & 0x7) << 13) | ((type_ & 0x1) << 12) | \
                       ((sec_hdr_flag & 0x1) << 11) | (apid & 0x7FF)
    primary_header_2 = ((group_flags & 0x3) << 14) | (seq_count & 0x3FFF)

    payload = struct.pack(">BBBfffffffff",
                          mode_adcs, mode_obsw, mode_fdir,
                          v_bat, i_bat, temp1, temp2, temp3, temp4,
                          roll, pitch, yaw)

    payload_length = len(payload)
    packet_length = payload_length + 7 - 1   # CCSDS: total - 1
    header = struct.pack(">HHH", primary_header_1, primary_header_2, packet_length)

    return header + payload


# --- TM Thread (generate random telemetry) ---
class TMThread(Thread):
    def __init__(self):
        super().__init__()
        self.seq = 0
        self.last_packet_info = ""

    def run(self):
        while True:
            mode_adcs = random.randint(0, 5)
            mode_obsw = random.randint(0, 2)
            mode_fdir = random.randint(0, 2)
            v_bat = random.uniform(3.0, 4.2)
            i_bat = random.uniform(0.0, 2.0)
            temp1 = random.uniform(-20.0, 80.0)
            temp2 = random.uniform(-20.0, 80.0)
            temp3 = random.uniform(-20.0, 80.0)
            temp4 = random.uniform(-20.0, 80.0)
            roll = random.uniform(-180, 180)
            pitch = random.uniform(-90, 90)
            yaw = random.uniform(-150, 150)

            packet = build_tm_packet(
                0, 0, 0, 110, 3, self.seq,
                mode_adcs, mode_obsw, mode_fdir,
                v_bat, i_bat, temp1, temp2, temp3, temp4,
                roll, pitch, yaw
            )

            tm_socket.sendto(packet, (TM_HOST, TM_PORT))

            # simpan info terakhir untuk ditampilkan di GUI
            self.last_packet_info = (
                f"SEQ={self.seq} | ADCS={mode_adcs} OBSW={mode_obsw} FDIR={mode_fdir}\n"
                f"Vbat={v_bat:.2f}V Ibat={i_bat:.2f}A\n"
                f"T1={temp1:.1f}°C T2={temp2:.1f}°C "
                f"T3={temp3:.1f}°C T4={temp4:.1f}°C\n"
                f"Roll={roll:.1f} Pitch={pitch:.1f} Yaw={yaw:.1f}"
            )

            self.seq = (self.seq + 1) & 0x3FFF  # wrap ke 14 bit
            time.sleep(1)


# --- GUI ---
class App:
    def __init__(self, root, tm_thread):
        self.tm = tm_thread
        self.root = root
        root.title("Satellite Telemetry Viewer")
        root.geometry("650x480")
        root.resizable(False, False)
        root.configure(bg="black")

        # Gambar satelit di tengah
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(script_dir, "satellite.png")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            self.sat_img = ImageTk.PhotoImage(img)
            self.image_label = tk.Label(root, image=self.sat_img, bg="black")
            self.image_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Label info
        self.info_label = tk.Label(root, text="Waiting TM...", fg="white", bg="black",
                                   font=("Courier", 12), justify="left")
        self.info_label.pack(side=tk.BOTTOM, pady=20)

        self.update_ui()

    def update_ui(self):
        # ambil info terbaru dari TMThread
        self.info_label.config(text=self.tm.last_packet_info)
        self.root.after(1000, self.update_ui)


# --- Run ---
tm_thread = TMThread()
tm_thread.daemon = True
tm_thread.start()

root = tk.Tk()
app = App(root, tm_thread)
root.mainloop()

