# Auto-generated Python procedure for SBNEO_RA03_OOP_UPDATE_MANAGEMENT

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
    # No description
    print('Running step: INITIALISE_PROCEDURE')
    pass

def set_variables():
    # No description
    print('Running step: SET_VARIABLES')
    pass

def check_cel():
    # No description
    print('Running step: CHECK_CEL')
    pass

def check_gnss_configuration():
    # No description
    print('Running step: CHECK_GNSS_CONFIGURATION')
    pass

def check_gnss_status():
    # No description
    print('Running step: CHECK_GNSS_STATUS')
    pass

def check_oop_status():
    # No description
    print('Running step: CHECK_OOP_STATUS')
    pass

def check_obcp_is_not_running():
    # Variable used to check if ESK OBCP is loaded in OPISS
    print('Running step: CHECK_OBCP_IS_NOT_RUNNING')
    pass

def check_reference_date_consistency():
    # Variable used to store current date.
    print('Running step: CHECK_REFERENCE_DATE_CONSISTENCY')
    pass

def configure_observability():
    # Variables used to compute required bandwidth for HK packets enabling
    print('Running step: CONFIGURE_OBSERVABILITY')
    pass

def check_gnss_and_oop_fdir_configuration():
    # No description
    print('Running step: CHECK_GNSS_AND_OOP_FDIR_CONFIGURATION')
    pass

def check_obt_ut():
    # Initiate Procedure RG01_OBT_MANAGEMENT
    print('Running step: CHECK_OBT_UT')
    pass

def disable_oop_update_by_gnss():
    # No description
    print('Running step: DISABLE_OOP_UPDATE_BY_GNSS')
    pass

def verify_gnss_validity_flag():
    # No description
    print('Running step: VERIFY_GNSS_VALIDITY_FLAG')
    pass

def configure_gnss_fdir():
    # No description
    print('Running step: CONFIGURE_GNSS_FDIR')
    pass

def deactivate_oop_fdir():
    # No description
    print('Running step: DEACTIVATE_OOP_FDIR')
    pass

def authorize_oop_parameters_loading():
    # SEND TC for authorizing the parameters loading
    print('Running step: AUTHORIZE_OOP_PARAMETERS_LOADING')
    pass

def load_oop_parameters():
    # SEND TC for initialisation OOP with external variables INIT_OOP
    print('Running step: LOAD_OOP_PARAMETERS')
    pass

def wait_reference_date():
    # Variable used to store current date
    print('Running step: WAIT_REFERENCE_DATE')
    pass

def verify_uploaded_parameters_in_open_mode():
    # No description
    print('Running step: VERIFY_UPLOADED_PARAMETERS_IN_OPEN_MODE')
    pass

def check_current_nominal_longitude():
    # No description
    print('Running step: CHECK_CURRENT_NOMINAL_LONGITUDE')
    pass

def check_aj_nominal_longitude():
    # Variable used to convert deg to rad
    print('Running step: CHECK_AJ_NOMINAL_LONGITUDE')
    pass

def flush_sgm_eeprom():
    # No description
    print('Running step: FLUSH_SGM_EEPROM')
    pass

def update_current_nominal_longitude():
    # No description
    print('Running step: UPDATE_CURRENT_NOMINAL_LONGITUDE')
    pass

def update_aj_nominal_longitude():
    # No description
    print('Running step: UPDATE_AJ_NOMINAL_LONGITUDE')
    pass

def write_in_sgm_eeprom():
    # No description
    print('Running step: WRITE_IN_SGM_EEPROM')
    pass

def update_oop_fdir_parameters():
    # Variable used to check YLOF and FDIR OOP thresholds
    print('Running step: UPDATE_OOP_FDIR_PARAMETERS')
    pass

def configure_oop_with_new_parameters():
    # VERIFY TM with external variables in PROC_initoop
    print('Running step: CONFIGURE_OOP_WITH_NEW_PARAMETERS')
    pass

def configure_oop_with_current_parameters():
    # OOP_LOAD_MEAN_ANO is not checked because not updated by OBSW (data not used).
    print('Running step: CONFIGURE_OOP_WITH_CURRENT_PARAMETERS')
    pass

def enable_update_by_gnss():
    # No description
    print('Running step: ENABLE_UPDATE_BY_GNSS')
    pass

def activate_oop_fdir():
    # Variable used to check Longitude before FDIR activation
    print('Running step: ACTIVATE_OOP_FDIR')
    pass

def restore_observability():
    # Disable packets which were disabled at procedure start.
    print('Running step: RESTORE_OBSERVABILITY')
    pass

def end_of_procedure():
    # No description
    print('Running step: END_OF_PROCEDURE')
    pass

