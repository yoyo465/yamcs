#!/usr/bin/env -S python3 -u
# OOP-like GNSS Update Procedure for Yamcs
#
# Place this file under: etc/scripts/
# In Yamcs Web -> Procedures -> Run a script, select this file and pass arguments, e.g.:
#   --oop-update ENABLE_UPDATE_BY_GNSS --enable-fdir DISABLED --action-mask-inflight YES
#
# The script uses YamcsClient.from_environment(), which receives connection info from Yamcs.
#
# Exit code: 0 on success, 1 on abort/failure (messages printed to stdout).

import argparse
import os
import sys
import time

try:
    from yamcs.client import YamcsClient
except Exception as e:
    print("[FATAL] yamcs Python client not available. Install with: pip install yamcs-client", flush=True)
    sys.exit(1)

def log(level, msg):
    print(f"[{level}] {msg}", flush=True)

def abort(code, msg):
    log("ABORT", f"code={code} msg={msg}")
    sys.exit(1)

def bool_from_yesno(v: str) -> bool:
    return str(v).strip().upper() in ("YES", "ENABLED", "TRUE", "1")

def get_param(processor, path, *, from_cache=False, timeout=5.0):
    try:
        pv = processor.get_parameter_value(path, from_cache=from_cache, timeout=timeout)
        return pv
    except Exception as e:
        abort(-20, f"Failed to read parameter {path}: {e}")

def pv_eng_value(pv):
    # yamcs client ParameterValue has 'eng_value' and 'raw_value'
    try:
        return pv.eng_value
    except Exception:
        return pv.value if hasattr(pv, "value") else pv

def issue_command(processor, path, args=None, await_ack=True, await_complete=False, timeout=10.0):
    try:
        conn = processor.create_command_connection() if (await_ack or await_complete) else None
        if conn:
            cmd = conn.issue(path, args=args or {})
            if await_ack:
                ack = cmd.await_acknowledgment("Acknowledge_Sent", timeout=timeout)
                log("INFO", f"Acknowledgment: {ack.name} -> {ack.status}")
            if await_complete:
                cmd.await_complete(timeout=timeout)
                if cmd.is_success():
                    log("INFO", f"Command completed OK: {path}")
                else:
                    abort(-19, f"Command failed: {path} error={cmd.error}")
            return True
        else:
            processor.issue_command(path, args=args or {})
            return True
    except Exception as e:
        abort(-19, f"Failed to issue command {path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="OOP-like GNSS Update Procedure for Yamcs")

    # User arguments (equiv. to proc.arg.* in the XML example)
    parser.add_argument("--oop-update", choices=["ENABLE_UPDATE_BY_GNSS", "DISABLE_UPDATE_BY_GNSS"],
                        required=True, help="Enable/Disable OOP update by GNSS function")
    parser.add_argument("--enable-fdir", choices=["ENABLED", "DISABLED"], required=True,
                        help="Enable/Disable OOP FDIR")

    # Config-like flags (equiv. to proc.var.SC_CFG_MASK_* in the XML example)
    parser.add_argument("--action-mask-inflight", choices=["YES", "NO"], default="YES",
                        help="SC_CFG_MASK_ActionToPerformInFlight_s_e (YES/NO)")
    parser.add_argument("--gnss-presence", choices=["YES", "NO"], default="YES",
                        help="SC_CFG_MASK_GNSSPresence_s_e (YES/NO)")

    # Optional: command to request one-shot HK (replicates PST_HK_ONE_SHOT_DWL concept)
    parser.add_argument("--cmd-hk", default=None,
                        help="Fully-qualified XTCE path of your ONE SHOT HK command (e.g. /simdhs/PST_HK_ONE_SHOT_DWL). If omitted, step is skipped.")
    parser.add_argument("--hk-count", type=int, default=1,
                        help="ONE SHOT HK: number of packets (default 1)")
    parser.add_argument("--hk-sid", default="AO_GNSS_HK",
                        help="ONE SHOT HK: SID to request (default AO_GNSS_HK)")

    # Parameter paths (defaults based on your 'simdhs' style naming; adjust as needed)
    parser.add_argument("--param-oop-upd-by-gnss-flag", default="/simdhs/PSA_OOP_UPD_BY_GNSS_FLG")
    parser.add_argument("--param-cel", default="/simdhs/PSF_CEL_PKT_NB")
    parser.add_argument("--param-gnss1-sts", default="/simdhs/CFG_GNSS_1_STS")
    parser.add_argument("--param-gnss2-sts", default="/simdhs/CFG_GNSS_2_STS")
    parser.add_argument("--param-oop-sts", default="/simdhs/OOP_STS")

    # Timing knobs
    parser.add_argument("--wait-after-hk-sec", type=float, default=5.0,
                        help="Wait time after requesting HK (seconds)")
    parser.add_argument("--timeout", type=float, default=8.0,
                        help="Generic timeout for reads/verifications (seconds)")

    args = parser.parse_args()

    log("INFO", f"OOPUpdate = {args.oop-update if False else args.oop_update}")
    log("INFO", f"EnableFDIR  = {args.enable_fdir}")
    log("INFO", f"ActionInFlight = {args.action_mask_inflight}, GNSSPresence = {args.gnss_presence}")

    # Connect using Yamcs-provided environment (YAMCS_URL, YAMCS_INSTANCE, YAMCS_PROCESSOR)
    try:
        client = YamcsClient.from_environment()
        processor = client.get_processor(instance=os.environ["YAMCS_INSTANCE"],
                                         processor=os.environ["YAMCS_PROCESSOR"])
    except Exception as e:
        abort(-16, f"Failed to connect to Yamcs via environment: {e}")

    # Step: INITIALISE_PROCEDURE
    oop_update_by_gnss_enabled = (args.oop_update == "ENABLE_UPDATE_BY_GNSS")
    # mirror the XML's OopUpdatedByGnssSts_s_g = true/false
    OopUpdatedByGnssSts_s_g = oop_update_by_gnss_enabled
    log("INFO", f"OopUpdatedByGnssSts = {OopUpdatedByGnssSts_s_g}")

    # Step: SET_VARIABLES (guarded by ActionToPerformInFlight == YES)
    if bool_from_yesno(args.action_mask_inflight):
        if args.cmd_hk:
            # Try to issue ONE SHOT HK for GNSS_HK
            log("INFO", f"Issuing ONE-SHOT HK command: {args.cmd_hk} (count={args.hk_count}, sid={args.hk_sid})")
            # Arguments depend on your MDB; adjust names as needed
            hk_args = {
                "CNT_TC_GRP71": int(args.hk_count),
                "APIDS_SIDS_GRP_SID2": str(args.hk_sid)
            }
            issue_command(processor, args.cmd_hk, args=hk_args, await_ack=True, await_complete=False, timeout=args.timeout)
            time.sleep(float(args.wait_after_hk_sec))
        else:
            log("WARN", "Skipping ONE-SHOT HK request (no --cmd-hk provided)")

        # Cache the initial 'update-by-GNSS' TM flag (if available)
        pv = get_param(processor, args.param_oop_upd_by_gnss_flag, from_cache=False, timeout=args.timeout)
        OOPByGNSSInitialSts = str(pv_eng_value(pv))
        log("INFO", f"OOPByGNSSInitialSts = {OOPByGNSSInitialSts}")
    else:
        log("INFO", "SET_VARIABLES skipped: ActionToPerformInFlight == NO")

    # Step: CHECK_CEL (only meaningful if CEL != 0 and action mask YES)
    if bool_from_yesno(args.action_mask_inflight):
        pv = get_param(processor, args.param_cel, from_cache=False, timeout=args.timeout)
        cel_val = pv_eng_value(pv)
        try:
            cel_num = int(cel_val)
        except Exception:
            cel_num = None

        if cel_num is not None and cel_num != 0:
            log("WARN", "CEL counter is not equal to 0.")
            abort(-1000, "CEL != 0")

    # Step: CHECK_GNSS_CONFIGURATION
    if oop_update_by_gnss_enabled and not bool_from_yesno(args.gnss_presence):
        log("WARN", "No GNSS embedded on spacecraft. OOP cannot be updated by GNSS.")
        abort(-1000, "GNSS presence == NO")

    # Step: CHECK_GNSS_STATUS
    if oop_update_by_gnss_enabled:
        gnss1 = str(pv_eng_value(get_param(processor, args.param_gnss1_sts, from_cache=False, timeout=args.timeout)))
        gnss2 = str(pv_eng_value(get_param(processor, args.param_gnss2_sts, from_cache=False, timeout=args.timeout)))
        if gnss1 != "OPERATIONAL" and gnss2 != "OPERATIONAL":
            log("WARN", "No GNSS is OPERATIONAL in SATCONF. Cannot use GNSS to update OOP.")
            abort(-1000, "GNSS both NOT OPERATIONAL")

    # Step: CHECK_OOP_STATUS
    pv = get_param(processor, args.param_oop_sts, from_cache=False, timeout=args.timeout)
    oop_sts = str(pv_eng_value(pv))
    log("INFO", f"OOP_STS = {oop_sts}")
    FirstOOPUpdate = (oop_sts == "DISABLED")
    log("INFO", f"FirstOOPUpdate = {FirstOOPUpdate}")

    if FirstOOPUpdate:
        # In the XML they flag OOPNewParamCheck_s_g = 'OK' just as a marker
        OOPNewParamCheck_s_g = "OK"
        log("INFO", f"OOPNewParamCheck = {OOPNewParamCheck_s_g}")

    # Prevent illegal combinations (same as XML warnings)
    if oop_update_by_gnss_enabled and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling update-by-GNSS")

    if (not oop_update_by_gnss_enabled) and (args.enable_fdir == "ENABLED") and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling OOP FDIR")

    # If we got here, consider the procedure successful
    log("SUCCESS", "Procedure finished without abort conditions.")
    sys.exit(0)

if __name__ == "__main__":
    main()
