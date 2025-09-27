# File: PS6_HOP_DHS_001.py
from yamcs import Procedure, prompt
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
# Main Procedure
# ------------------------------------------------------------------------


def run(proc: Procedure, apType="SHIP", ARGS=None):
    # ==========================================================================
    proc.step("INIT", "Initialization")
    g = procedure_initialize(apType, "PS6_HOP_DHS_001", ARGS)

    # ==========================================================================
    proc.step("START", "Begin PS6_HOP_DHS_001")
    mainStepFlowControl("START", "Begin PS6_HOP_DHS_001", g)

    # ==========================================================================
    proc.step("1.1", "Which processor is Primary?")
    stepFlowControl("1.1", "Which processor is Primary?", g)
    varDH50200 = proc.getTM("T DH50200 Primary Processor ID")

    if varDH50200 == "GSP1":
        proc.goto("1.2")
    else:
        proc.goto("1.5")

    # ==========================================================================
    proc.step("1.2", "Monitor the Processor 1 health statuses for 5 minutes")
    stepFlowControl(
        "1.2", "Monitor the Processor 1 health statuses for 5 minutes", g)
    prompt.ok("Monitor the Processor 1 health statuses for 5 minutes")

    # ==========================================================================
    proc.step("1.3", "Wait 5 minutes")
    stepFlowControl("1.3", "Wait 5 minutes", g)
    proc.wait(300)

    # ==========================================================================
    proc.step("1.4", "Are health checks OK?")
    stepFlowControl("1.4", "Are health checks OK?", g)
    if not prompt.yesno("Are health checks OK?"):
        proc.goto("1.8")
    else:
        proc.goto("2")

    # ==========================================================================
    proc.step("1.5", "Monitor the Processor 2 health statuses for 5 minutes")
    stepFlowControl(
        "1.5", "Monitor the Processor 2 health statuses for 5 minutes", g)
    prompt.ok("Monitor the Processor 2 health statuses for 5 minutes")

    # ==========================================================================
    proc.step("1.6", "Wait 5 minutes")
    stepFlowControl("1.6", "Wait 5 minutes", g)
    proc.wait(300)

    # ==========================================================================
    proc.step("1.7", "Are health checks OK?")
    stepFlowControl("1.7", "Are health checks OK?", g)
    if not prompt.yesno("Are health checks OK?"):
        proc.goto("1.8")
    else:
        proc.goto("3")

    # ==========================================================================
    proc.step("1.8", "Convene Contingency Meeting")
    stepFlowControl("1.8", "Convene Contingency Meeting", g)
    prompt.ok("Convene Contingency Meeting")
    proc.goto("999")

    # ==========================================================================
    proc.step("2", "Processor 1 Checkout")
    mainStepFlowControl("2", "Processor 1 Checkout", g)

    proc.step("2.1", "Go to HOP_DHS_002b, Decoder Redundancy Checkout")
    stepFlowControl(
        "2.1", "Go to HOP_DHS_002b, Decoder Redundancy Checkout", g)
    if prompt.yesno("Do you want this script to now open PS6_HOP_DHS_002b?"):
        proc.start("PS6_HOP_DHS_002b", args=[["globalSettings", g]])

    proc.step(
        "2.2", "Determine if EEPROM Readout has been executed in the last year.")
    stepFlowControl(
        "2.2", "Determine if EEPROM Readout has been executed in the last year.", g)
    if not prompt.yesno("Determine if EEPROM Readout has been executed in the last year."):
        proc.goto("2.3")
    else:
        proc.goto("2.4")

    proc.step(
        "2.3", "Go to HOP_DHS_003, EEPROM Readout and Comparison to Ground Image")
    stepFlowControl(
        "2.3", "Go to HOP_DHS_003, EEPROM Readout and Comparison to Ground Image", g)
    if prompt.yesno("Do you want this script to now open PS6_HOP_DHS_003?"):
        proc.start("PS6_HOP_DHS_003", args=[["globalSettings", g]])

    proc.step("2.4", "Is the EEPROM image nominal?")
    stepFlowControl("2.4", "Is the EEPROM image nominal?", g)
    if not prompt.yesno("Is the EEPROM image nominal?"):
        proc.goto("2.5")
    else:
        proc.goto("999")

    proc.step("2.5", "Convene Contingency meeting")
    stepFlowControl("2.5", "Convene Contingency meeting", g)
    prompt.ok("Convene Contingency meeting")
    proc.goto("999")

    # ==========================================================================
    proc.step("3", "Processor 2 Checkout")
    mainStepFlowControl("3", "Processor 2 Checkout", g)

    proc.step("3.1", "Go to HOP_DHS_002b, Decoder Redundancy Checkout")
    stepFlowControl(
        "3.1", "Go to HOP_DHS_002b, Decoder Redundancy Checkout", g)
    if prompt.yesno("Do you want this script to now open PS6_HOP_DHS_002b?"):
        proc.start("PS6_HOP_DHS_002b", args=[["globalSettings", g]])

    proc.step(
        "3.2", "Determine if EEPROM Readout has been executed in the last year.")
    stepFlowControl(
        "3.2", "Determine if EEPROM Readout has been executed in the last year.", g)
    if not prompt.yesno("Determine if EEPROM Readout has been executed in the last year."):
        proc.goto("3.3")
    else:
        proc.goto("3.4")

    proc.step(
        "3.3", "Go to HOP_DHS_003, EEPROM Readout and Comparison to Ground Image")
    stepFlowControl(
        "3.3", "Go to HOP_DHS_003, EEPROM Readout and Comparison to Ground Image", g)
    if prompt.yesno("Do you want this script to now open PS6_HOP_DHS_003?"):
        proc.start("PS6_HOP_DHS_003", args=[["globalSettings", g]])

    proc.step("3.4", "Is the EEPROM image nominal?")
    stepFlowControl("3.4", "Is the EEPROM image nominal?", g)
    if not prompt.yesno("Is the EEPROM image nominal?"):
        proc.goto("3.5")
    else:
        proc.goto("999")

    proc.step("3.5", "Convene Contingency meeting")
    stepFlowControl("3.5", "Convene Contingency meeting", g)
    prompt.ok("Convene Contingency meeting")

    # ==========================================================================
    proc.step("999", "END")
    mainStepFlowControl("999", "END", g)
    cleanup("PS6_HOP_DHS_001")

    proc.step("END", "End PS6_HOP_DHS_001")
