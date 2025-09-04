#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OOP-like GNSS Update Procedure for Yamcs (updated)
--------------------------------------------------
- Meniru alur prosedur XML: INITIALISE → SET_VARIABLES → CHECK_CEL → CHECK_GNSS_CONFIGURATION
  → CHECK_GNSS_STATUS → CHECK_OOP_STATUS.
- Dijalan­kan dari YAMCS Web: Procedures → Run a script.
- Mengandalkan Yamcs Python Client (pip install yamcs-client).

Argumen contoh:
  --oop-update DISABLE_UPDATE_BY_GNSS --enable-fdir DISABLED --action-mask-inflight YES --gnss-presence YES
  --cmd-hk /simdhs/PST_HK_ONE_SHOT_DWL --hk-count 1 --hk-sid AO_GNSS_HK
  --param-oop-upd-by-gnss-flag /simdhs/PSA_OOP_UPD_BY_GPS_FLG
  --param-cel /simdhs/PSF_CEL_PKT_NB
  --param-gnss1-sts /simdhs/CFG_GNSS_1_STS
  --param-gnss2-sts /simdhs/CFG_GNSS_2_STS
  --param-oop-sts /simdhs/OOP_STS

Exit code:
  0 = SUCCESS, 1 = ABORT/FAILED (lihat log Activities).
"""
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
    """Read a single parameter value (engineering)."""
    try:
        pv = processor.get_parameter_value(path, from_cache=from_cache, timeout=timeout)
        return pv
    except Exception as e:
        abort(-20, f"Failed to read parameter {path}: {e}")

def pv_eng_value(pv):
    # yamcs client ParameterValue typically has 'eng_value' (or 'value' attr fallback)
    try:
        return pv.eng_value
    except Exception:
        return getattr(pv, "value", pv)

def issue_command(processor, path, args=None, await_ack=True, await_complete=False, timeout=10.0):
    try:
        if await_ack or await_complete:
            conn = processor.create_command_connection()
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

    # User arguments (equiv to proc.arg.*)
    parser.add_argument("--oop-update", choices=["ENABLE_UPDATE_BY_GNSS", "DISABLE_UPDATE_BY_GNSS"], required=True,
                        help="Enable/Disable OOP update by GNSS")
    parser.add_argument("--enable-fdir", choices=["ENABLED", "DISABLED"], required=True,
                        help="Enable/Disable OOP FDIR")

    # Config-like flags (equiv to proc.var.SC_CFG_MASK_*)
    parser.add_argument("--action-mask-inflight", choices=["YES", "NO"], default="YES",
                        help="SC_CFG_MASK_ActionToPerformInFlight_s_e (YES/NO)")
    parser.add_argument("--gnss-presence", choices=["YES", "NO"], default="YES",
                        help="SC_CFG_MASK_GNSSPresence_s_e (YES/NO)")

    # Optional one-shot HK command (replicate PST_HK_ONE_SHOT_DWL idea)
    parser.add_argument("--cmd-hk", default=None, help="XTCE path of ONE SHOT HK command (e.g. /simdhs/PST_HK_ONE_SHOT_DWL)")
    parser.add_argument("--hk-count", type=int, default=1, help="ONE SHOT HK: number of packets")
    parser.add_argument("--hk-sid", default="AO_GNSS_HK", help="ONE SHOT HK: SID")

    # Parameter paths (defaults aligned to your 'GPS' naming in XML)
    parser.add_argument("--param-oop-upd-by-gnss-flag", default="/simdhs/PSA_OOP_UPD_BY_GPS_FLG")
    parser.add_argument("--param-cel", default="/simdhs/PSF_CEL_PKT_NB")
    parser.add_argument("--param-gnss1-sts", default="/simdhs/CFG_GNSS_1_STS")
    parser.add_argument("--param-gnss2-sts", default="/simdhs/CFG_GNSS_2_STS")
    parser.add_argument("--param-oop-sts", default="/simdhs/OOP_STS")

    # Timing knobs
    parser.add_argument("--wait-after-hk-sec", type=float, default=5.0, help="Wait after ONE SHOT HK (seconds)")
    parser.add_argument("--timeout", type=float, default=8.0, help="Generic timeout (seconds)")

    # Debug verbosity
    parser.add_argument("--debug", action="store_true", help="Print interpreter/env info at start")

    args = parser.parse_args()

    if args.debug:
        log("INFO", f"Python = {sys.executable}")
        log("INFO", f"PATH = {os.environ.get('PATH','')}")

    log("INFO", f"OOPUpdate = {args.oop_update}")
    log("INFO", f"EnableFDIR  = {args.enable_fdir}")
    log("INFO", f"ActionInFlight = {args.action_mask_inflight}, GNSSPresence = {args.gnss_presence}")

    # Connect using YAMCS_* env (provided by Web Procedures runner)
    try:
        client = YamcsClient.from_environment()
        instance = os.environ["YAMCS_INSTANCE"]
        processor_name = os.environ["YAMCS_PROCESSOR"]
        processor = client.get_processor(instance=instance, processor=processor_name)
    except Exception as e:
        abort(-16, f"Failed to connect to Yamcs via environment: {e}")

    # Step: INITIALISE_PROCEDURE
    oop_update_by_gnss_enabled = (args.oop_update == "ENABLE_UPDATE_BY_GNSS")
    OopUpdatedByGnssSts_s_g = oop_update_by_gnss_enabled
    log("INFO", f"OopUpdatedByGnssSts = {OopUpdatedByGnssSts_s_g}")

    # Step: SET_VARIABLES (only if inflight YES)
    if bool_from_yesno(args.action_mask_inflight):
        if args.cmd_hk:
            log("INFO", f"Issuing ONE-SHOT HK: {args.cmd_hk} (count={args.hk_count}, sid={args.hk_sid})")
            # Adjust argument names to your MDB if needed:
            hk_args = {
                "CNT_TC_GRP71": int(args.hk_count),
                "APIDS_SIDS_GRP_SID2": str(args.hk_sid),
            }
            issue_command(processor, args.cmd_hk, args=hk_args, await_ack=True, await_complete=False, timeout=args.timeout)
            time.sleep(float(args.wait_after_hk_sec))
        else:
            log("WARN", "Skipping ONE-SHOT HK (no --cmd-hk provided)")

        pv = get_param(processor, args.param_oop_upd_by_gnss_flag, from_cache=False, timeout=args.timeout)
        OOPByGNSSInitialSts = str(pv_eng_value(pv))
        log("INFO", f"OOPByGNSSInitialSts = {OOPByGNSSInitialSts}")
    else:
        log("INFO", "SET_VARIABLES skipped: ActionToPerformInFlight == NO")

    # Step: CHECK_CEL
    if bool_from_yesno(args.action_mask_inflight):
        pv = get_param(processor, args.param_cel, from_cache=False, timeout=args.timeout)
        try:
            cel_num = int(pv_eng_value(pv))
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
        OOPNewParamCheck_s_g = "OK"
        log("INFO", f"OOPNewParamCheck = {OOPNewParamCheck_s_g}")

    # Illegal combos (same as XML)
    if oop_update_by_gnss_enabled and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling update-by-GNSS")
    if (not oop_update_by_gnss_enabled) and (args.enable_fdir == "ENABLED") and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling OOP FDIR")

    log("SUCCESS", "Procedure finished without abort conditions.")
    sys.exit(0)

if __name__ == "__main__":
    main()
