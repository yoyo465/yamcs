import socket
import time

SIMULATOR_HOST = "localhost"
SIMULATOR_PORT = 12345
TEST_MESSAGE = b"PING"
TIMEOUT = 1.0  # detik

def test_connection():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TIMEOUT)
        sock.sendto(TEST_MESSAGE, (SIMULATOR_HOST, SIMULATOR_PORT))

        # Coba tunggu respons PING balik jika simulator mendukung
        try:
            data, _ = sock.recvfrom(1024)
            if data.strip() == b"PONG":
                print("✅ Terhubung dengan simulator (respon PONG diterima)")
            else:
                print(f"⚠️ Respon tidak dikenal: {data}")
        except socket.timeout:
            print("✅ UDP terkirim — tidak ada respon (simulator mode 1 arah)")

        sock.close()
        return True

    except Exception as e:
        print("❌ Tidak dapat terhubung ke simulator:", str(e))
        return False


def send_reset():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'RESET', (SIMULATOR_HOST, SIMULATOR_PORT))
        sock.close()
        print("✅ RESET command sent to simulator")
    except Exception as e:
        print("❌ ERROR saat kirim RESET:", str(e))


def run():
    print("[INFO] Menguji koneksi ke simulator...")
    if test_connection():
        time.sleep(0.5)
        print("[INFO] Mengirim perintah RESET...")
        send_reset()
    else:
        print("❌ Gagal: Simulator tidak merespons, RESET dibatalkan.")


if __name__ == "__main__":
    run()
