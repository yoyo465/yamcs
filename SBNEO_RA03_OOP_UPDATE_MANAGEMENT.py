def initialise_procedure():
    print("✅ initialise_procedure: Start OOP management sequence")

def set_variables():
    voltage = tlm("Battery1_Voltage")
    temp = tlm("Battery1_Temp")
    print(f"🔋 Battery 1: Voltage = {voltage} V, Temp = {temp} °C")

def check_cel():
    cel_status = tlm("CDHS_Error_Flag")
    print(f"🧠 CDHS Error Flag: {cel_status}")
    if cel_status:
        print("⚠️ Warning: CDHS Error is active!")

def check_gnss_configuration():
    print("🛰️ GNSS configuration: not available in current telemetry")

def check_gnss_status():
    sunsensor = tlm("Sunsensor")
    print(f"🛰️ GNSS/Sunsensor value: {sunsensor}")

def check_oop_status():
    status = tlm("Payload_Error_Flag")
    print(f"📡 OOP Payload Error Flag: {status}")
    if status:
        print("⚠️ Payload Error Flag is TRUE!")

def check_obcp_is_not_running():
    mode = tlm("Mode_Safe")
    print(f"🧪 Safe Mode Active: {mode}")
    if mode:
        print("⚠️ Warning: System is in Safe Mode!")

def check_reference_date_consistency():
    ref_date = tlm("EpochUSNO")
    print(f"📅 Reference Epoch USNO: {ref_date}")

def configure_observability():
    status = tlm("Mode_Payload")
    print(f"🔍 Observability Mode Payload: {status}")

def check_gnss_and_oop_fdir_configuration():
    oop_fdir = tlm("EPS_Error_Flag")
    print(f"🛠️ OOP FDIR Status: {oop_fdir}")

def check_obt_ut():
    elapsed = tlm("ElapsedSeconds")
    print(f"⏱️ Elapsed Seconds: {elapsed}")

def disable_oop_update_by_gnss():
    print("🛑 Simulating disable OOP update by GNSS...")

def verify_gnss_validity_flag():
    lat = tlm("Latitude")
    lon = tlm("Longitude")
    print(f"🌐 GNSS Position: Latitude = {lat}, Longitude = {lon}")

def configure_gnss_fdir():
    print("⚙️ GNSS FDIR configured (simulated)")

def deactivate_oop_fdir():
    print("🛑 OOP FDIR deactivated (simulated)")

def authorize_oop_parameters_loading():
    print("🔓 OOP parameter loading authorized")

def load_oop_parameters():
    print("📦 Loading OOP parameters from XML (simulated)")

def wait_reference_date():
    print("⏳ Waiting for reference date... (simulated delay)")

def verify_uploaded_parameters_in_open_mode():
    print("📋 Verifying uploaded OOP parameters in open mode")

def check_current_nominal_longitude():
    lon = tlm("Longitude")
    print(f"🧭 Current Nominal Longitude: {lon}")

def check_aj_nominal_longitude():
    print("🧭 AJ Nominal Longitude check (placeholder)")

def flush_sgm_eeprom():
    print("💾 EEPROM flush simulated")

def update_current_nominal_longitude():
    print("📍 Update current nominal longitude")

def update_aj_nominal_longitude():
    print("📍 Update AJ nominal longitude")

def write_in_sgm_eeprom():
    print("📝 Writing data into SGM EEPROM...")

def update_oop_fdir_parameters():
    print("🛠️ Updating OOP FDIR parameters...")

def configure_oop_with_new_parameters():
    print("🆕 Applying new OOP parameters")

def configure_oop_with_current_parameters():
    print("🔁 Reapplying current OOP parameters")

def enable_update_by_gnss():
    print("✅ Enabling update by GNSS")

def activate_oop_fdir():
    print("🚀 Activating OOP FDIR logic")

def restore_observability():
    print("🔄 Restoring system observability")

def end_of_procedure():
    print("✅ Procedure complete! All steps executed.")

# Optional simulation fallback
def tlm(param):
    dummy_data = {
        "Battery1_Voltage": 20.004,
        "Battery1_Temp": 4.5,
        "CDHS_Error_Flag": False,
        "Payload_Error_Flag": False,
        "Mode_Safe": False,
        "EpochUSNO": 57388.117,
        "ElapsedSeconds": 9952,
        "EPS_Error_Flag": False,
        "Latitude": -50.770676,
        "Longitude": 98.226654,
        "Sunsensor": 960.01904,
        "Mode_Payload": False,
    }
    return dummy_data.get(param, "N/A")

def main():
    initialise_procedure()
    set_variables()
    check_cel()
    check_gnss_configuration()
    check_gnss_status()
    check_oop_status()
    check_obcp_is_not_running()
    check_reference_date_consistency()
    configure_observability()
    check_gnss_and_oop_fdir_configuration()
    check_obt_ut()
    disable_oop_update_by_gnss()
    verify_gnss_validity_flag()
    configure_gnss_fdir()
    deactivate_oop_fdir()
    authorize_oop_parameters_loading()
    load_oop_parameters()
    wait_reference_date()
    verify_uploaded_parameters_in_open_mode()
    check_current_nominal_longitude()
    check_aj_nominal_longitude()
    flush_sgm_eeprom()
    update_current_nominal_longitude()
    update_aj_nominal_longitude()
    write_in_sgm_eeprom()
    update_oop_fdir_parameters()
    configure_oop_with_new_parameters()
    configure_oop_with_current_parameters()
    enable_update_by_gnss()
    activate_oop_fdir()
    restore_observability()
    end_of_procedure()

if __name__ == '__main__':
    main()
