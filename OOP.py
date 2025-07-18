import time
import os

# Global Variables
oop_file = []
gnss_file = []
oop_update_s_u = None
enable_fdiroot_s_u = None

def prompt(message):
    print(message)

def tlm(parameter):
    """Simulasi pengambilan data telemetry (TLMS) berdasarkan parameter."""
    # Ini harus diubah dengan kode yang sesuai untuk mendapatkan telemetry data
    return 0  # Misalnya mengembalikan status OK (0)

def cmd(command):
    """Simulasi pengiriman perintah ke sistem."""
    print(f"Perintah yang dikirim: {command}")

def wait(seconds):
    """Menunggu selama beberapa detik."""
    time.sleep(seconds)

def step1_initialise_procedure():
    """Pilih aksi untuk pembaruan OOP dan aktifkan FDIR."""
    global oop_update_s_u, enable_fdiroot_s_u
    oop_update_s_u = input("Pilih Aksi untuk Pembaruan OOP (ENABLE_UPDATE_BY_GNSS, DISABLE_UPDATE_BY_GNSS, UPDATE_BY_GROUND): ")
    enable_fdiroot_s_u = input("Aktifkan FDIR OOP (ENABLE, DISABLE): ")

# Menghapus step2_set_variables karena berkaitan dengan file XML

def step3_check_cel():
    """Memeriksa status CEL dari simulator di Yamcs."""
    cel_status = tlm("INST HEALTH_STATUS COLLECTS")
    if cel_status != 0:
        return True
    else:
        prompt("Status CEL tidak sesuai!")
        return False

def step4_check_gnss_configuration():
    """Memeriksa file konfigurasi GNSS."""
    prompt("Konfigurasi GNSS: Tidak ada file XML yang diproses.")
    return True

def step5_check_gnss_status():
    """Memeriksa status GNSS dari simulator di Yamcs."""
    gnss_1_status = tlm("NST HEALTH_STATUS COLLECTS")
    gnss_2_status = tlm("NST HEALTH_STATUS COLLECTS")
    if gnss_1_status != 0 and gnss_2_status != 0:
        return True
    else:
        prompt("Status GNSS tidak valid!")
        return False

def step6_check_oop_status():
    """Mengirimkan perintah untuk menghapus status OOP dan memeriksa status."""
    cmd("INST CLEAR")  # Kirim perintah untuk menghapus status
    oop_status = tlm("NST HEALTH_STATUS COLLECTS")
    if oop_status == 0:
        prompt("Status OOP valid.")
        return True
    else:
        prompt("Status OOP tidak valid!")
        return False

def step7_check_obcp_is_not_running():
    """Memeriksa status proses OBC."""
    obc_proc_status = tlm("NST HEALTH_STATUS COLLECTS")
    if obc_proc_status == 0:
        prompt("Proses OBC tidak berjalan.")
        return True
    else:
        prompt("Proses OBC masih berjalan!")
        return False

def step8_check_reference_date_consistency():
    """Memeriksa konsistensi tanggal referensi."""
    prompt("Tanggal Referensi: Tidak ada data dari file XML.")
    return True

def step9_configure_observability():
    """Mengonfigurasi observabilitas berdasarkan bandwidth."""
    observability_status = tlm("NST HEALTH_STATUS COLLECTS")
    cmd("INST CLEAR")  # Mengaktifkan observabilitas
    return True

def step10_check_gnss_and_oop_fdir_configuration():
    """Memeriksa konfigurasi FDIR untuk OOP dan GNSS."""
    fdir_status = tlm("NST HEALTH_STATUS COLLECTS")
    if fdir_status == 0:
        prompt("FDIR konfigurasi valid!")
        return True
    else:
        prompt("FDIR konfigurasi tidak valid!")
        return False

def step11_check_obt_ut():
    """Memeriksa waktu OBT (On-Board Time)."""
    obt_time = tlm("NST PARAMS PACKET_TIMEFORMATTED")
    prompt("Waktu OBT: " + str(obt_time))
    return True

def step12_disable_oop_update_by_gnss():
    """Menonaktifkan pembaruan OOP berdasarkan GNSS."""
    cmd("INST CLEAR")  # Kirim perintah untuk menonaktifkan pembaruan OOP
    gnss_status = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("Status GNSS setelah menonaktifkan: " + str(gnss_status))
    wait(5)
    return True

def step13_verify_gnss_validity_flag():
    """Memverifikasi bendera validitas GNSS."""
    gnss_validity_flag = tlm("NST HEALTH_STATUS COLLECTS")
    if gnss_validity_flag == 1:
        prompt("GNSS validitas terverifikasi.")
        return True
    else:
        prompt("GNSS validitas gagal!")
        return False

def step14_configure_gnss_fdir():
    """Mengonfigurasi FDIR untuk GNSS."""
    gnss_fdir_status = tlm("NST HEALTH_STATUS COLLECTS")
    if gnss_fdir_status == 0:
        prompt("GNSS FDIR konfigurasi berhasil!")
        return True
    else:
        prompt("GNSS FDIR konfigurasi gagal!")
        return False

def step15_deactivate_oop_fdir():
    """Menonaktifkan FDIR untuk OOP."""
    cmd("INST CLEAR")  # Mengirim perintah untuk menonaktifkan FDIR OOP
    return True

def step16_authorize_oop_parameters_loading():
    """Mengotorisasi pemuatan parameter OOP."""
    oop_phase = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("OOP Phase: " + str(oop_phase))
    return True

def step32_end_of_procedure():
    """Prosedur selesai."""
    print("Prosedur selesai")

# Main Procedure
step1_initialise_procedure()
step3_check_cel()
step4_check_gnss_configuration()
step5_check_gnss_status()
step6_check_oop_status()
step7_check_obcp_is_not_running()
step8_check_reference_date_consistency()
step9_configure_observability()
step10_check_gnss_and_oop_fdir_configuration()
step11_check_obt_ut()
step12_disable_oop_update_by_gnss()
step13_verify_gnss_validity_flag()
step14_configure_gnss_fdir()
step15_deactivate_oop_fdir()
step16_authorize_oop_parameters_loading()
step32_end_of_procedure()
