# File: PS6_HOP_DHS_001.py
import time
from yamcs import log

# ------------------------------------------------------------------------
# Stub fungsi helper (opsional, bisa dikustomisasi)
# ------------------------------------------------------------------------
def procedure_initialize(apType, procName, ARGS):
    return {}

def mainStepFlowControl(stepId, stepName, g):
    log(f"[{stepId}] {stepName} (main step)")

def stepFlowControl(stepId, stepName, g):
    log(f"[{stepId}] {stepName}")

def cleanup(procName):
    log(f"Cleanup procedure {procName}")

# ------------------------------------------------------------------------
# Main Procedure
# ------------------------------------------------------------------------
def run(apType="SHIP", ARGS=None):
    g = procedure_initialize(apType, "PS6_HOP_DHS_001", ARGS)

    log("=== START: PS6_HOP_DHS_001 ===")

    # ==================================================================
    mainStepFlowControl("START", "Begin PS6_HOP_DHS_001", g)

    # Step 1.1
    stepFlowControl("1.1", "Which processor is Primary?", g)
    varDH50200 = get_value("T DH50200 Primary Processor ID")
    log(f"Telemetry T DH50200 Primary Processor ID = {varDH50200}")

    if varDH50200 == "GSP1":
        goto = "1.2"
    else:
        goto = "1.5"

    # Processor 1 branch
    if goto == "1.2":
        stepFlowControl("1.2", "Monitor the Processor 1 health statuses for 5 minutes", g)
        log("Monitoring Processor 1 health...")
        time.sleep(5)  # ganti jadi 300 detik untuk real wait
        stepFlowControl("1.3", "Wait 5 minutes", g)
        log("Waited 5 minutes (simulated 5s).")
        stepFlowControl("1.4", "Are health checks OK?", g)
        health_ok = True  # dummy
        log(f"Processor 1 health OK? {health_ok}")
        if not health_ok:
            goto = "1.8"
        else:
            goto = "2"

    # Processor 2 branch
    elif goto == "1.5":
        stepFlowControl("1.5", "Monitor the Processor 2 health statuses for 5 minutes", g)
        log("Monitoring Processor 2 health...")
        time.sleep(5)
        stepFlowControl("1.6", "Wait 5 minutes", g)
        log("Waited 5 minutes (simulated 5s).")
        stepFlowControl("1.7", "Are health checks OK?", g)
        health_ok = True  # dummy
        log(f"Processor 2 health OK? {health_ok}")
        if not health_ok:
            goto = "1.8"
        else:
            goto = "3"

    # Step 1.8
    if goto == "1.8":
        stepFlowControl("1.8", "Convene Contingency Meeting", g)
        log("Contingency meeting required.")
        goto = "999"

    # Step 2: Processor 1 Checkout
    if goto == "2":
        mainStepFlowControl("2", "Processor 1 Checkout", g)
        stepFlowControl("2.1", "Decoder Redundancy Checkout", g)
        log("Would run PS6_HOP_DHS_002b here.")
        stepFlowControl("2.2", "Determine EEPROM Readout executed?", g)
        eeprom_executed = True  # dummy
        log(f"EEPROM readout executed in last year? {eeprom_executed}")
        if not eeprom_executed:
            goto = "2.3"
        else:
            goto = "2.4"

        if goto == "2.3":
            stepFlowControl("2.3", "EEPROM Readout and Comparison to Ground Image", g)
            log("Would run PS6_HOP_DHS_003 here.")
            goto = "2.4"

        if goto == "2.4":
            stepFlowControl("2.4", "Is the EEPROM image nominal?", g)
            eeprom_nominal = True  # dummy
            log(f"EEPROM nominal? {eeprom_nominal}")
            if not eeprom_nominal:
                goto = "2.5"
            else:
                goto = "999"

        if goto == "2.5":
            stepFlowControl("2.5", "Convene Contingency meeting", g)
            log("Contingency meeting required.")
            goto = "999"

    # Step 3: Processor 2 Checkout
    if goto == "3":
        mainStepFlowControl("3", "Processor 2 Checkout", g)
        stepFlowControl("3.1", "Decoder Redundancy Checkout", g)
        log("Would run PS6_HOP_DHS_002b here.")
        stepFlowControl("3.2", "Determine EEPROM Readout executed?", g)
        eeprom_executed = True  # dummy
        log(f"EEPROM readout executed in last year? {eeprom_executed}")
        if not eeprom_executed:
            goto = "3.3"
        else:
            goto = "3.4"

        if goto == "3.3":
            stepFlowControl("3.3", "EEPROM Readout and Comparison to Ground Image", g)
            log("Would run PS6_HOP_DHS_003 here.")
            goto = "3.4"

        if goto == "3.4":
            stepFlowControl("3.4", "Is the EEPROM image nominal?", g)
            eeprom_nominal = True  # dummy
            log(f"EEPROM nominal? {eeprom_nominal}")
            if not eeprom_nominal:
                goto = "3.5"
            else:
                goto = "999"

        if goto == "3.5":
            stepFlowControl("3.5", "Convene Contingency meeting", g)
            log("Contingency meeting required.")
            goto = "999"

    # Step 999: END
    if goto == "999":
        mainStepFlowControl("999", "END", g)
        cleanup("PS6_HOP_DHS_001")
        log("=== END: PS6_HOP_DHS_001 ===")
