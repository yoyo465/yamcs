# File: PS6_HOP_DHS_001.py
import time

# ------------------------------------------------------------------------
# Stub fungsi helper (kalau belum ada di sistem Anda)
# Bisa diganti implementasi asli sesuai kebutuhan
# ------------------------------------------------------------------------
def procedure_initialize(apType, procName, ARGS):
    return {}

def mainStepFlowControl(stepId, stepName, g):
    pass

def stepFlowControl(stepId, stepName, g):
    pass

def branchCntrl(g, stepA, stepB, defaultStep):
    return defaultStep

def cleanup(procName):
    pass

# ------------------------------------------------------------------------
# Main Procedure (versi clean tanpa Procedure/prompt)
# ------------------------------------------------------------------------
def run(apType="SHIP", ARGS=None):
    g = procedure_initialize(apType, "PS6_HOP_DHS_001", ARGS)

    log("START: PS6_HOP_DHS_001")

    # Cek Primary Processor
    varDH50200 = get_value("T DH50200 Primary Processor ID")
    if varDH50200 == "GSP1":
        log("Primary Processor = GSP1, lanjut cek Processor 1")
        # Monitor Processor 1
        log("Monitoring Processor 1 health status selama 5 menit")
        time.sleep(300)

        # Cek health (dummy check → silakan ganti dengan logika TM real)
        health_ok = True
        if health_ok:
            log("Processor 1 health OK → lanjut ke Checkout")
            # Panggil prosedur lain jika perlu
            # send_command("CMD.PROCESSOR1_CHECKOUT")
        else:
            log("Processor 1 health NOT OK → Contingency Meeting")
            return
    else:
        log("Primary Processor ≠ GSP1, lanjut cek Processor 2")
        # Monitor Processor 2
        log("Monitoring Processor 2 health status selama 5 menit")
        time.sleep(300)

        # Cek health (dummy check)
        health_ok = True
        if health_ok:
            log("Processor 2 health OK → lanjut ke Checkout")
            # send_command("CMD.PROCESSOR2_CHECKOUT")
        else:
            log("Processor 2 health NOT OK → Contingency Meeting")
            return

    # EEPROM check (contoh otomatis → tanpa prompt)
    eeprom_nominal = True
    if eeprom_nominal:
        log("EEPROM image nominal → prosedur selesai normal")
    else:
        log("EEPROM image TIDAK nominal → Contingency Meeting")

    cleanup("PS6_HOP_DHS_001")
    log("END: PS6_HOP_DHS_001")
