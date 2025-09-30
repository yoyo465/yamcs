import time

# --- Utility untuk simulasi log ke Activity Log ---
def log(msg: str):
    print(f"[LOG] {msg}")

def procedure_initialize(apType, name, args=None):
    log(f"Initialize procedure {name} untuk {apType} dengan args={args}")
    return {}

def cleanup(name):
    log(f"Cleanup procedure {name}")

# --- Main procedure ---
def run(apType="SHIP", ARGS=None):
    g = procedure_initialize(apType, "PS6_HOP_DHS_001", ARGS)

    log("=== START: PS6_HOP_DHS_001 ===")

    # Dummy nilai telemetri (contoh simulasi)
    varDH50200 = "GSP1"   # misalnya telemetri ini hasil pembacaan Primary Processor ID
    log(f"Primary Processor ID = {varDH50200}")

    if varDH50200 == "GSP1":
        log("Primary Processor = GSP1, monitoring Processor 1")
        time.sleep(5)  # simulasi tunggu 5 detik (aslinya 300 detik)
        log("Processor 1 health OK → lanjut checkout")
    else:
        log("Primary Processor ≠ GSP1, monitoring Processor 2")
        time.sleep(5)
        log("Processor 2 health OK → lanjut checkout")

    # EEPROM check (dummy)
    eeprom_nominal = True
    log(f"EEPROM image nominal? {eeprom_nominal}")

    cleanup("PS6_HOP_DHS_001")
    log("=== END: PS6_HOP_DHS_001 ===")
