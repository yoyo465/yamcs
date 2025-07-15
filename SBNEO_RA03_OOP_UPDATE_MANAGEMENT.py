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


def initialise_procedure():
    print("✅ Running step: initialise_procedure")

def set_variables():
    print("✅ Running step: set_variables")

def check_cel():
    print("✅ Running step: check_cel")

def check_gnss_configuration():
    print("✅ Running step: check_gnss_configuration")

def check_gnss_status():
    print("✅ Running step: check_gnss_status")

def check_oop_status():
    print("✅ Running step: check_oop_status")

def check_obcp_is_not_running():
    print("✅ Running step: check_obcp_is_not_running")

def check_reference_date_consistency():
    print("✅ Running step: check_reference_date_consistency")

def configure_observability():
    print("✅ Running step: configure_observability")

def check_gnss_and_oop_fdir_configuration():
    print("✅ Running step: check_gnss_and_oop_fdir_configuration")

def check_obt_ut():
    print("✅ Running step: check_obt_ut")

def disable_oop_update_by_gnss():
    print("✅ Running step: disable_oop_update_by_gnss")

def verify_gnss_validity_flag():
    print("✅ Running step: verify_gnss_validity_flag")

def configure_gnss_fdir():
    print("✅ Running step: configure_gnss_fdir")

def deactivate_oop_fdir():
    print("✅ Running step: deactivate_oop_fdir")

def authorize_oop_parameters_loading():
    print("✅ Running step: authorize_oop_parameters_loading")

def load_oop_parameters():
    print("✅ Running step: load_oop_parameters")

def wait_reference_date():
    print("✅ Running step: wait_reference_date")

def verify_uploaded_parameters_in_open_mode():
    print("✅ Running step: verify_uploaded_parameters_in_open_mode")

def check_current_nominal_longitude():
    print("✅ Running step: check_current_nominal_longitude")

def check_aj_nominal_longitude():
    print("✅ Running step: check_aj_nominal_longitude")

def flush_sgm_eeprom():
    print("✅ Running step: flush_sgm_eeprom")

def update_current_nominal_longitude():
    print("✅ Running step: update_current_nominal_longitude")

def update_aj_nominal_longitude():
    print("✅ Running step: update_aj_nominal_longitude")

def write_in_sgm_eeprom():
    print("✅ Running step: write_in_sgm_eeprom")

def update_oop_fdir_parameters():
    print("✅ Running step: update_oop_fdir_parameters")

def configure_oop_with_new_parameters():
    print("✅ Running step: configure_oop_with_new_parameters")

def configure_oop_with_current_parameters():
    print("✅ Running step: configure_oop_with_current_parameters")

def enable_update_by_gnss():
    print("✅ Running step: enable_update_by_gnss")

def activate_oop_fdir():
    print("✅ Running step: activate_oop_fdir")

def restore_observability():
    print("✅ Running step: restore_observability")

def end_of_procedure():
    print("✅ Procedure finished.")
