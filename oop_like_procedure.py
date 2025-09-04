#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OOP-like Procedure (NO CLIENT)
------------------------------
- Tidak memakai paket `yamcs-client`, hanya REST API via urllib (stdlib).
- Meniru alur: INITIALISE → SET_VARIABLES → CHECK_CEL → CHECK_GNSS_CONFIGURATION
  → CHECK_GNSS_STATUS → CHECK_OOP_STATUS.

Exit code:
  0 = SUCCESS, 1 = ABORT/FAILED (lihat log Activities).
"""
import argparse, json, os, sys, time
from urllib.request import Request, urlopen
from urllib.parse import quote

def log(level, msg): print(f"[{level}] {msg}", flush=True)
def abort(code, msg):
    log("ABORT", f"code={code} msg={msg}")
    sys.exit(1)

def bool_from_yesno(v: str) -> bool:
    return str(v).strip().upper() in ("YES", "ENABLED", "TRUE", "1")

# ==== REST helpers (tanpa paket eksternal) ====
def rest(base, path, method="GET", data=None, token=None, timeout=8.0):
    url = f"{base}{path}"
    req = Request(url, method=method)
    req.add_header("Accept", "application/json")
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
        req.data = body
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urlopen(req, timeout=timeout) as resp:
        ctype = resp.headers.get("Content-Type","")
        if "application/json" in ctype:
            return json.loads(resp.read().decode("utf-8"))
        return resp.read().decode("utf-8")

def eng_value_from_param_json(obj):
    # Ambil nilai engineering dari JSON ParameterValue YAMCS
    v = obj.get("engValue") or obj.get("value") or {}
    if isinstance(v, dict):
        for k, val in v.items():
            if k.endswith("Value") and k != "type":
                return val
        # fallback kalau struktur tidak standar
        return v.get("stringValue") or v.get("floatValue") or v.get("doubleValue") or v.get("uint32Value") or v.get("sint32Value") or v
    return v

def get_param(base, instance, processor, name, token=None, timeout=8.0):
    safe = quote(name, safe="")  # encode slash/space dsb
    try:
        j = rest(base, f"/api/processors/{instance}/{processor}/parameters/{safe}", "GET", None, token, timeout)
        return eng_value_from_param_json(j)
    except Exception as e:
        abort(-20, f"Failed to read parameter {name}: {e}")

def issue_command(base, instance, processor, qname, args=None, token=None, wait_ack=True, timeout=8.0):
    # Sederhana: POST command, lalu (opsional) polling status singkat sampai ACK 'Acknowledge_Sent' muncul.
    qsafe = quote(qname, safe="")
    try:
        j = rest(base, f"/api/processors/{instance}/{processor}/commands/{qsafe}",
                 "POST", {"args": args or {}}, token, timeout)
        cmd_id = j.get("id") or j.get("commandId") or j  # fleksibel
        log("INFO", f"Issued command: {qname}")
        if not wait_ack:
            return True
        # Poll daftar command terbaru & cari status (poll ringan 5x)
        for _ in range(5):
            time.sleep(0.8)
            try:
                lst = rest(base, f"/api/instances/{instance}/processors/{processor}/commands", "GET", None, token, timeout)
                # cari entry terakhir dengan qname cocok
                if isinstance(lst, dict) and "commands" in lst:
                    for c in lst["commands"][-10:]:
                        if c.get("qualifiedName") == qname:
                            acks = c.get("acknowledgments", [])
                            for a in acks:
                                if a.get("name") == "Acknowledge_Sent":
                                    log("INFO", f"Acknowledgment: {a.get('name')} -> {a.get('status')}")
                                    return True
            except Exception:
                pass
        log("WARN", "ACK not observed (continuing).")
        return True
    except Exception as e:
        abort(-19, f"Failed to issue command {qname}: {e}")

def main():
    p = argparse.ArgumentParser(description="OOP-like GNSS Update Procedure (no yamcs-client)")
    # ===== args seperti versi sebelumnya =====
    p.add_argument("--oop-update", choices=["ENABLE_UPDATE_BY_GNSS", "DISABLE_UPDATE_BY_GNSS"], required=True)
    p.add_argument("--enable-fdir", choices=["ENABLED", "DISABLED"], required=True)
    p.add_argument("--action-mask-inflight", choices=["YES","NO"], default="YES")
    p.add_argument("--gnss-presence", choices=["YES","NO"], default="YES")

    p.add_argument("--cmd-hk", default=None)
    p.add_argument("--hk-count", type=int, default=1)
    p.add_argument("--hk-sid", default="AO_GNSS_HK")

    p.add_argument("--param-oop-upd-by-gnss-flag", default="/simdhs/PSA_OOP_UPD_BY_GPS_FLG")
    p.add_argument("--param-cel", default="/simdhs/PSF_CEL_PKT_NB")
    p.add_argument("--param-gnss1-sts", default="/simdhs/CFG_GNSS_1_STS")
    p.add_argument("--param-gnss2-sts", default="/simdhs/CFG_GNSS_2_STS")
    p.add_argument("--param-oop-sts", default="/simdhs/OOP_STS")

    p.add_argument("--wait-after-hk-sec", type=float, default=5.0)
    p.add_argument("--timeout", type=float, default=8.0)

    # ===== koneksi REST (ambil dari env bila ada) =====
    p.add_argument("--url", default=os.environ.get("YAMCS_URL", "http://localhost:8090"))
    p.add_argument("--instance", default=os.environ.get("YAMCS_INSTANCE", "satx"))
    p.add_argument("--processor", default=os.environ.get("YAMCS_PROCESSOR", "realtime"))
    p.add_argument("--auth-token", default=os.environ.get("YAMCS_AUTH_TOKEN", None))
    p.add_argument("--debug", action="store_true")

    a = p.parse_args()

    if a.debug:
        log("INFO", f"Python = {sys.executable}")
        log("INFO", f"BASE = {a.url}, INSTANCE = {a.instance}, PROCESSOR = {a.processor}")

    log("INFO", f"OOPUpdate = {a.oop_update}")
    log("INFO", f"EnableFDIR  = {a.enable_fdir}")
    log("INFO", f"ActionInFlight = {a.action_mask_inflight}, GNSSPresence = {a.gnss_presence}")

    base = a.url.rstrip("/")
    instance = a.instance
    processor = a.processor
    token = a.auth_token

    # INITIALISE_PROCEDURE
    oop_update_by_gnss_enabled = (a.oop_update == "ENABLE_UPDATE_BY_GNSS")
    OopUpdatedByGnssSts = oop_update_by_gnss_enabled
    log("INFO", f"OopUpdatedByGnssSts = {OopUpdatedByGnssSts}")

    # SET_VARIABLES
    if bool_from_yesno(a.action_mask_inflight):
        if a.cmd_hk:
            log("INFO", f"Issuing ONE-SHOT HK: {a.cmd_hk} (count={a.hk_count}, sid={a.hk_sid})")
            hk_args = {"CNT_TC_GRP71": int(a.hk_count), "APIDS_SIDS_GRP_SID2": str(a.hk_sid)}
            issue_command(base, instance, processor, a.cmd_hk, args=hk_args, token=token, wait_ack=True, timeout=a.timeout)
            time.sleep(float(a.wait_after_hk_sec))
        else:
            log("WARN", "Skipping ONE-SHOT HK (no --cmd-hk provided)")

        try:
            OOPByGNSSInitialSts = str(get_param(base, instance, processor, a.param_oop_upd_by_gnss_flag, token, a.timeout))
        except SystemExit:
            raise
        except Exception as e:
            abort(-20, f"Cannot read initial OOPByGNSS flag: {e}")
        log("INFO", f"OOPByGNSSInitialSts = {OOPByGNSSInitialSts}")
    else:
        log("INFO", "SET_VARIABLES skipped: ActionToPerformInFlight == NO")

    # CHECK_CEL
    if bool_from_yesno(a.action_mask_inflight):
        cel = get_param(base, instance, processor, a.param_cel, token, a.timeout)
        try:
            cel_num = int(cel)
        except Exception:
            cel_num = None
        if cel_num is not None and cel_num != 0:
            log("WARN", "CEL counter is not equal to 0.")
            abort(-1000, "CEL != 0")

    # CHECK_GNSS_CONFIGURATION
    if oop_update_by_gnss_enabled and not bool_from_yesno(a.gnss_presence):
        log("WARN", "No GNSS embedded on spacecraft. OOP cannot be updated by GNSS.")
        abort(-1000, "GNSS presence == NO")

    # CHECK_GNSS_STATUS
    if oop_update_by_gnss_enabled:
        gnss1 = str(get_param(base, instance, processor, a.param_gnss1_sts, token, a.timeout))
        gnss2 = str(get_param(base, instance, processor, a.param_gnss2_sts, token, a.timeout))
        if gnss1 != "OPERATIONAL" and gnss2 != "OPERATIONAL":
            log("WARN", "No GNSS is OPERATIONAL in SATCONF. Cannot use GNSS to update OOP.")
            abort(-1000, "GNSS both NOT OPERATIONAL")

    # CHECK_OOP_STATUS
    oop_sts = str(get_param(base, instance, processor, a.param_oop_sts, token, a.timeout))
    log("INFO", f"OOP_STS = {oop_sts}")
    FirstOOPUpdate = (oop_sts == "DISABLED")
    log("INFO", f"FirstOOPUpdate = {FirstOOPUpdate}")

    if FirstOOPUpdate:
        log("INFO", "OOPNewParamCheck = OK")

    # Illegal combos (sama seperti XML)
    if oop_update_by_gnss_enabled and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling update-by-GNSS")
    if (not oop_update_by_gnss_enabled) and (a.enable_fdir == "ENABLED") and FirstOOPUpdate:
        abort(-1000, "OOP must be run before enabling OOP FDIR")

    log("SUCCESS", "Procedure finished without abort conditions.")
    sys.exit(0)

if __name__ == "__main__":
    main()
