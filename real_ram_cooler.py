# -*- coding: utf-8 -*-
"""
Real_RAM_cooler v1.2  ❄  Eisblau Neon
=====================================
Ein ehrliches RAM-Tool für Windows.

WAS ES ECHT MACHT (🎮):
  Leert die Windows-Standby-Liste über die native API
  (NtSetSystemInformation → MemoryPurgeStandbyList) — derselbe
  Mechanismus wie RAMMap -Et und ISLC. Hilft real gegen
  Gaming-Stutter, wenn sich die Standby-Liste aufgebläht hat.

WAS ES ALS GAG MACHT (✨):
  "Placebo-Modus" — trimmt Working-Sets aller Prozesse
  (EmptyWorkingSet). Macht die Zahlen im Task-Manager hübsch,
  den PC aber nicht schneller. Windows schiebt alles in
  Memory Compression und holt es gleich zurück. Ehrlich
  beschriftet, weil wir das live bewiesen haben. 😉

BRAUCHT: Admin-Rechte (Windows erlaubt das Leeren der
Standby-Liste nur so), Python 64-bit, pystray + pillow.

BUILD:
  pip install pystray pillow
  python -m PyInstaller --onefile --noconsole --uac-admin --name Real_RAM_cooler real_ram_cooler.py

Autor: Dennis + Claude, gemeinsame Nacht-Session. 🧊💙
"""

import sys
import os
import json
import time
import ctypes
import threading
import subprocess

# ── Nur Windows ──────────────────────────────────────────────────────
if sys.platform != "win32":
    print("Real_RAM_cooler läuft nur unter Windows.")
    sys.exit(1)

import tkinter as tk
from tkinter import messagebox
from ctypes import wintypes, byref, sizeof

import pystray
from pystray import MenuItem as TrayItem, Menu as TrayMenu
from PIL import Image, ImageDraw

APP_NAME = "Real_RAM_cooler"
VERSION = "1.2"
TASK_NAME = "Real_RAM_cooler_Autostart"

# ═════════════════════════════════════════════════════════════════════
#  EISBLAU NEON — die Farbwelt (fest verdrahtet, erst fahren dann lackieren)
# ═════════════════════════════════════════════════════════════════════
C_BG       = "#0b111a"   # tiefes Nachtblau — Fensterhintergrund
C_PANEL    = "#101a28"   # Panels / Karten
C_PANEL2   = "#0e1622"   # dunklere Panel-Variante
C_ACCENT   = "#66e0ff"   # Eisblau Neon — DIE Farbe
C_ACCENT_D = "#2b8fb3"   # Eisblau gedimmt (Linien, Rahmen)
C_TEXT     = "#e8f4fa"   # fast weiß, leicht kühl
C_MUTED    = "#7f9db0"   # gedämpfter Text (Fußnoten)
C_GOOD     = "#6ee7b7"   # Erfolg (kühles Mintgrün)
C_WARN     = "#ffb86c"   # Warnung (warmer Kontrast)
C_BAR_USED = "#3b82c4"   # RAM-Balken: in Benutzung
C_BAR_STBY = "#66e0ff"   # RAM-Balken: Standby (das, was wir "kühlen")
C_BAR_FREE = "#152435"   # RAM-Balken: wirklich frei

FONT       = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BOLD  = ("Segoe UI", 10, "bold")
FONT_H1    = ("Segoe UI", 13, "bold")
FONT_MONO  = ("Consolas", 10)

# ═════════════════════════════════════════════════════════════════════
#  KONFIG — config.json neben der .exe (sys.frozen-Muster wie beim Ticker)
# ═════════════════════════════════════════════════════════════════════

def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(app_dir(), "config.json")

DEFAULT_CFG = {
    "auto_clean": False,          # ISLC-Automatik — Opt-in, Default AUS
    "standby_threshold_mb": 1024, # leeren, wenn Standby GRÖSSER als …
    "free_threshold_mb": 1536,    # … UND frei KLEINER als …
    "overlay": False,             # schwebendes Mini-Overlay
    "overlay_alpha": 0.28,        # Deckkraft: 0.28 = 28 % sichtbar,
                                  # man sieht hindurch (in config.json
                                  # jederzeit ohne Neubau änderbar)
    "overlay_x": 60,
    "overlay_y": 60,
    "autostart": False,           # via Task Scheduler (RL HIGHEST)
    "language": "auto",           # "auto" (Windows-Sprache) | "de" | "en"
}

def load_cfg():
    cfg = dict(DEFAULT_CFG)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:
        pass
    return cfg

def save_cfg(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Konfig speichern fehlgeschlagen:", e)

CFG = load_cfg()

# ═════════════════════════════════════════════════════════════════════
#  SPRACHEN — Deutsch + Englisch (handpoliert, inkl. Wortwitz).
#  Start folgt der Windows-Anzeigesprache; in den Einstellungen
#  umschaltbar (config.json: "language": "auto" | "de" | "en").
# ═════════════════════════════════════════════════════════════════════

L = {
    "de": {
        "adminOk": "Admin ✓",
        "adminNo": "kein Admin — nur Anzeige",
        "btnReal": "🎮  Fürs Gaming bereinigen",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": ("Trimmt Working-Sets: macht die Zahlen im Task-Manager "
                       "hübsch, den PC nicht schneller. Windows schiebt alles in "
                       "Memory Compression und holt es zurück. Ehrenwort. 😉"),
        "topList": "Top-12 RAM-Fresser",
        "colProcess": "Prozess",
        "colCount": "Anz.",
        "colTouched": "Berührt",
        "colOwns": "Besitzt",
        "cookbook": ("🍳 „Berührt“ = alles, was der Prozess nutzt — inklusive "
                     "dem geteilten Kochbuch auf dem WG-Tisch (DLLs). "
                     "„Besitzt“ = nur seine eigenen Seiten (die Task-Manager-Zahl)."),
        "ex2Fallback": ("* Dieses Windows liefert kein privates Working Set — "
                        "Anzeige: Private Bytes (Commit)."),
        "selfUse": ("Eigenverbrauch: {mb} MB — ein RAM-Tool sollte selbst "
                    "keins fressen. 😉"),
        "legendFull": ("● In Benutzung {used}   ● Standby {stby}   "
                       "● Wirklich frei {free}   (gesamt {total})"),
        "legendNoPdh": ("● In Benutzung {used}   ● Verfügbar {avail}   "
                        "(Standby-Zähler nicht verfügbar)"),
        "ovFull": "❄ Frei {free} · Standby {stby}",
        "ovNoPdh": "❄ Verfügbar {avail}",
        "realDone": ("🎮 Standby-Liste geleert: {before} → {after} ✓  "
                     "({freed} fürs Spiel freigeräumt)"),
        "realDoneNoMeasure": "🎮 Standby-Liste geleert ✓ (Messung nicht verfügbar)",
        "realFail": "Leeren fehlgeschlagen — fehlen Admin-Rechte?",
        "notifyRealTitle": "Bereit fürs Gaming 🎮",
        "placeboDone": ("✨ Zahlen poliert: {n} Prozesse getrimmt, {delta} "
                        "„befreit“. Gefühlt schneller: 100 %. Messbar schneller: 0 %. "
                        "(Windows räumt’s gleich zurück — grüß mir Memory "
                        "Compression. 😉)"),
        "needAdmin": ("Ohne Admin-Rechte erlaubt Windows das Leeren der "
                      "Standby-Liste nicht. Bitte die App als Administrator "
                      "starten."),
        "autoTitle": "Automatik ❄",
        "autoNotify": "Standby geleert: {before} → {after} ({freed} frei)",
        "autoBanner": "❄ Automatik: Standby {before} → {after} ✓",
        "trayDashboard": "Dashboard öffnen",
        "trayReal": "🎮 Fürs Gaming bereinigen",
        "trayPlacebo": "✨ Placebo-Modus",
        "traySettings": "⚙ Einstellungen",
        "trayQuit": "Beenden",
        "setTitle": "Einstellungen ❄",
        "secAuto": "Automatik (ISLC-Stil)",
        "chkAuto": "Automatisch leeren, wenn beide Schwellwerte reißen",
        "sliderStandby": "leeren wenn Standby größer als",
        "sliderFree": "und wirklich frei kleiner als",
        "secOverlay": "Overlay",
        "chkOverlay": "Schwebendes Mini-Overlay anzeigen (ziehbar)",
        "secAutostart": "Autostart",
        "chkAutostart": ("Mit Windows starten (Aufgabenplanung, ohne "
                         "UAC-Abfrage beim Hochfahren)"),
        "taskErr": "Aufgabenplanung meldet:\n{err}",
        "unknownErr": "unbekannter Fehler",
        "adminHint": ("Hinweis: Die App braucht Admin-Rechte, weil Windows "
                      "das Leeren der Standby-Liste nur so erlaubt."),
        "secLang": "Sprache / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Sprache gespeichert — gilt ab dem nächsten Start der App.",
        "alreadyRunning": "läuft bereits (Blick ins Tray ❄).",
        "niceDwm": "dwm (Desktopfenster)",
    },
    "en": {
        "adminOk": "Admin ✓",
        "adminNo": "no admin — view only",
        "btnReal": "🎮  Clean up for gaming",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": ("Trims working sets: makes the Task Manager numbers "
                       "pretty, not your PC faster. Windows shoves it all into "
                       "Memory Compression and takes it right back. "
                       "Scout's honor. 😉"),
        "topList": "Top 12 RAM hogs",
        "colProcess": "Process",
        "colCount": "Cnt",
        "colTouched": "Touches",
        "colOwns": "Owns",
        "cookbook": ("🍳 “Touches” = everything the process uses — including "
                     "the shared cookbook on the kitchen table (DLLs). "
                     "“Owns” = only its own pages (the Task Manager number)."),
        "ex2Fallback": ("* This Windows build doesn't report private working "
                        "sets — showing Private Bytes (commit) instead."),
        "selfUse": ("Own footprint: {mb} MB — a RAM tool shouldn't hog any "
                    "itself. 😉"),
        "legendFull": ("● In use {used}   ● Standby {stby}   "
                       "● Truly free {free}   (total {total})"),
        "legendNoPdh": ("● In use {used}   ● Available {avail}   "
                        "(standby counters unavailable)"),
        "ovFull": "❄ Free {free} · Standby {stby}",
        "ovNoPdh": "❄ Available {avail}",
        "realDone": ("🎮 Standby list purged: {before} → {after} ✓  "
                     "({freed} cleared for your game)"),
        "realDoneNoMeasure": "🎮 Standby list purged ✓ (measurement unavailable)",
        "realFail": "Purge failed — missing admin rights?",
        "notifyRealTitle": "Ready for gaming 🎮",
        "placeboDone": ("✨ Numbers polished: {n} processes trimmed, {delta} "
                        "“freed”. Feels faster: 100%. Measurably faster: 0%. "
                        "(Windows puts it all back in a second — say hi to "
                        "Memory Compression. 😉)"),
        "needAdmin": ("Without admin rights Windows won't allow purging the "
                      "standby list. Please run the app as administrator."),
        "autoTitle": "Automatic ❄",
        "autoNotify": "Standby purged: {before} → {after} ({freed} free)",
        "autoBanner": "❄ Automatic: standby {before} → {after} ✓",
        "trayDashboard": "Open dashboard",
        "trayReal": "🎮 Clean up for gaming",
        "trayPlacebo": "✨ Placebo mode",
        "traySettings": "⚙ Settings",
        "trayQuit": "Quit",
        "setTitle": "Settings ❄",
        "secAuto": "Automatic (ISLC style)",
        "chkAuto": "Purge automatically when both thresholds are crossed",
        "sliderStandby": "purge when standby exceeds",
        "sliderFree": "and truly free is below",
        "secOverlay": "Overlay",
        "chkOverlay": "Show floating mini overlay (draggable)",
        "secAutostart": "Autostart",
        "chkAutostart": ("Start with Windows (Task Scheduler, no UAC prompt "
                         "at boot)"),
        "taskErr": "Task Scheduler says:\n{err}",
        "unknownErr": "unknown error",
        "adminHint": ("Note: the app needs admin rights because Windows only "
                      "allows purging the standby list that way."),
        "secLang": "Sprache / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Language saved — takes effect the next time the app starts.",
        "alreadyRunning": "is already running (check the tray ❄).",
        "niceDwm": "dwm (desktop windows)",
    },
}

def detect_lang():
    pref = CFG.get("language", "auto")
    if pref in L:
        return pref
    try:  # 0x07 = LANG_GERMAN (primäre Sprach-ID der Windows-Anzeigesprache)
        langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return "de" if (langid & 0x3FF) == 0x07 else "en"
    except Exception:
        return "en"

LANG = detect_lang()

def t(key, **kw):
    table = L.get(LANG) or L["en"]
    s = table.get(key) or L["en"].get(key, key)
    return s.format(**kw) if kw else s

# ═════════════════════════════════════════════════════════════════════
#  WINDOWS-API-SCHICHT (ctypes) — hier passiert das Echte
# ═════════════════════════════════════════════════════════════════════
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
ntdll    = ctypes.WinDLL("ntdll")
psapi    = ctypes.WinDLL("psapi", use_last_error=True)
shell32  = ctypes.WinDLL("shell32")
pdh      = ctypes.WinDLL("pdh")

# ── Saubere Signaturen ───────────────────────────────────────────────
# HANDLEs sind auf 64-bit-Windows Pointer, keine ints. Ohne diese
# Deklarationen stutzt ctypes sie auf 32 bit — DER Klassiker unter
# den ctypes-Stolperfallen. Einmal sauber deklariert, nie wieder Ärger.
HANDLE = wintypes.HANDLE
kernel32.GetCurrentProcess.restype = HANDLE
kernel32.OpenProcess.restype = HANDLE
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL,
                                 wintypes.DWORD]
kernel32.CloseHandle.argtypes = [HANDLE]
kernel32.CreateToolhelp32Snapshot.restype = HANDLE
kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD,
                                              wintypes.DWORD]
kernel32.Process32FirstW.argtypes = [HANDLE, ctypes.c_void_p]
kernel32.Process32NextW.argtypes = [HANDLE, ctypes.c_void_p]
kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.c_void_p]
kernel32.CreateMutexW.restype = HANDLE
kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL,
                                  wintypes.LPCWSTR]
if hasattr(kernel32, "K32GetProcessMemoryInfo"):
    kernel32.K32GetProcessMemoryInfo.argtypes = [HANDLE, ctypes.c_void_p,
                                                 wintypes.DWORD]
psapi.GetProcessMemoryInfo.argtypes = [HANDLE, ctypes.c_void_p,
                                       wintypes.DWORD]
psapi.EmptyWorkingSet.argtypes = [HANDLE]
advapi32.OpenProcessToken.argtypes = [HANDLE, wintypes.DWORD,
                                      ctypes.POINTER(HANDLE)]
advapi32.LookupPrivilegeValueW.argtypes = [wintypes.LPCWSTR,
                                           wintypes.LPCWSTR,
                                           ctypes.c_void_p]
advapi32.AdjustTokenPrivileges.argtypes = [HANDLE, wintypes.BOOL,
                                           ctypes.c_void_p, wintypes.DWORD,
                                           ctypes.c_void_p, ctypes.c_void_p]
ntdll.NtSetSystemInformation.argtypes = [ctypes.c_int, ctypes.c_void_p,
                                         ctypes.c_ulong]
pdh.PdhOpenQueryW.argtypes = [wintypes.LPCWSTR, ctypes.c_size_t,
                              ctypes.POINTER(HANDLE)]
pdh.PdhAddEnglishCounterW.argtypes = [HANDLE, wintypes.LPCWSTR,
                                      ctypes.c_size_t,
                                      ctypes.POINTER(HANDLE)]
pdh.PdhCollectQueryData.argtypes = [HANDLE]
pdh.PdhGetFormattedCounterValue.argtypes = [HANDLE, wintypes.DWORD,
                                            ctypes.POINTER(wintypes.DWORD),
                                            ctypes.c_void_p]

# ── Admin-Check & Selbst-Erhöhung ────────────────────────────────────

def is_admin() -> bool:
    try:
        return bool(shell32.IsUserAnAdmin())
    except Exception:
        return False

def relaunch_as_admin():
    """Startet uns selbst einmal mit Admin-Rechten neu (UAC-Abfrage).
    Die gebaute .exe braucht das dank --uac-admin gar nicht — das hier
    ist das Netz für den Skript-Modus (python real_ram_cooler.py)."""
    params = "" if getattr(sys, "frozen", False) else f'"{os.path.abspath(__file__)}"'
    exe = sys.executable
    shell32.ShellExecuteW.restype = ctypes.c_void_p
    ret = shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
    return int(ret or 0) > 32  # >32 = Erfolg laut MSDN

# ── Privilegien freischalten ─────────────────────────────────────────
# Windows verlangt für die Standby-Bereinigung das Privileg
# "SeProfileSingleProcessPrivilege" (RAMMap nutzt exakt dasselbe).
# SeDebug hilft zusätzlich, mehr Prozesse für die Anzeige zu öffnen.

TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY             = 0x0008
SE_PRIVILEGE_ENABLED    = 0x0002

class LUID(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [("PrivilegeCount", wintypes.DWORD),
                ("Privileges", LUID_AND_ATTRIBUTES * 1)]

def enable_privilege(name: str) -> bool:
    token = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(),
                                     TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                                     byref(token)):
        return False
    try:
        luid = LUID()
        if not advapi32.LookupPrivilegeValueW(None, name, byref(luid)):
            return False
        tp = TOKEN_PRIVILEGES()
        tp.PrivilegeCount = 1
        tp.Privileges[0].Luid = luid
        tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
        advapi32.AdjustTokenPrivileges(token, False, byref(tp), 0, None, None)
        return ctypes.get_last_error() == 0
    finally:
        kernel32.CloseHandle(token)

# ── DAS HERZ: Standby-Liste leeren (der echte ISLC-Mechanismus) ──────

SystemMemoryListInformation = 0x50   # Info-Klasse 80
MemoryPurgeStandbyList      = 4      # Kommando: Standby-Liste leeren

def purge_standby_list() -> bool:
    """Leert die Standby-Liste. Gibt True bei Erfolg zurück.
    NTSTATUS 0 == STATUS_SUCCESS."""
    enable_privilege("SeProfileSingleProcessPrivilege")
    cmd = ctypes.c_int(MemoryPurgeStandbyList)
    status = ntdll.NtSetSystemInformation(SystemMemoryListInformation,
                                          byref(cmd), sizeof(cmd))
    return status == 0

# ── DER GAG: Working-Sets trimmen (Placebo, ehrlich beschriftet) ─────

PROCESS_QUERY_INFORMATION         = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_QUOTA                 = 0x0100

def trim_working_sets() -> int:
    """EmptyWorkingSet auf alle erreichbaren Prozesse.
    Rückgabe: Anzahl getrimmter Prozesse. (Windows holt sich das
    meiste sofort zurück — siehe Memory Compression. Wir wissen es. 😉)"""
    count = 0
    for pid in _enum_pids():
        if pid == 0:
            continue
        h = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_SET_QUOTA,
                                 False, pid)
        if not h:
            continue
        try:
            if psapi.EmptyWorkingSet(h):
                count += 1
        finally:
            kernel32.CloseHandle(h)
    return count

# ── RAM-Gesamtstatus (GlobalMemoryStatusEx) ──────────────────────────

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [("dwLength", wintypes.DWORD),
                ("dwMemoryLoad", wintypes.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

def get_memory_status():
    ms = MEMORYSTATUSEX()
    ms.dwLength = sizeof(MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx(byref(ms))
    return ms.ullTotalPhys, ms.ullAvailPhys

# ── Standby-Größe via PDH-Leistungsindikatoren ───────────────────────
# "Verfügbar" bei Windows = wirklich frei + Standby-Cache. Um den
# Standby-Anteil einzeln zu sehen, fragen wir die drei offiziellen
# Zähler ab — genau wie der Ressourcenmonitor.

PDH_FMT_LARGE = 0x00000400

class PDH_FMT_COUNTERVALUE(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("longValue", wintypes.LONG),
                    ("doubleValue", ctypes.c_double),
                    ("largeValue", ctypes.c_longlong),
                    ("AnsiStringValue", ctypes.c_char_p),
                    ("WideStringValue", ctypes.c_wchar_p)]
    _anonymous_ = ("u",)
    _fields_ = [("CStatus", wintypes.DWORD), ("u", _U)]

_pdh_query = None
_pdh_counters = []
_pdh_ok = True

_STANDBY_COUNTERS = [
    r"\Memory\Standby Cache Core Bytes",
    r"\Memory\Standby Cache Normal Priority Bytes",
    r"\Memory\Standby Cache Reserve Bytes",
]

def _pdh_init():
    global _pdh_query, _pdh_ok
    try:
        q = wintypes.HANDLE()
        if pdh.PdhOpenQueryW(None, 0, byref(q)) != 0:
            _pdh_ok = False
            return
        _pdh_query = q
        for path in _STANDBY_COUNTERS:
            h = wintypes.HANDLE()
            if pdh.PdhAddEnglishCounterW(q, path, 0, byref(h)) == 0:
                _pdh_counters.append(h)
        if not _pdh_counters:
            _pdh_ok = False
    except Exception:
        _pdh_ok = False

def get_standby_bytes():
    """Summe der drei Standby-Cache-Zähler, oder None wenn PDH streikt."""
    global _pdh_ok
    if not _pdh_ok:
        return None
    if _pdh_query is None:
        _pdh_init()
        if not _pdh_ok:
            return None
    try:
        if pdh.PdhCollectQueryData(_pdh_query) != 0:
            return None
        total = 0
        for h in _pdh_counters:
            val = PDH_FMT_COUNTERVALUE()
            if pdh.PdhGetFormattedCounterValue(h, PDH_FMT_LARGE, None,
                                               byref(val)) == 0:
                total += max(0, val.largeValue)
        return total
    except Exception:
        _pdh_ok = False
        return None

# ── Prozessliste: Namen via Toolhelp, Speicher via GetProcessMemoryInfo ──
# Zwei Spalten, wie besprochen:
#   "Berührt"  = WorkingSetSize        (inkl. geteilter DLLs — das Kochbuch)
#   "Besitzt"  = PrivateWorkingSetSize (nur die eigenen Seiten — Task-Manager-Zahl)

TH32CS_SNAPPROCESS = 0x00000002
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_void_p),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_wchar * 260)]

class PROCESS_MEMORY_COUNTERS_EX2(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
                ("PrivateUsage", ctypes.c_size_t),
                ("PrivateWorkingSetSize", ctypes.c_size_t),
                ("SharedCommitUsage", ctypes.c_ulonglong)]

# Manche älteren Windows-Builds kennen die EX2-Struktur (mit privatem
# Working Set) noch nicht — dann fallen wir auf PrivateUsage zurück
# und markieren die Spalte ehrlich mit einem Sternchen.
EX2_SUPPORTED = None

def _get_proc_mem(handle):
    """(working_set, privat, ist_ex2) für ein Prozess-Handle."""
    global EX2_SUPPORTED
    pmc = PROCESS_MEMORY_COUNTERS_EX2()
    pmc.cb = sizeof(pmc)
    getinfo = getattr(kernel32, "K32GetProcessMemoryInfo", None) or \
              psapi.GetProcessMemoryInfo
    if getinfo(handle, byref(pmc), pmc.cb):
        ex2 = pmc.PrivateWorkingSetSize > 0
        if EX2_SUPPORTED is None:
            EX2_SUPPORTED = ex2
        priv = pmc.PrivateWorkingSetSize if ex2 else pmc.PrivateUsage
        return pmc.WorkingSetSize, priv, ex2
    return None

def _enum_pids():
    pids = []
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == INVALID_HANDLE_VALUE:
        return pids
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = sizeof(PROCESSENTRY32W)
        if kernel32.Process32FirstW(snap, byref(entry)):
            while True:
                pids.append(entry.th32ProcessID)
                if not kernel32.Process32NextW(snap, byref(entry)):
                    break
    finally:
        kernel32.CloseHandle(snap)
    return pids

_NICE_NAMES = {
    "memcompression": "Memory Compression",
    "msmpeng": "MsMpEng (Defender)",
    "dwm": t("niceDwm"),
}

def list_top_processes(n=12):
    """Top-N-Fresser, gruppiert nach Name.
    Rückgabe: Liste (anzeige_name, anzahl, ws_bytes, priv_bytes)."""
    agg = {}
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == INVALID_HANDLE_VALUE:
        return []
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = sizeof(PROCESSENTRY32W)
        ok = kernel32.Process32FirstW(snap, byref(entry))
        while ok:
            pid = entry.th32ProcessID
            name = entry.szExeFile or f"PID {pid}"
            if pid != 0:
                h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,
                                         False, pid)
                if h:
                    try:
                        mem = _get_proc_mem(h)
                    finally:
                        kernel32.CloseHandle(h)
                    if mem:
                        ws, priv, _ = mem
                        key = name.lower().removesuffix(".exe")
                        if key not in agg:
                            agg[key] = [0, 0, 0]
                        agg[key][0] += 1
                        agg[key][1] += ws
                        agg[key][2] += priv
            ok = kernel32.Process32NextW(snap, byref(entry))
    finally:
        kernel32.CloseHandle(snap)

    rows = []
    for key, (cnt, ws, priv) in agg.items():
        display = _NICE_NAMES.get(key, key)
        rows.append((display, cnt, ws, priv))
    rows.sort(key=lambda r: r[2], reverse=True)
    return rows[:n]

def own_memory_mb():
    """Eigenverbrauch — ein RAM-Tool sollte selbst keins fressen. 😉"""
    mem = _get_proc_mem(kernel32.GetCurrentProcess())
    if mem:
        return mem[0] / (1024 * 1024)
    return 0.0

def trim_self():
    """Trimmt das EIGENE Working Set. Fun Fact: Das ist der einzige
    ehrliche Einsatzort des Placebo-Tricks — beim eigenen Prozess im
    Leerlauf. WIR entscheiden, den Nachlade-Preis zu zahlen, damit wir
    anderen (z.B. deinem Spiel) nicht im Weg rumliegen. Windows macht
    dasselbe mit minimierten Fenstern."""
    try:
        psapi.EmptyWorkingSet(kernel32.GetCurrentProcess())
    except Exception:
        pass

# ── Autostart via Aufgabenplanung (schtasks, RL HIGHEST) ─────────────
# Der Trick seriöser Admin-Tools: eine geplante Aufgabe mit "höchsten
# Privilegien" startet ohne UAC-Abfrage beim Anmelden. Die Abfrage
# kommt genau EINMAL — beim Setzen des Häkchens.

CREATE_NO_WINDOW = 0x08000000

def _task_target():
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    return f'"{sys.executable}" "{os.path.abspath(__file__)}"'

def autostart_enabled() -> bool:
    try:
        r = subprocess.run(["schtasks", "/Query", "/TN", TASK_NAME],
                           capture_output=True, creationflags=CREATE_NO_WINDOW)
        return r.returncode == 0
    except Exception:
        return False

def set_autostart(enabled: bool):
    """True bei Erfolg, sonst (False, fehlertext)."""
    try:
        if enabled:
            r = subprocess.run(
                ["schtasks", "/Create", "/TN", TASK_NAME, "/TR", _task_target(),
                 "/SC", "ONLOGON", "/RL", "HIGHEST", "/F"],
                capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        else:
            r = subprocess.run(
                ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
                capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        if r.returncode == 0:
            return True, ""
        return False, (r.stderr or r.stdout or "").strip()
    except Exception as e:
        return False, str(e)

# ═════════════════════════════════════════════════════════════════════
#  HELFER
# ═════════════════════════════════════════════════════════════════════

def fmt_mb(b):
    """Bytes → 'X.XXX MB' (Tausendertrennung je nach Sprache)."""
    s = f"{b / (1024 * 1024):,.0f}"
    if LANG == "de":
        s = s.replace(",", ".")
    return s + " MB"

def fmt_gb(b):
    s = f"{b / (1024 ** 3):.1f}"
    if LANG == "de":
        s = s.replace(".", ",")
    return s + " GB"

class Tooltip:
    """Winziger Tooltip fürs ehrliche Placebo-Label."""
    def __init__(self, widget, text):
        self.widget, self.text, self.tip = widget, text, None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, bg=C_PANEL, fg=C_TEXT, font=FONT_SMALL,
                 justify="left", wraplength=320, padx=10, pady=6,
                 highlightthickness=1,
                 highlightbackground=C_ACCENT_D).pack()

    def _hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

# ═════════════════════════════════════════════════════════════════════
#  DIE APP
# ═════════════════════════════════════════════════════════════════════

class RealRAMCooler:
    def __init__(self):
        self.admin = is_admin()
        if self.admin:
            enable_privilege("SeProfileSingleProcessPrivilege")
            enable_privilege("SeIncreaseQuotaPrivilege")
            enable_privilege("SeDebugPrivilege")  # mehr Prozesse sichtbar

        self.tray = None
        self.tray_ready = False
        self.actions = []                 # Warteschlange Tray-Thread → Tk
        self.actions_lock = threading.Lock()
        self.last_auto_purge = 0.0
        self.banner_until = 0.0

        # gecachte Messwerte (der 3-Sekunden-Takt füllt sie)
        self.total = self.avail = 0
        self.standby = None

        self._build_root()
        self._build_dashboard()
        self._build_overlay()
        self._build_tray()

        self._tick()  # Herzschlag starten
        # Nach dem Start einmal die eigene Startlast abwerfen
        self.root.after(8000, trim_self)

    # ── Hauptfenster = Dashboard (Schließen → Tray) ──────────────────
    def _build_root(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} ❄ v{VERSION}")
        self.root.configure(bg=C_BG)
        self.root.geometry("560x640")
        self.root.minsize(520, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.hide_dashboard)
        try:  # Fenster-Icon aus dem Tray-Bild
            from PIL import ImageTk
            self._icon_img = ImageTk.PhotoImage(make_icon_image(64))
            self.root.iconphoto(True, self._icon_img)
        except Exception:
            pass

    def _build_dashboard(self):
        pad = {"padx": 16}

        # Kopfzeile
        head = tk.Frame(self.root, bg=C_BG)
        head.pack(fill="x", pady=(14, 6), **pad)
        tk.Label(head, text=f"❄ {APP_NAME}", font=FONT_H1,
                 bg=C_BG, fg=C_ACCENT).pack(side="left")
        self.lbl_admin = tk.Label(
            head,
            text=t("adminOk") if self.admin else t("adminNo"),
            font=FONT_SMALL, bg=C_BG,
            fg=C_GOOD if self.admin else C_WARN)
        self.lbl_admin.pack(side="right")

        # RAM-Balken
        barbox = tk.Frame(self.root, bg=C_PANEL, highlightthickness=1,
                          highlightbackground=C_ACCENT_D)
        barbox.pack(fill="x", pady=(6, 4), **pad)
        self.bar = tk.Canvas(barbox, height=30, bg=C_PANEL,
                             highlightthickness=0)
        self.bar.pack(fill="x", padx=10, pady=(10, 4))
        self.lbl_legend = tk.Label(barbox, text="", font=FONT_SMALL,
                                   bg=C_PANEL, fg=C_MUTED)
        self.lbl_legend.pack(anchor="w", padx=10, pady=(0, 8))

        # Vorher/Nachher-Banner (erscheint nach jeder Bereinigung)
        self.banner = tk.Label(self.root, text="", font=FONT_BOLD, bg=C_BG,
                               fg=C_GOOD, wraplength=520, justify="left")
        self.banner.pack(fill="x", pady=(2, 2), **pad)

        # Buttons
        btns = tk.Frame(self.root, bg=C_BG)
        btns.pack(fill="x", pady=(4, 8), **pad)

        self.btn_real = tk.Button(
            btns, text=t("btnReal"),
            font=FONT_BOLD, bg=C_ACCENT, fg=C_BG,
            activebackground=C_ACCENT_D, activeforeground=C_TEXT,
            relief="flat", cursor="hand2", padx=14, pady=7,
            command=self.do_real_clean)
        self.btn_real.pack(side="left")

        self.btn_placebo = tk.Button(
            btns, text=t("btnPlacebo"),
            font=FONT, bg=C_PANEL, fg=C_ACCENT,
            activebackground=C_PANEL2, activeforeground=C_ACCENT,
            relief="flat", cursor="hand2", padx=12, pady=7,
            highlightthickness=1, highlightbackground=C_ACCENT_D,
            command=self.do_placebo)
        self.btn_placebo.pack(side="left", padx=(10, 0))
        Tooltip(self.btn_placebo, t("tipPlacebo"))

        tk.Button(btns, text="⚙", font=("Segoe UI", 12), bg=C_PANEL,
                  fg=C_TEXT, activebackground=C_PANEL2,
                  activeforeground=C_ACCENT, relief="flat", cursor="hand2",
                  padx=12, pady=5, command=self.open_settings
                  ).pack(side="right")

        if not self.admin:
            self.btn_real.configure(state="disabled")
            self.btn_placebo.configure(state="disabled")

        # Prozess-Tabelle
        tablebox = tk.Frame(self.root, bg=C_PANEL, highlightthickness=1,
                            highlightbackground=C_ACCENT_D)
        tablebox.pack(fill="both", expand=True, pady=(2, 6), **pad)
        tk.Label(tablebox, text=t("topList"), font=FONT_BOLD,
                 bg=C_PANEL, fg=C_TEXT).pack(anchor="w", padx=10,
                                             pady=(8, 2))
        self.table = tk.Frame(tablebox, bg=C_PANEL)
        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # Fußnoten: Kochbuch 🍳 + Eigenverbrauch
        self.lbl_cookbook = tk.Label(
            self.root,
            text=t("cookbook"),
            font=FONT_SMALL, bg=C_BG, fg=C_MUTED, wraplength=520,
            justify="left")
        self.lbl_cookbook.pack(fill="x", pady=(0, 2), **pad)
        self.lbl_self = tk.Label(self.root, text="", font=FONT_SMALL,
                                 bg=C_BG, fg=C_MUTED)
        self.lbl_self.pack(anchor="w", pady=(0, 10), **pad)

    # ── Overlay (optional, Usage-Ticker-Vibe) ────────────────────────
    def _build_overlay(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        try:
            self.overlay.attributes("-alpha",
                                    float(CFG.get("overlay_alpha", 0.28)))
        except Exception:
            pass
        self.overlay.configure(bg=C_BG, highlightthickness=1,
                               highlightbackground=C_ACCENT_D)
        self.lbl_overlay = tk.Label(self.overlay, text="❄ …",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=C_BG, fg=C_ACCENT, padx=10, pady=4)
        self.lbl_overlay.pack()
        self.overlay.geometry(f"+{CFG['overlay_x']}+{CFG['overlay_y']}")

        # ziehbar machen
        self.lbl_overlay.bind("<Button-1>", self._ov_start)
        self.lbl_overlay.bind("<B1-Motion>", self._ov_drag)
        self.lbl_overlay.bind("<ButtonRelease-1>", self._ov_drop)
        self._ov_off = (0, 0)

        if not CFG["overlay"]:
            self.overlay.withdraw()

    def _ov_start(self, e):
        self._ov_off = (e.x, e.y)

    def _ov_drag(self, e):
        x = self.overlay.winfo_pointerx() - self._ov_off[0]
        y = self.overlay.winfo_pointery() - self._ov_off[1]
        self.overlay.geometry(f"+{x}+{y}")

    def _ov_drop(self, _):
        CFG["overlay_x"] = self.overlay.winfo_x()
        CFG["overlay_y"] = self.overlay.winfo_y()
        save_cfg(CFG)

    # ── Tray ─────────────────────────────────────────────────────────
    def _build_tray(self):
        def q(fn):
            """Tray-Callback → sicher in den Tk-Thread schieben."""
            def wrapper(icon=None, item=None):
                with self.actions_lock:
                    self.actions.append(fn)
            return wrapper

        menu = TrayMenu(
            TrayItem(t("trayDashboard"), q(self.show_dashboard),
                     default=True),
            TrayItem(t("trayReal"), q(self.do_real_clean)),
            TrayItem(t("trayPlacebo"), q(self.do_placebo)),
            TrayMenu.SEPARATOR,
            TrayItem(t("traySettings"), q(self.open_settings)),
            TrayItem(t("trayQuit"), q(self.quit_app)),
        )
        self.tray = pystray.Icon(APP_NAME, make_icon_image(64),
                                 f"{APP_NAME} ❄", menu=menu)

        def run_tray():
            # Learning vom Ticker: notify() erst NACH Icon-Init benutzen.
            def setup(icon):
                icon.visible = True
                self.tray_ready = True
            self.tray.run(setup=setup)

        threading.Thread(target=run_tray, daemon=True).start()

    def notify(self, title, msg):
        if self.tray_ready:
            try:
                self.tray.notify(msg, title)
            except Exception:
                pass

    # ── Aktionen ─────────────────────────────────────────────────────
    def do_real_clean(self):
        """DAS ECHTE: Standby-Liste leeren, mit Vorher/Nachher."""
        if not self.admin:
            messagebox.showwarning(APP_NAME, t("needAdmin"))
            return
        before = get_standby_bytes()
        ok = purge_standby_list()
        time.sleep(0.25)              # Windows kurz atmen lassen
        after = get_standby_bytes()

        if ok:
            if before is not None and after is not None:
                freed = max(0, before - after)
                text = t("realDone", before=fmt_mb(before),
                         after=fmt_mb(after), freed=fmt_mb(freed))
            else:
                text = t("realDoneNoMeasure")
            self.set_banner(text, C_GOOD)
            self.notify(t("notifyRealTitle"), text.replace("🎮 ", ""))
        else:
            self.set_banner(t("realFail"), C_WARN)
        self.refresh_now()

    def do_placebo(self):
        """DER GAG: ehrlich beschriftetes Working-Set-Trimmen."""
        if not self.admin:
            return
        rows_before = get_memory_status()
        avail_before = rows_before[1]
        n = trim_working_sets()
        time.sleep(0.25)
        _, avail_after = get_memory_status()
        delta = max(0, avail_after - avail_before)
        self.set_banner(t("placeboDone", n=n, delta=fmt_mb(delta)), C_ACCENT)
        self.refresh_now()

    def set_banner(self, text, color):
        self.banner.configure(text=text, fg=color)
        self.banner_until = time.time() + 25

    # ── Fenster-Steuerung ────────────────────────────────────────────
    def show_dashboard(self):
        self.root.deiconify()
        self.root.lift()
        self.refresh_now()

    def hide_dashboard(self):
        self.root.withdraw()
        # Ab ins Tray = Leerlauf → eigene Seiten abgeben
        self.root.after(500, trim_self)

    def quit_app(self):
        try:
            if self.tray:
                self.tray.stop()
        except Exception:
            pass
        self.root.after(50, self.root.destroy)

    # ── Einstellungen ────────────────────────────────────────────────
    def open_settings(self):
        if getattr(self, "_settings", None) and \
           self._settings.winfo_exists():
            self._settings.lift()
            return
        w = self._settings = tk.Toplevel(self.root)
        w.title(t("setTitle"))
        w.configure(bg=C_BG)
        w.geometry("500x560")
        w.resizable(False, False)
        pad = {"padx": 16}

        def sec(text):
            tk.Label(w, text=text, font=FONT_BOLD, bg=C_BG,
                     fg=C_ACCENT).pack(anchor="w", pady=(14, 2), **pad)

        def check(text, key, cb=None):
            var = tk.BooleanVar(value=CFG[key])
            def on_change():
                CFG[key] = var.get()
                save_cfg(CFG)
                if cb:
                    cb(var.get())
            c = tk.Checkbutton(w, text=text, variable=var, font=FONT,
                               wraplength=430, justify="left",
                               bg=C_BG, fg=C_TEXT, selectcolor=C_PANEL,
                               activebackground=C_BG,
                               activeforeground=C_ACCENT,
                               command=on_change)
            c.pack(anchor="w", **pad)
            return var

        # Automatik (ISLC-Stil)
        sec(t("secAuto"))
        check(t("chkAuto"), "auto_clean")

        def slider(text, key, lo, hi):
            row = tk.Frame(w, bg=C_BG)
            row.pack(fill="x", **pad)
            lbl = tk.Label(row, text="", font=FONT_SMALL, bg=C_BG,
                           fg=C_MUTED, width=34, anchor="w")
            def upd(v):
                CFG[key] = int(float(v))
                lbl.configure(text=f"{text}: {CFG[key]} MB")
            s = tk.Scale(row, from_=lo, to=hi, orient="horizontal",
                         resolution=128, showvalue=False, length=180,
                         bg=C_BG, fg=C_TEXT, troughcolor=C_PANEL,
                         highlightthickness=0, activebackground=C_ACCENT,
                         command=upd)
            s.set(CFG[key])
            s.bind("<ButtonRelease-1>", lambda e: save_cfg(CFG))
            lbl.pack(side="left")
            s.pack(side="right")
            upd(CFG[key])

        slider(t("sliderStandby"), "standby_threshold_mb", 256, 4096)
        slider(t("sliderFree"), "free_threshold_mb", 256, 4096)

        # Overlay
        sec(t("secOverlay"))
        def toggle_overlay(on):
            if on:
                self.overlay.deiconify()
            else:
                self.overlay.withdraw()
        check(t("chkOverlay"), "overlay", toggle_overlay)

        # Autostart
        sec(t("secAutostart"))
        CFG["autostart"] = autostart_enabled()   # echten Zustand spiegeln
        def toggle_autostart(on):
            ok, err = set_autostart(on)
            if not ok:
                CFG["autostart"] = not on
                save_cfg(CFG)
                messagebox.showerror(APP_NAME,
                    t("taskErr", err=err or t("unknownErr")))
                w.lift()
        check(t("chkAutostart"), "autostart", toggle_autostart)

        # Sprache / Language
        sec(t("secLang"))
        lang_var = tk.StringVar(value=CFG.get("language", "auto"))
        lang_row = tk.Frame(w, bg=C_BG)
        lang_row.pack(anchor="w", **pad)

        def on_lang_change():
            CFG["language"] = lang_var.get()
            save_cfg(CFG)
            messagebox.showinfo(APP_NAME, t("langSaved"))
            w.lift()

        for val, label in ((("auto"), t("langAuto")),
                           ("de", "Deutsch"), ("en", "English")):
            tk.Radiobutton(lang_row, text=label, value=val,
                           variable=lang_var, font=FONT, bg=C_BG,
                           fg=C_TEXT, selectcolor=C_PANEL,
                           activebackground=C_BG,
                           activeforeground=C_ACCENT,
                           command=on_lang_change
                           ).pack(side="left", padx=(0, 12))

        tk.Label(w, text=t("adminHint"),
                 font=FONT_SMALL, bg=C_BG, fg=C_MUTED, wraplength=420,
                 justify="left").pack(anchor="w", pady=(16, 0), **pad)

    # ── Anzeige-Aktualisierung ───────────────────────────────────────
    def refresh_now(self):
        self._read_stats()
        self._draw_bar()
        self._draw_table()
        self._draw_overlay()
        self.lbl_self.configure(text=t("selfUse", mb=f"{own_memory_mb():.0f}"))

    def _read_stats(self):
        self.total, self.avail = get_memory_status()
        self.standby = get_standby_bytes()

    def _draw_bar(self):
        self.bar.delete("all")
        w = max(self.bar.winfo_width(), 100)
        h = 30
        total = self.total or 1
        used = total - self.avail
        stby = self.standby if self.standby is not None else 0
        stby = min(stby, self.avail)          # Sicherheitsnetz
        free = self.avail - stby

        x = 0
        for val, col in ((used, C_BAR_USED), (stby, C_BAR_STBY),
                         (free, C_BAR_FREE)):
            seg = int(w * val / total)
            if seg > 0:
                self.bar.create_rectangle(x, 4, x + seg, h - 4,
                                          fill=col, width=0)
            x += seg

        if self.standby is not None:
            legend = t("legendFull", used=fmt_gb(used), stby=fmt_mb(stby),
                       free=fmt_gb(free), total=fmt_gb(total))
        else:
            legend = t("legendNoPdh", used=fmt_gb(used),
                       avail=fmt_gb(self.avail))
        self.lbl_legend.configure(text=legend)

    def _draw_table(self):
        for child in self.table.winfo_children():
            child.destroy()

        priv_head = t("colOwns") if EX2_SUPPORTED else t("colOwns") + "*"
        headers = (t("colProcess"), t("colCount"), t("colTouched"), priv_head)
        widths  = (24, 5, 10, 10)
        for col, (txt, wd) in enumerate(zip(headers, widths)):
            tk.Label(self.table, text=txt, font=FONT_BOLD, bg=C_PANEL,
                     fg=C_ACCENT, width=wd,
                     anchor="w" if col == 0 else "e"
                     ).grid(row=0, column=col, sticky="we", pady=(0, 3))

        for r, (name, cnt, ws, priv) in enumerate(list_top_processes(12),
                                                  start=1):
            vals = (name[:26], f"{cnt}×" if cnt > 1 else "",
                    fmt_mb(ws).replace(" MB", ""),
                    fmt_mb(priv).replace(" MB", ""))
            for col, txt in enumerate(vals):
                tk.Label(self.table, text=txt,
                         font=FONT_MONO if col else FONT,
                         bg=C_PANEL, fg=C_TEXT if col == 0 else C_MUTED,
                         anchor="w" if col == 0 else "e"
                         ).grid(row=r, column=col, sticky="we")
        self.table.grid_columnconfigure(0, weight=1)

        if EX2_SUPPORTED is False:
            tk.Label(self.table,
                     text=t("ex2Fallback"),
                     font=FONT_SMALL, bg=C_PANEL, fg=C_MUTED
                     ).grid(row=13, column=0, columnspan=4, sticky="w",
                            pady=(4, 0))

    def _draw_overlay(self):
        if not CFG["overlay"]:
            return
        if self.standby is not None:
            free = self.avail - min(self.standby, self.avail)
            self.lbl_overlay.configure(
                text=t("ovFull", free=fmt_gb(free),
                       stby=fmt_mb(self.standby)))
        else:
            self.lbl_overlay.configure(
                text=t("ovNoPdh", avail=fmt_gb(self.avail)))

    # ── Der Herzschlag: alle 3 s ─────────────────────────────────────
    def _tick(self):
        # 1) Tray-Aktionen abarbeiten (thread-sicher in Tk)
        with self.actions_lock:
            pending, self.actions = self.actions, []
        for fn in pending:
            try:
                fn()
            except Exception as e:
                print("Aktion fehlgeschlagen:", e)

        # 2) Messwerte + Anzeige
        try:
            self._read_stats()
            self._draw_overlay()
            if self.root.state() != "withdrawn":
                self._draw_bar()
                self._draw_table()
                self.lbl_self.configure(
                    text=t("selfUse", mb=f"{own_memory_mb():.0f}"))
        except Exception as e:
            print("Anzeige-Update fehlgeschlagen:", e)

        # 3) Banner nach 25 s ausblenden
        if self.banner_until and time.time() > self.banner_until:
            self.banner.configure(text="")
            self.banner_until = 0.0

        # 4) Automatik (ISLC-Logik): Standby > X UND frei < Y → leeren.
        #    Cooldown 120 s, damit wir nicht im Kreis putzen.
        try:
            if (CFG["auto_clean"] and self.admin
                    and self.standby is not None
                    and time.time() - self.last_auto_purge > 120):
                stby_mb = self.standby / (1024 * 1024)
                free_mb = (self.avail - min(self.standby, self.avail)) \
                          / (1024 * 1024)
                if (stby_mb > CFG["standby_threshold_mb"]
                        and free_mb < CFG["free_threshold_mb"]):
                    before = self.standby
                    if purge_standby_list():
                        self.last_auto_purge = time.time()
                        time.sleep(0.2)
                        after = get_standby_bytes() or 0
                        freed = max(0, before - after)
                        self.notify(t("autoTitle"),
                                    t("autoNotify", before=fmt_mb(before),
                                      after=fmt_mb(after), freed=fmt_mb(freed)))
                        self.set_banner(
                            t("autoBanner", before=fmt_mb(before),
                              after=fmt_mb(after)), C_GOOD)
        except Exception as e:
            print("Automatik-Fehler:", e)

        self.root.after(3000, self._tick)

    def run(self):
        self.refresh_now()
        self.root.mainloop()

# ═════════════════════════════════════════════════════════════════════
#  TRAY-ICON: Eisblaue Schneeflocke, mit PIL gezeichnet
# ═════════════════════════════════════════════════════════════════════

def make_icon_image(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # dunkler runder Grund
    d.ellipse((2, 2, size - 2, size - 2), fill=(13, 20, 32, 255),
              outline=(43, 143, 179, 255), width=2)
    # 6-strahlige Schneeflocke
    cx = cy = size / 2
    r_long, r_tick = size * 0.36, size * 0.12
    ice = (102, 224, 255, 255)
    import math
    for i in range(6):
        a = math.radians(i * 60)
        x2, y2 = cx + r_long * math.cos(a), cy + r_long * math.sin(a)
        d.line((cx, cy, x2, y2), fill=ice, width=max(2, size // 20))
        # kleine Seitenzweige
        for frac in (0.55, 0.8):
            bx, by = cx + r_long * frac * math.cos(a), \
                     cy + r_long * frac * math.sin(a)
            for da in (math.radians(35), -math.radians(35)):
                tx = bx + r_tick * math.cos(a + da)
                ty = by + r_tick * math.sin(a + da)
                d.line((bx, by, tx, ty), fill=ice,
                       width=max(1, size // 28))
    return img

# ═════════════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════════════

def main():
    # icon.ico für den PyInstaller-Build erzeugen:
    #   python real_ram_cooler.py --make-icon
    if "--make-icon" in sys.argv:
        sizes = [16, 24, 32, 48, 64, 128, 256]
        img = make_icon_image(256)
        path = os.path.join(app_dir(), "icon.ico")
        img.save(path, format="ICO", sizes=[(s, s) for s in sizes])
        print("icon.ico erstellt:", path)
        sys.exit(0)

    # DPI-Awareness → knackscharfes Tkinter auf 1440p
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    # Einzel-Instanz (sonst zwei Tray-Schneeflocken = Verwirrung)
    kernel32.CreateMutexW(None, False, f"{APP_NAME}_Mutex")
    ERROR_ALREADY_EXISTS = 183
    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        ctypes.windll.user32.MessageBoxW(
            None, f"{APP_NAME} " + t("alreadyRunning"),
            APP_NAME, 0x40)
        sys.exit(0)

    # Entscheidung 4A: immer als Admin. Die .exe erledigt das via
    # --uac-admin selbst; im Skript-Modus erhöhen wir uns hier einmal.
    if not is_admin() and os.environ.get("RRC_ELEVATION_TRIED") != "1":
        os.environ["RRC_ELEVATION_TRIED"] = "1"
        if relaunch_as_admin():
            sys.exit(0)
        # UAC abgelehnt → ehrlich weiterlaufen im Nur-Anzeige-Modus.

    app = RealRAMCooler()
    app.run()

if __name__ == "__main__":
    main()
