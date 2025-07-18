import time

# Global Variables
oop_file = []
gnss_file = []
oop_update_s_u = "ENABLE_UPDATE_BY_GNSS"  # default action
enable_fdiroot_s_u = "ENABLE"            # default FDIR setting

def prompt(message):
    print("🟢 " + str(message))

def tlm(parameter):
    """Simulasi telemetry dari YAMCS."""
    mock_data = {
        "NST HEALTH_STATUS COLLECTS": 0,
        "NST PARAMS PACKET_TIMEFORMATTED": "2025-07-18T01:46:00Z"
    }
    return mock_data.get(parameter, 0)

def cmd(command):
    """Simulasi command ke sistem."""
    print(f"📤 Command sent: {command}")

def wait(seconds):
    """Delay simulasi"""
    print(f"⏳ Waiting {seconds} seconds...")
    time.sleep(seconds)

# ================== Step Functions ==================

def step1_initialise_procedure():
    prompt("✅ step1_initialise_procedure: OOP action = " + oop_update_s_u)
    prompt("✅ FDIR activation = " + enable_fdiroot_s_u)

def step3_check_cel():
    cel = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step3_check_cel: CEL Status = " + str(cel))
    return cel == 0

def step4_check_gnss_configuration():
    prompt("✅ step4_check_gnss_configuration: GNSS config dummy loaded")
    return True

def step5_check_gnss_status():
    gnss1 = tlm("NST HEALTH_STATUS COLLECTS")
    gnss2 = tlm("NST HEALTH_STATUS COLLECTS")
    prompt(f"✅ step5_check_gnss_status: GNSS1 = {gnss1}, GNSS2 = {gnss2}")
    return True

def step6_check_oop_status():
    cmd("INST CLEAR")
    status = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step6_check_oop_status: OOP Status = " + str(status))
    return status == 0

def step7_check_obcp_is_not_running():
    obcp = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step7_check_obcp_is_not_running: OBCP status = " + str(obcp))
    return obcp == 0

def step8_check_reference_date_consistency():
    prompt("✅ step8_check_reference_date_consistency: Using default reference date")
    return True

def step9_configure_observability():
    tlm("NST HEALTH_STATUS COLLECTS")
    cmd("INST CLEAR")
    prompt("✅ step9_configure_observability: Observability configured")
    return True

def step10_check_gnss_and_oop_fdir_configuration():
    fdir = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step10_check_gnss_and_oop_fdir_configuration: FDIR status = " + str(fdir))
    return fdir == 0

def step11_check_obt_ut():
    obt = tlm("NST PARAMS PACKET_TIMEFORMATTED")
    prompt("✅ step11_check_obt_ut: OBT Time = " + str(obt))
    return True

def step12_disable_oop_update_by_gnss():
    cmd("INST CLEAR")
    flag = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step12_disable_oop_update_by_gnss: Status = " + str(flag))
    wait(2)
    return True

def step13_verify_gnss_validity_flag():
    valid = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step13_verify_gnss_validity_flag: GNSS flag = " + str(valid))
    return valid == 1

def step14_configure_gnss_fdir():
    result = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step14_configure_gnss_fdir: Result = " + str(result))
    return True

def step15_deactivate_oop_fdir():
    cmd("INST CLEAR")
    prompt("✅ step15_deactivate_oop_fdir: FDIR deactivated")
    return True

def step16_authorize_oop_parameters_loading():
    oop = tlm("NST HEALTH_STATUS COLLECTS")
    prompt("✅ step16_authorize_oop_parameters_loading: OOP Phase = " + str(oop))
    return True

def step32_end_of_procedure():
    prompt("✅ step32_end_of_procedure: Procedure finished.")

# ================== MAIN PROCEDURE ==================

def main():
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

# Jalankan saat script dimulai
if __name__ == '__main__':
    main()
