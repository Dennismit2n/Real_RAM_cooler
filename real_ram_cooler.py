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
import tkinter.font as tkfont
from tkinter import messagebox
from ctypes import wintypes, byref, sizeof

import pystray
from pystray import MenuItem as TrayItem, Menu as TrayMenu
from PIL import Image, ImageDraw

APP_NAME = "Real_RAM_cooler"
VERSION = "1.3.3"
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
#  SPRACHEN: 14 wie die Startseite (handpoliert, inkl. Wortwitz).
#  Start folgt der Windows-Anzeigesprache; in den Einstellungen
#  umschaltbar (config.json: "language": "auto" | "de" | "en" | "es" | …).
# ═════════════════════════════════════════════════════════════════════

L = {
    "de": {
        "adminOk": "Admin ✓",
        "adminNo": "kein Admin, nur Anzeige",
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
        "cookbook": ("🍳 „Berührt“ = alles, was der Prozess nutzt, auch "
                     "das geteilte Kochbuch auf dem WG-Tisch (DLLs). "
                     "„Besitzt“ = nur seine eigenen Seiten (die Task-Manager-Zahl)."),
        "ex2Fallback": ("* Dieses Windows liefert kein privates Working Set, "
                        "angezeigt werden Private Bytes (Commit)."),
        "selfUse": ("Eigenverbrauch: {mb} MB, ein RAM-Tool sollte selbst "
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
        "realFail": "Leeren fehlgeschlagen, fehlen Admin-Rechte?",
        "notifyRealTitle": "Bereit fürs Gaming 🎮",
        "placeboDone": ("✨ Zahlen poliert: {n} Prozesse getrimmt, {delta} "
                        "„befreit“. Gefühlt schneller: 100 %. Messbar schneller: 0 %. "
                        "(Windows räumt’s gleich zurück, grüß mir Memory "
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
        "langSaved": "Sprache gespeichert, gilt ab dem nächsten Start der App.",
        "alreadyRunning": "läuft bereits (Blick ins Tray ❄).",
        "niceDwm": "dwm (Desktopfenster)",
    },
    "en": {
        "adminOk": "Admin ✓",
        "adminNo": "no admin, view only",
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
        "cookbook": ("🍳 “Touches” = everything the process uses, including "
                     "the shared cookbook on the kitchen table (DLLs). "
                     "“Owns” = only its own pages (the Task Manager number)."),
        "ex2Fallback": ("* This Windows build doesn't report private working "
                        "sets, so it shows Private Bytes (commit) instead."),
        "selfUse": ("Own footprint: {mb} MB, a RAM tool shouldn't hog any "
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
        "realFail": "Purge failed, missing admin rights?",
        "notifyRealTitle": "Ready for gaming 🎮",
        "placeboDone": ("✨ Numbers polished: {n} processes trimmed, {delta} "
                        "“freed”. Feels faster: 100%. Measurably faster: 0%. "
                        "(Windows puts it all back in a second, say hi to "
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
        "langSaved": "Language saved, takes effect the next time the app starts.",
        "alreadyRunning": "is already running (check the tray ❄).",
        "niceDwm": "dwm (desktop windows)",
    },
    "es": {
        "adminOk": "Admin ✓",
        "adminNo": "sin admin: solo vista",
        "btnReal": "🎮  Limpiar para jugar",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Recorta los working sets: deja bonitos los números del Administrador de tareas, pero no hace más rápido el PC. Windows lo mete todo en Memory Compression y lo recupera enseguida. Palabra de honor. 😉",
        "topList": "Los 12 que más RAM comen",
        "colProcess": "Proceso",
        "colCount": "Cant.",
        "colTouched": "Toca",
        "colOwns": "Posee",
        "cookbook": "🍳 «Toca» = todo lo que usa el proceso, incluido el libro de cocina compartido en la mesa del piso (DLL). «Posee» = solo sus propias páginas (el número del Administrador de tareas).",
        "ex2Fallback": "* Este Windows no informa del working set privado: se muestran los Private Bytes (commit).",
        "selfUse": "Consumo propio: {mb} MB. Una herramienta de RAM no debería comérsela. 😉",
        "legendFull": "● En uso {used}   ● Standby {stby}   ● Libre de verdad {free}   (total {total})",
        "legendNoPdh": "● En uso {used}   ● Disponible {avail}   (contadores de standby no disponibles)",
        "ovFull": "❄ Libre {free} · Standby {stby}",
        "ovNoPdh": "❄ Disponible {avail}",
        "realDone": "🎮 Lista standby vaciada: {before} → {after} ✓  ({freed} liberados para tu juego)",
        "realDoneNoMeasure": "🎮 Lista standby vaciada ✓ (medición no disponible)",
        "realFail": "No se pudo vaciar. ¿Faltan permisos de administrador?",
        "notifyRealTitle": "Listo para jugar 🎮",
        "placeboDone": "✨ Números pulidos: {n} procesos recortados, {delta} «liberados». Más rápido a la vista: 100 %. Más rápido medible: 0 %. (Windows lo devuelve enseguida, saludos a Memory Compression. 😉)",
        "needAdmin": "Sin permisos de administrador, Windows no deja vaciar la lista standby. Inicia la app como administrador.",
        "autoTitle": "Automático ❄",
        "autoNotify": "Standby vaciado: {before} → {after} ({freed} libres)",
        "autoBanner": "❄ Automático: standby {before} → {after} ✓",
        "trayDashboard": "Abrir panel",
        "trayReal": "🎮 Limpiar para jugar",
        "trayPlacebo": "✨ Modo placebo",
        "traySettings": "⚙ Ajustes",
        "trayQuit": "Salir",
        "setTitle": "Ajustes ❄",
        "secAuto": "Automático (estilo ISLC)",
        "chkAuto": "Vaciar automáticamente cuando se superen ambos umbrales",
        "sliderStandby": "vaciar si el standby supera",
        "sliderFree": "y lo libre de verdad baja de",
        "secOverlay": "Overlay",
        "chkOverlay": "Mostrar mini overlay flotante (se puede arrastrar)",
        "secAutostart": "Inicio automático",
        "chkAutostart": "Iniciar con Windows (Programador de tareas, sin aviso de UAC al arrancar)",
        "taskErr": "El Programador de tareas dice:\n{err}",
        "unknownErr": "error desconocido",
        "adminHint": "Nota: la app necesita permisos de administrador porque Windows solo permite vaciar la lista standby así.",
        "secLang": "Idioma / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Idioma guardado. Se aplica la próxima vez que inicies la app.",
        "alreadyRunning": "ya está en marcha (mira en la bandeja ❄).",
        "niceDwm": "dwm (ventanas del escritorio)",
    },
    "fr": {
        "adminOk": "Admin ✓",
        "adminNo": "pas admin : affichage seul",
        "btnReal": "🎮  Nettoyer pour jouer",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Réduit les working sets : rend jolis les chiffres du Gestionnaire des tâches, pas votre PC plus rapide. Windows envoie tout dans Memory Compression et le reprend aussitôt. Parole d’honneur. 😉",
        "topList": "Les 12 plus gros mangeurs de RAM",
        "colProcess": "Processus",
        "colCount": "Nb",
        "colTouched": "Touche",
        "colOwns": "Possède",
        "cookbook": "🍳 « Touche » = tout ce que le processus utilise, y compris le livre de cuisine partagé sur la table de la coloc (DLL). « Possède » = seulement ses propres pages (le chiffre du Gestionnaire des tâches).",
        "ex2Fallback": "* Ce Windows ne fournit pas de working set privé : affichage des Private Bytes (commit).",
        "selfUse": "Consommation propre : {mb} MB. Un outil RAM ne devrait pas en dévorer lui-même. 😉",
        "legendFull": "● Utilisée {used}   ● Standby {stby}   ● Vraiment libre {free}   (total {total})",
        "legendNoPdh": "● Utilisée {used}   ● Disponible {avail}   (compteurs standby indisponibles)",
        "ovFull": "❄ Libre {free} · Standby {stby}",
        "ovNoPdh": "❄ Disponible {avail}",
        "realDone": "🎮 Liste standby vidée : {before} → {after} ✓  ({freed} libérés pour votre jeu)",
        "realDoneNoMeasure": "🎮 Liste standby vidée ✓ (mesure indisponible)",
        "realFail": "Échec du vidage. Droits d’administrateur manquants ?",
        "notifyRealTitle": "Prêt à jouer 🎮",
        "placeboDone": "✨ Chiffres polis : {n} processus réduits, {delta} « libérés ». Ressenti plus rapide : 100 %. Mesurablement plus rapide : 0 %. (Windows remet tout en place aussitôt, bonjour à Memory Compression. 😉)",
        "needAdmin": "Sans droits d’administrateur, Windows ne permet pas de vider la liste standby. Lancez l’application en tant qu’administrateur.",
        "autoTitle": "Automatique ❄",
        "autoNotify": "Standby vidé : {before} → {after} ({freed} libres)",
        "autoBanner": "❄ Automatique : standby {before} → {after} ✓",
        "trayDashboard": "Ouvrir le tableau de bord",
        "trayReal": "🎮 Nettoyer pour jouer",
        "trayPlacebo": "✨ Mode placebo",
        "traySettings": "⚙ Réglages",
        "trayQuit": "Quitter",
        "setTitle": "Réglages ❄",
        "secAuto": "Automatique (façon ISLC)",
        "chkAuto": "Vider automatiquement quand les deux seuils sont franchis",
        "sliderStandby": "vider si le standby dépasse",
        "sliderFree": "et si le vraiment libre passe sous",
        "secOverlay": "Overlay",
        "chkOverlay": "Afficher le mini overlay flottant (déplaçable)",
        "secAutostart": "Démarrage automatique",
        "chkAutostart": "Démarrer avec Windows (Planificateur de tâches, sans invite UAC au démarrage)",
        "taskErr": "Le Planificateur de tâches indique :\n{err}",
        "unknownErr": "erreur inconnue",
        "adminHint": "Remarque : l’application a besoin des droits d’administrateur, car Windows ne permet de vider la liste standby que de cette façon.",
        "secLang": "Langue / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Langue enregistrée. Elle s’applique au prochain démarrage de l’application.",
        "alreadyRunning": "est déjà lancé (regardez dans la zone de notification ❄).",
        "niceDwm": "dwm (fenêtres du bureau)",
    },
    "it": {
        "adminOk": "Admin ✓",
        "adminNo": "non admin: solo visualizzazione",
        "btnReal": "🎮  Pulisci per giocare",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Riduce i working set: rende belli i numeri di Gestione attività, non più veloce il PC. Windows sposta tutto in Memory Compression e lo riprende subito. Parola d’onore. 😉",
        "topList": "I 12 che mangiano più RAM",
        "colProcess": "Processo",
        "colCount": "N.",
        "colTouched": "Tocca",
        "colOwns": "Possiede",
        "cookbook": "🍳 «Tocca» = tutto ciò che il processo usa, compreso il ricettario condiviso sul tavolo dei coinquilini (DLL). «Possiede» = solo le sue pagine (il numero di Gestione attività).",
        "ex2Fallback": "* Questo Windows non fornisce il working set privato: mostro i Private Bytes (commit).",
        "selfUse": "Consumo proprio: {mb} MB. Uno strumento per la RAM non dovrebbe mangiarsela. 😉",
        "legendFull": "● In uso {used}   ● Standby {stby}   ● Davvero libera {free}   (totale {total})",
        "legendNoPdh": "● In uso {used}   ● Disponibile {avail}   (contatori standby non disponibili)",
        "ovFull": "❄ Libera {free} · Standby {stby}",
        "ovNoPdh": "❄ Disponibile {avail}",
        "realDone": "🎮 Lista standby svuotata: {before} → {after} ✓  ({freed} liberati per il gioco)",
        "realDoneNoMeasure": "🎮 Lista standby svuotata ✓ (misura non disponibile)",
        "realFail": "Svuotamento non riuscito. Mancano i diritti di amministratore?",
        "notifyRealTitle": "Pronto per giocare 🎮",
        "placeboDone": "✨ Numeri lucidati: {n} processi ridotti, {delta} «liberati». Più veloce a sensazione: 100%. Più veloce misurabile: 0%. (Windows rimette tutto a posto tra un attimo, salutami Memory Compression. 😉)",
        "needAdmin": "Senza diritti di amministratore Windows non permette di svuotare la lista standby. Avvia l’app come amministratore.",
        "autoTitle": "Automatico ❄",
        "autoNotify": "Standby svuotato: {before} → {after} ({freed} liberi)",
        "autoBanner": "❄ Automatico: standby {before} → {after} ✓",
        "trayDashboard": "Apri il pannello",
        "trayReal": "🎮 Pulisci per giocare",
        "trayPlacebo": "✨ Modalità placebo",
        "traySettings": "⚙ Impostazioni",
        "trayQuit": "Esci",
        "setTitle": "Impostazioni ❄",
        "secAuto": "Automatico (stile ISLC)",
        "chkAuto": "Svuota automaticamente quando entrambe le soglie vengono superate",
        "sliderStandby": "svuota se lo standby supera",
        "sliderFree": "e la RAM davvero libera scende sotto",
        "secOverlay": "Overlay",
        "chkOverlay": "Mostra il mini overlay mobile (trascinabile)",
        "secAutostart": "Avvio automatico",
        "chkAutostart": "Avvia con Windows (Utilità di pianificazione, senza richiesta UAC all’avvio)",
        "taskErr": "L’Utilità di pianificazione dice:\n{err}",
        "unknownErr": "errore sconosciuto",
        "adminHint": "Nota: l’app ha bisogno dei diritti di amministratore perché Windows permette di svuotare la lista standby solo così.",
        "secLang": "Lingua / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Lingua salvata. Vale dal prossimo avvio dell’app.",
        "alreadyRunning": "è già in esecuzione (guarda nell’area di notifica ❄).",
        "niceDwm": "dwm (finestre del desktop)",
    },
    "nl": {
        "adminOk": "Admin ✓",
        "adminNo": "geen admin: alleen weergave",
        "btnReal": "🎮  Opschonen voor gaming",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Trimt working sets: maakt de cijfers in Taakbeheer mooi, niet je pc sneller. Windows schuift alles in Memory Compression en haalt het meteen terug. Erewoord. 😉",
        "topList": "Top 12 RAM-vreters",
        "colProcess": "Proces",
        "colCount": "Aant.",
        "colTouched": "Raakt",
        "colOwns": "Bezit",
        "cookbook": "🍳 ‘Raakt’ = alles wat het proces gebruikt, inclusief het gedeelde kookboek op de keukentafel van het studentenhuis (DLL’s). ‘Bezit’ = alleen zijn eigen pagina’s (het getal in Taakbeheer).",
        "ex2Fallback": "* Deze Windows-versie levert geen privé-working set: weergave van Private Bytes (commit).",
        "selfUse": "Eigen verbruik: {mb} MB. Een RAM-tool hoort zelf niks op te vreten. 😉",
        "legendFull": "● In gebruik {used}   ● Standby {stby}   ● Echt vrij {free}   (totaal {total})",
        "legendNoPdh": "● In gebruik {used}   ● Beschikbaar {avail}   (standby-tellers niet beschikbaar)",
        "ovFull": "❄ Vrij {free} · Standby {stby}",
        "ovNoPdh": "❄ Beschikbaar {avail}",
        "realDone": "🎮 Standby-lijst geleegd: {before} → {after} ✓  ({freed} vrijgemaakt voor je game)",
        "realDoneNoMeasure": "🎮 Standby-lijst geleegd ✓ (meting niet beschikbaar)",
        "realFail": "Legen mislukt. Ontbreken er beheerdersrechten?",
        "notifyRealTitle": "Klaar om te gamen 🎮",
        "placeboDone": "✨ Cijfers opgepoetst: {n} processen getrimd, {delta} ‘bevrijd’. Gevoelsmatig sneller: 100%. Meetbaar sneller: 0%. (Windows zet het zo terug, doe Memory Compression de groeten. 😉)",
        "needAdmin": "Zonder beheerdersrechten laat Windows het legen van de standby-lijst niet toe. Start de app als administrator.",
        "autoTitle": "Automatisch ❄",
        "autoNotify": "Standby geleegd: {before} → {after} ({freed} vrij)",
        "autoBanner": "❄ Automatisch: standby {before} → {after} ✓",
        "trayDashboard": "Dashboard openen",
        "trayReal": "🎮 Opschonen voor gaming",
        "trayPlacebo": "✨ Placebomodus",
        "traySettings": "⚙ Instellingen",
        "trayQuit": "Afsluiten",
        "setTitle": "Instellingen ❄",
        "secAuto": "Automatisch (ISLC-stijl)",
        "chkAuto": "Automatisch legen als beide drempels worden overschreden",
        "sliderStandby": "legen als standby groter is dan",
        "sliderFree": "en echt vrij kleiner is dan",
        "secOverlay": "Overlay",
        "chkOverlay": "Zwevende mini-overlay tonen (versleepbaar)",
        "secAutostart": "Automatisch starten",
        "chkAutostart": "Met Windows starten (Taakplanner, zonder UAC-vraag bij het opstarten)",
        "taskErr": "Taakplanner meldt:\n{err}",
        "unknownErr": "onbekende fout",
        "adminHint": "Let op: de app heeft beheerdersrechten nodig, omdat Windows het legen van de standby-lijst alleen zo toestaat.",
        "secLang": "Taal / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Taal opgeslagen. Geldt vanaf de volgende start van de app.",
        "alreadyRunning": "draait al (kijk in het systeemvak ❄).",
        "niceDwm": "dwm (bureaubladvensters)",
    },
    "pl": {
        "adminOk": "Admin ✓",
        "adminNo": "bez admina: tylko podgląd",
        "btnReal": "🎮  Wyczyść pod gry",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Przycina working sety: upiększa liczby w Menedżerze zadań, ale nie przyspiesza komputera. Windows wrzuca wszystko do Memory Compression i zaraz to zabiera z powrotem. Słowo honoru. 😉",
        "topList": "12 największych pożeraczy RAM",
        "colProcess": "Proces",
        "colCount": "Ile",
        "colTouched": "Dotyka",
        "colOwns": "Ma",
        "cookbook": "🍳 „Dotyka” = wszystko, czego proces używa, łącznie ze wspólną książką kucharską na stole we wspólnym mieszkaniu (DLL). „Ma” = tylko jego własne strony (liczba z Menedżera zadań).",
        "ex2Fallback": "* Ten Windows nie podaje prywatnego working setu: pokazuję Private Bytes (commit).",
        "selfUse": "Własne zużycie: {mb} MB. Narzędzie do RAM nie powinno samo go zjadać. 😉",
        "legendFull": "● W użyciu {used}   ● Standby {stby}   ● Naprawdę wolne {free}   (razem {total})",
        "legendNoPdh": "● W użyciu {used}   ● Dostępne {avail}   (liczniki standby niedostępne)",
        "ovFull": "❄ Wolne {free} · Standby {stby}",
        "ovNoPdh": "❄ Dostępne {avail}",
        "realDone": "🎮 Lista standby wyczyszczona: {before} → {after} ✓  ({freed} zwolnione dla gry)",
        "realDoneNoMeasure": "🎮 Lista standby wyczyszczona ✓ (pomiar niedostępny)",
        "realFail": "Czyszczenie się nie udało. Brak praw administratora?",
        "notifyRealTitle": "Gotowe do grania 🎮",
        "placeboDone": "✨ Liczby wypolerowane: przycięte procesy: {n}, „uwolnione”: {delta}. Szybciej na oko: 100%. Szybciej w pomiarze: 0%. (Windows zaraz wszystko odda, pozdrów ode mnie Memory Compression. 😉)",
        "needAdmin": "Bez praw administratora Windows nie pozwala czyścić listy standby. Uruchom aplikację jako administrator.",
        "autoTitle": "Automatycznie ❄",
        "autoNotify": "Standby wyczyszczony: {before} → {after} (wolne {freed})",
        "autoBanner": "❄ Automatycznie: standby {before} → {after} ✓",
        "trayDashboard": "Otwórz panel",
        "trayReal": "🎮 Wyczyść pod gry",
        "trayPlacebo": "✨ Tryb placebo",
        "traySettings": "⚙ Ustawienia",
        "trayQuit": "Zakończ",
        "setTitle": "Ustawienia ❄",
        "secAuto": "Automatycznie (w stylu ISLC)",
        "chkAuto": "Czyść automatycznie, gdy oba progi zostaną przekroczone",
        "sliderStandby": "czyść, gdy standby większe niż",
        "sliderFree": "i naprawdę wolne mniejsze niż",
        "secOverlay": "Nakładka",
        "chkOverlay": "Pokaż pływającą mini nakładkę (do przeciągania)",
        "secAutostart": "Autostart",
        "chkAutostart": "Uruchamiaj z Windows (Harmonogram zadań, bez pytania UAC przy starcie)",
        "taskErr": "Harmonogram zadań zgłasza:\n{err}",
        "unknownErr": "nieznany błąd",
        "adminHint": "Uwaga: aplikacja potrzebuje praw administratora, bo tylko wtedy Windows pozwala czyścić listę standby.",
        "secLang": "Język / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Język zapisany. Obowiązuje od następnego uruchomienia aplikacji.",
        "alreadyRunning": "już działa (zajrzyj do zasobnika ❄).",
        "niceDwm": "dwm (okna pulpitu)",
    },
    "pt": {
        "adminOk": "Admin ✓",
        "adminNo": "sem admin: só exibição",
        "btnReal": "🎮  Limpar para jogar",
        "btnPlacebo": "✨ Placebo",
        "tipPlacebo": "Corta os working sets: deixa bonitos os números do Gerenciador de Tarefas, não o PC mais rápido. O Windows joga tudo na Memory Compression e pega de volta na hora. Palavra de honra. 😉",
        "topList": "Os 12 maiores comilões de RAM",
        "colProcess": "Processo",
        "colCount": "Qtd.",
        "colTouched": "Toca",
        "colOwns": "Possui",
        "cookbook": "🍳 «Toca» = tudo o que o processo usa, inclusive o livro de receitas compartilhado na mesa da república (DLLs). «Possui» = só as páginas dele (o número do Gerenciador de Tarefas).",
        "ex2Fallback": "* Este Windows não informa o working set privado: exibindo Private Bytes (commit).",
        "selfUse": "Consumo próprio: {mb} MB. Uma ferramenta de RAM não deveria comer RAM. 😉",
        "legendFull": "● Em uso {used}   ● Standby {stby}   ● Livre de verdade {free}   (total {total})",
        "legendNoPdh": "● Em uso {used}   ● Disponível {avail}   (contadores de standby indisponíveis)",
        "ovFull": "❄ Livre {free} · Standby {stby}",
        "ovNoPdh": "❄ Disponível {avail}",
        "realDone": "🎮 Lista standby esvaziada: {before} → {after} ✓  ({freed} liberados para o jogo)",
        "realDoneNoMeasure": "🎮 Lista standby esvaziada ✓ (medição indisponível)",
        "realFail": "Falha ao esvaziar. Faltam direitos de administrador?",
        "notifyRealTitle": "Pronto para jogar 🎮",
        "placeboDone": "✨ Números polidos: {n} processos cortados, {delta} «liberados». Mais rápido na sensação: 100%. Mais rápido de verdade: 0%. (O Windows devolve tudo num instante, mande um oi para a Memory Compression. 😉)",
        "needAdmin": "Sem direitos de administrador o Windows não deixa esvaziar a lista standby. Inicie o app como administrador.",
        "autoTitle": "Automático ❄",
        "autoNotify": "Standby esvaziado: {before} → {after} ({freed} livres)",
        "autoBanner": "❄ Automático: standby {before} → {after} ✓",
        "trayDashboard": "Abrir painel",
        "trayReal": "🎮 Limpar para jogar",
        "trayPlacebo": "✨ Modo placebo",
        "traySettings": "⚙ Configurações",
        "trayQuit": "Sair",
        "setTitle": "Configurações ❄",
        "secAuto": "Automático (estilo ISLC)",
        "chkAuto": "Esvaziar automaticamente quando os dois limites forem ultrapassados",
        "sliderStandby": "esvaziar se o standby passar de",
        "sliderFree": "e o livre de verdade ficar abaixo de",
        "secOverlay": "Overlay",
        "chkOverlay": "Mostrar mini overlay flutuante (arrastável)",
        "secAutostart": "Início automático",
        "chkAutostart": "Iniciar com o Windows (Agendador de Tarefas, sem aviso do UAC na inicialização)",
        "taskErr": "O Agendador de Tarefas diz:\n{err}",
        "unknownErr": "erro desconhecido",
        "adminHint": "Observação: o app precisa de direitos de administrador porque o Windows só deixa esvaziar a lista standby assim.",
        "secLang": "Idioma / Language",
        "langAuto": "Auto (Windows)",
        "langSaved": "Idioma salvo. Vale a partir da próxima vez que o app iniciar.",
        "alreadyRunning": "já está em execução (olhe na bandeja ❄).",
        "niceDwm": "dwm (janelas da área de trabalho)",
    },
    "tr": {
        "adminOk": "Admin ✓",
        "adminNo": "yönetici değil: yalnızca görüntüleme",
        "btnReal": "🎮  Oyun için temizle",
        "btnPlacebo": "✨ Plasebo",
        "tipPlacebo": "Working set’leri kırpar: Görev Yöneticisi’ndeki sayıları güzelleştirir, bilgisayarı hızlandırmaz. Windows her şeyi Memory Compression’a iter ve hemen geri alır. Söz. 😉",
        "topList": "En çok RAM yiyen 12 işlem",
        "colProcess": "İşlem",
        "colCount": "Adet",
        "colTouched": "Dokunur",
        "colOwns": "Sahip",
        "cookbook": "🍳 “Dokunur” = işlemin kullandığı her şey, ev arkadaşlarının ortak mutfak masasındaki yemek kitabı (DLL’ler) dahil. “Sahip” = yalnızca kendi sayfaları (Görev Yöneticisi’ndeki sayı).",
        "ex2Fallback": "* Bu Windows özel working set bildirmiyor: Private Bytes (commit) gösteriliyor.",
        "selfUse": "Kendi tüketimi: {mb} MB. Bir RAM aracı kendisi RAM yememeli. 😉",
        "legendFull": "● Kullanımda {used}   ● Bekleme {stby}   ● Gerçekten boş {free}   (toplam {total})",
        "legendNoPdh": "● Kullanımda {used}   ● Kullanılabilir {avail}   (bekleme sayaçları yok)",
        "ovFull": "❄ Boş {free} · Bekleme {stby}",
        "ovNoPdh": "❄ Kullanılabilir {avail}",
        "realDone": "🎮 Bekleme listesi boşaltıldı: {before} → {after} ✓  (oyununuz için {freed} açıldı)",
        "realDoneNoMeasure": "🎮 Bekleme listesi boşaltıldı ✓ (ölçüm yok)",
        "realFail": "Boşaltma başarısız. Yönetici hakları eksik mi?",
        "notifyRealTitle": "Oyuna hazır 🎮",
        "placeboDone": "✨ Sayılar parlatıldı: {n} işlem kırpıldı, {delta} “serbest bırakıldı”. Hissedilen hız: %100. Ölçülebilen hız: %0. (Windows birazdan hepsini geri koyar, Memory Compression’a selam söyleyin. 😉)",
        "needAdmin": "Yönetici hakları olmadan Windows bekleme listesinin boşaltılmasına izin vermez. Uygulamayı yönetici olarak başlatın.",
        "autoTitle": "Otomatik ❄",
        "autoNotify": "Bekleme boşaltıldı: {before} → {after} ({freed} boş)",
        "autoBanner": "❄ Otomatik: bekleme {before} → {after} ✓",
        "trayDashboard": "Paneli aç",
        "trayReal": "🎮 Oyun için temizle",
        "trayPlacebo": "✨ Plasebo modu",
        "traySettings": "⚙ Ayarlar",
        "trayQuit": "Çık",
        "setTitle": "Ayarlar ❄",
        "secAuto": "Otomatik (ISLC tarzı)",
        "chkAuto": "İki eşik de aşılınca otomatik boşalt",
        "sliderStandby": "bekleme şundan büyükse boşalt",
        "sliderFree": "ve gerçekten boş şundan küçükse",
        "secOverlay": "Katman",
        "chkOverlay": "Yüzen mini katmanı göster (sürüklenebilir)",
        "secAutostart": "Otomatik başlatma",
        "chkAutostart": "Windows ile başlat (Görev Zamanlayıcı, açılışta UAC sorusu yok)",
        "taskErr": "Görev Zamanlayıcı diyor ki:\n{err}",
        "unknownErr": "bilinmeyen hata",
        "adminHint": "Not: Uygulama yönetici haklarına ihtiyaç duyar, çünkü Windows bekleme listesinin boşaltılmasına yalnızca böyle izin verir.",
        "secLang": "Dil / Language",
        "langAuto": "Otomatik (Windows)",
        "langSaved": "Dil kaydedildi. Uygulamanın bir sonraki başlatılışında geçerli olur.",
        "alreadyRunning": "zaten çalışıyor (bildirim alanına bakın ❄).",
        "niceDwm": "dwm (masaüstü pencereleri)",
    },
    "ru": {
        "adminOk": "Админ ✓",
        "adminNo": "без прав админа: только просмотр",
        "btnReal": "🎮  Очистить для игр",
        "btnPlacebo": "✨ Плацебо",
        "tipPlacebo": "Урезает рабочие наборы: числа в диспетчере задач становятся красивыми, а ПК быстрее не становится. Windows отправляет всё в Memory Compression и сразу забирает обратно. Честное слово. 😉",
        "topList": "12 главных пожирателей RAM",
        "colProcess": "Процесс",
        "colCount": "Шт.",
        "colTouched": "Касается",
        "colOwns": "Владеет",
        "cookbook": "🍳 «Касается» = всё, что использует процесс, включая общую поваренную книгу на кухонном столе в общаге (DLL). «Владеет» = только его собственные страницы (число из диспетчера задач).",
        "ex2Fallback": "* Эта версия Windows не сообщает частный рабочий набор: показаны Private Bytes (commit).",
        "selfUse": "Собственный расход: {mb} MB. Инструмент для RAM не должен сам её есть. 😉",
        "legendFull": "● Используется {used}   ● Резерв {stby}   ● Реально свободно {free}   (всего {total})",
        "legendNoPdh": "● Используется {used}   ● Доступно {avail}   (счётчики резерва недоступны)",
        "ovFull": "❄ Свободно {free} · Резерв {stby}",
        "ovNoPdh": "❄ Доступно {avail}",
        "realDone": "🎮 Резервный список очищен: {before} → {after} ✓  ({freed} освобождено для игры)",
        "realDoneNoMeasure": "🎮 Резервный список очищен ✓ (измерение недоступно)",
        "realFail": "Очистка не удалась. Нет прав администратора?",
        "notifyRealTitle": "Готово к игре 🎮",
        "placeboDone": "✨ Числа отполированы: урезано процессов: {n}, «освобождено» {delta}. Быстрее на ощущение: 100 %. Быстрее по замерам: 0 %. (Windows сейчас всё вернёт, передайте привет Memory Compression. 😉)",
        "needAdmin": "Без прав администратора Windows не разрешает очищать резервный список. Запустите приложение от имени администратора.",
        "autoTitle": "Автоматика ❄",
        "autoNotify": "Резерв очищен: {before} → {after} (свободно {freed})",
        "autoBanner": "❄ Автоматика: резерв {before} → {after} ✓",
        "trayDashboard": "Открыть панель",
        "trayReal": "🎮 Очистить для игр",
        "trayPlacebo": "✨ Режим плацебо",
        "traySettings": "⚙ Настройки",
        "trayQuit": "Выход",
        "setTitle": "Настройки ❄",
        "secAuto": "Автоматика (как ISLC)",
        "chkAuto": "Очищать автоматически, когда превышены оба порога",
        "sliderStandby": "очищать, если резерв больше",
        "sliderFree": "и реально свободно меньше",
        "secOverlay": "Оверлей",
        "chkOverlay": "Показывать плавающий мини-оверлей (можно перетаскивать)",
        "secAutostart": "Автозапуск",
        "chkAutostart": "Запускать вместе с Windows (Планировщик заданий, без запроса UAC при загрузке)",
        "taskErr": "Планировщик заданий сообщает:\n{err}",
        "unknownErr": "неизвестная ошибка",
        "adminHint": "Примечание: приложению нужны права администратора, потому что только так Windows разрешает очищать резервный список.",
        "secLang": "Язык / Language",
        "langAuto": "Авто (Windows)",
        "langSaved": "Язык сохранён. Он применится при следующем запуске приложения.",
        "alreadyRunning": "уже запущен (загляните в трей ❄).",
        "niceDwm": "dwm (окна рабочего стола)",
    },
    "hi": {
        "adminOk": "एडमिन ✓",
        "adminNo": "एडमिन नहीं: केवल देखना",
        "btnReal": "🎮  गेमिंग के लिए साफ़ करें",
        "btnPlacebo": "✨ प्लेसीबो",
        "tipPlacebo": "वर्किंग सेट छोटे करता है: टास्क मैनेजर के आँकड़े सुंदर दिखते हैं, पीसी तेज़ नहीं होता। Windows सब कुछ Memory Compression में डालता है और तुरंत वापस ले लेता है। वादा। 😉",
        "topList": "सबसे ज़्यादा RAM खाने वाले 12",
        "colProcess": "प्रोसेस",
        "colCount": "संख्या",
        "colTouched": "छूता है",
        "colOwns": "अपना",
        "cookbook": "🍳 “छूता है” = वह सब जो प्रोसेस इस्तेमाल करता है, फ़्लैट की रसोई की मेज़ पर रखी साझा रसोई की किताब (DLL) समेत। “अपना” = केवल उसके अपने पेज (टास्क मैनेजर वाला आँकड़ा)।",
        "ex2Fallback": "* यह Windows निजी वर्किंग सेट नहीं बताता: Private Bytes (commit) दिखाए जा रहे हैं।",
        "selfUse": "अपनी खपत: {mb} MB। RAM टूल को खुद RAM नहीं खानी चाहिए। 😉",
        "legendFull": "● उपयोग में {used}   ● स्टैंडबाय {stby}   ● सच में खाली {free}   (कुल {total})",
        "legendNoPdh": "● उपयोग में {used}   ● उपलब्ध {avail}   (स्टैंडबाय काउंटर उपलब्ध नहीं)",
        "ovFull": "❄ खाली {free} · स्टैंडबाय {stby}",
        "ovNoPdh": "❄ उपलब्ध {avail}",
        "realDone": "🎮 स्टैंडबाय सूची खाली हुई: {before} → {after} ✓  (गेम के लिए {freed} खाली)",
        "realDoneNoMeasure": "🎮 स्टैंडबाय सूची खाली हुई ✓ (माप उपलब्ध नहीं)",
        "realFail": "खाली नहीं हो सकी। क्या एडमिन अधिकार नहीं हैं?",
        "notifyRealTitle": "गेमिंग के लिए तैयार 🎮",
        "placeboDone": "✨ आँकड़े चमकाए: {n} प्रोसेस छोटे किए, {delta} “मुक्त”। महसूस में तेज़: 100%। मापने में तेज़: 0%। (Windows अभी सब वापस रख देगा, Memory Compression को मेरा नमस्ते कहिए। 😉)",
        "needAdmin": "एडमिन अधिकारों के बिना Windows स्टैंडबाय सूची खाली नहीं करने देता। कृपया ऐप को एडमिनिस्ट्रेटर के रूप में चलाएँ।",
        "autoTitle": "स्वचालित ❄",
        "autoNotify": "स्टैंडबाय खाली: {before} → {after} ({freed} खाली)",
        "autoBanner": "❄ स्वचालित: स्टैंडबाय {before} → {after} ✓",
        "trayDashboard": "डैशबोर्ड खोलें",
        "trayReal": "🎮 गेमिंग के लिए साफ़ करें",
        "trayPlacebo": "✨ प्लेसीबो मोड",
        "traySettings": "⚙ सेटिंग्स",
        "trayQuit": "बंद करें",
        "setTitle": "सेटिंग्स ❄",
        "secAuto": "स्वचालित (ISLC जैसा)",
        "chkAuto": "दोनों सीमाएँ पार होने पर अपने आप खाली करें",
        "sliderStandby": "खाली करें जब स्टैंडबाय इससे ज़्यादा हो",
        "sliderFree": "और सच में खाली इससे कम हो",
        "secOverlay": "ओवरले",
        "chkOverlay": "तैरता हुआ छोटा ओवरले दिखाएँ (खींचा जा सकता है)",
        "secAutostart": "अपने आप शुरू",
        "chkAutostart": "Windows के साथ शुरू करें (टास्क शेड्यूलर, बूट पर UAC प्रश्न नहीं)",
        "taskErr": "टास्क शेड्यूलर कहता है:\n{err}",
        "unknownErr": "अज्ञात त्रुटि",
        "adminHint": "ध्यान दें: ऐप को एडमिन अधिकार चाहिए, क्योंकि Windows केवल इसी तरह स्टैंडबाय सूची खाली करने देता है।",
        "secLang": "भाषा / Language",
        "langAuto": "ऑटो (Windows)",
        "langSaved": "भाषा सहेजी गई। ऐप के अगली बार शुरू होने पर लागू होगी।",
        "alreadyRunning": "पहले से चल रहा है (ट्रे में देखें ❄)।",
        "niceDwm": "dwm (डेस्कटॉप विंडो)",
    },
    "zh": {
        "adminOk": "管理员 ✓",
        "adminNo": "非管理员：仅显示",
        "btnReal": "🎮  为游戏清理",
        "btnPlacebo": "✨ 安慰剂",
        "tipPlacebo": "修剪工作集：任务管理器里的数字会变好看，电脑却不会变快。Windows 会把一切塞进 Memory Compression，又马上取回来。说真的。😉",
        "topList": "吃内存最多的 12 个",
        "colProcess": "进程",
        "colCount": "数量",
        "colTouched": "触及",
        "colOwns": "独占",
        "cookbook": "🍳 “触及” = 进程用到的一切，包括合租公寓餐桌上那本共用的菜谱（DLL）。“独占” = 只有它自己的页面（任务管理器里的数字）。",
        "ex2Fallback": "* 此 Windows 不提供专用工作集：显示 Private Bytes（提交）。",
        "selfUse": "自身占用：{mb} MB。内存工具自己可不该吃内存。😉",
        "legendFull": "● 使用中 {used}   ● 待机 {stby}   ● 真正空闲 {free}   （共 {total}）",
        "legendNoPdh": "● 使用中 {used}   ● 可用 {avail}   （待机计数器不可用）",
        "ovFull": "❄ 空闲 {free} · 待机 {stby}",
        "ovNoPdh": "❄ 可用 {avail}",
        "realDone": "🎮 待机列表已清空：{before} → {after} ✓  （为游戏腾出 {freed}）",
        "realDoneNoMeasure": "🎮 待机列表已清空 ✓（无法测量）",
        "realFail": "清空失败。是不是缺少管理员权限？",
        "notifyRealTitle": "准备好玩游戏了 🎮",
        "placeboDone": "✨ 数字已抛光：修剪了 {n} 个进程，“释放”了 {delta}。感觉更快：100%。测得更快：0%。（Windows 马上就会把它们放回去，替我向 Memory Compression 问好。😉）",
        "needAdmin": "没有管理员权限，Windows 不允许清空待机列表。请以管理员身份启动此应用。",
        "autoTitle": "自动 ❄",
        "autoNotify": "待机已清空：{before} → {after}（空闲 {freed}）",
        "autoBanner": "❄ 自动：待机 {before} → {after} ✓",
        "trayDashboard": "打开面板",
        "trayReal": "🎮 为游戏清理",
        "trayPlacebo": "✨ 安慰剂模式",
        "traySettings": "⚙ 设置",
        "trayQuit": "退出",
        "setTitle": "设置 ❄",
        "secAuto": "自动（ISLC 风格）",
        "chkAuto": "两个阈值都越过时自动清空",
        "sliderStandby": "待机大于此值时清空",
        "sliderFree": "且真正空闲小于",
        "secOverlay": "悬浮窗",
        "chkOverlay": "显示可拖动的迷你悬浮窗",
        "secAutostart": "开机启动",
        "chkAutostart": "随 Windows 启动（任务计划程序，开机时不弹 UAC）",
        "taskErr": "任务计划程序提示：\n{err}",
        "unknownErr": "未知错误",
        "adminHint": "提示：此应用需要管理员权限，因为 Windows 只允许这样清空待机列表。",
        "secLang": "语言 / Language",
        "langAuto": "自动（Windows）",
        "langSaved": "语言已保存，下次启动应用时生效。",
        "alreadyRunning": "已在运行（看看托盘 ❄）。",
        "niceDwm": "dwm（桌面窗口）",
    },
    "ja": {
        "adminOk": "管理者 ✓",
        "adminNo": "管理者ではありません：表示のみ",
        "btnReal": "🎮  ゲーム用にクリーンアップ",
        "btnPlacebo": "✨ プラシーボ",
        "tipPlacebo": "ワーキングセットを削ります。タスクマネージャーの数字はきれいになりますが、PC は速くなりません。Windows はすべてを Memory Compression に押し込み、すぐに取り戻します。本当です。😉",
        "topList": "RAM を食う上位 12",
        "colProcess": "プロセス",
        "colCount": "数",
        "colTouched": "触れている",
        "colOwns": "所有",
        "cookbook": "🍳 「触れている」= プロセスが使うすべて。シェアハウスの食卓にある共用のレシピ本（DLL）も含みます。「所有」= 自分専用のページだけ（タスクマネージャーの数字）。",
        "ex2Fallback": "* この Windows はプライベート ワーキングセットを返しません：Private Bytes（コミット）を表示しています。",
        "selfUse": "自身の使用量：{mb} MB。RAM ツールが自分で RAM を食べてはいけません。😉",
        "legendFull": "● 使用中 {used}   ● スタンバイ {stby}   ● 本当に空き {free}   （合計 {total}）",
        "legendNoPdh": "● 使用中 {used}   ● 利用可能 {avail}   （スタンバイのカウンターなし）",
        "ovFull": "❄ 空き {free} · スタンバイ {stby}",
        "ovNoPdh": "❄ 利用可能 {avail}",
        "realDone": "🎮 スタンバイリストを空にしました：{before} → {after} ✓  （ゲーム用に {freed} 確保）",
        "realDoneNoMeasure": "🎮 スタンバイリストを空にしました ✓（測定できません）",
        "realFail": "空にできませんでした。管理者権限がありませんか？",
        "notifyRealTitle": "ゲームの準備完了 🎮",
        "placeboDone": "✨ 数字を磨きました：{n} 個のプロセスを削り、{delta} を「解放」。体感の速さ：100%。測れる速さ：0%。（Windows がすぐに元に戻します。Memory Compression によろしく。😉）",
        "needAdmin": "管理者権限がないと、Windows はスタンバイリストを空にできません。アプリを管理者として起動してください。",
        "autoTitle": "自動 ❄",
        "autoNotify": "スタンバイを空にしました：{before} → {after}（空き {freed}）",
        "autoBanner": "❄ 自動：スタンバイ {before} → {after} ✓",
        "trayDashboard": "ダッシュボードを開く",
        "trayReal": "🎮 ゲーム用にクリーンアップ",
        "trayPlacebo": "✨ プラシーボモード",
        "traySettings": "⚙ 設定",
        "trayQuit": "終了",
        "setTitle": "設定 ❄",
        "secAuto": "自動（ISLC 風）",
        "chkAuto": "両方のしきい値を超えたら自動で空にする",
        "sliderStandby": "スタンバイがこれを超えたら空にする",
        "sliderFree": "かつ本当の空きがこれを下回ったら",
        "secOverlay": "オーバーレイ",
        "chkOverlay": "浮かぶミニオーバーレイを表示（ドラッグ可）",
        "secAutostart": "自動起動",
        "chkAutostart": "Windows と一緒に起動（タスク スケジューラ、起動時の UAC 確認なし）",
        "taskErr": "タスク スケジューラのメッセージ：\n{err}",
        "unknownErr": "不明なエラー",
        "adminHint": "注意：Windows はこの方法でしかスタンバイリストを空にできないため、アプリには管理者権限が必要です。",
        "secLang": "言語 / Language",
        "langAuto": "自動（Windows）",
        "langSaved": "言語を保存しました。次回アプリを起動したときに反映されます。",
        "alreadyRunning": "はすでに起動しています（トレイを見てください ❄）。",
        "niceDwm": "dwm（デスクトップ ウィンドウ）",
    },
    "ko": {
        "adminOk": "관리자 ✓",
        "adminNo": "관리자 아님: 보기 전용",
        "btnReal": "🎮  게임용으로 정리",
        "btnPlacebo": "✨ 플라세보",
        "tipPlacebo": "작업 집합을 줄입니다. 작업 관리자의 숫자는 예뻐지지만 PC가 빨라지지는 않습니다. Windows는 모든 것을 Memory Compression에 밀어 넣었다가 곧바로 되가져옵니다. 진짜예요. 😉",
        "topList": "RAM을 가장 많이 먹는 12개",
        "colProcess": "프로세스",
        "colCount": "개수",
        "colTouched": "건드림",
        "colOwns": "소유",
        "cookbook": "🍳 ‘건드림’ = 프로세스가 쓰는 모든 것. 셰어하우스 식탁 위의 공용 요리책(DLL)까지 포함합니다. ‘소유’ = 자기만의 페이지(작업 관리자에 나오는 숫자).",
        "ex2Fallback": "* 이 Windows는 개인 작업 집합을 알려 주지 않습니다: Private Bytes(커밋)를 표시합니다.",
        "selfUse": "자체 사용량: {mb} MB. RAM 도구가 스스로 RAM을 먹으면 안 되죠. 😉",
        "legendFull": "● 사용 중 {used}   ● 대기 {stby}   ● 진짜 여유 {free}   (전체 {total})",
        "legendNoPdh": "● 사용 중 {used}   ● 사용 가능 {avail}   (대기 카운터 없음)",
        "ovFull": "❄ 여유 {free} · 대기 {stby}",
        "ovNoPdh": "❄ 사용 가능 {avail}",
        "realDone": "🎮 대기 목록 비움: {before} → {after} ✓  (게임용으로 {freed} 확보)",
        "realDoneNoMeasure": "🎮 대기 목록 비움 ✓ (측정 불가)",
        "realFail": "비우지 못했습니다. 관리자 권한이 없나요?",
        "notifyRealTitle": "게임 준비 완료 🎮",
        "placeboDone": "✨ 숫자를 닦았습니다: 프로세스 {n}개 정리, {delta} ‘해제’. 체감 속도: 100%. 측정 속도: 0%. (Windows가 곧 다 되돌려 놓습니다. Memory Compression에 안부 전해 주세요. 😉)",
        "needAdmin": "관리자 권한이 없으면 Windows는 대기 목록 비우기를 허용하지 않습니다. 앱을 관리자 권한으로 실행하세요.",
        "autoTitle": "자동 ❄",
        "autoNotify": "대기 비움: {before} → {after} (여유 {freed})",
        "autoBanner": "❄ 자동: 대기 {before} → {after} ✓",
        "trayDashboard": "대시보드 열기",
        "trayReal": "🎮 게임용으로 정리",
        "trayPlacebo": "✨ 플라세보 모드",
        "traySettings": "⚙ 설정",
        "trayQuit": "종료",
        "setTitle": "설정 ❄",
        "secAuto": "자동 (ISLC 방식)",
        "chkAuto": "두 기준을 모두 넘으면 자동으로 비우기",
        "sliderStandby": "대기가 이보다 크면 비우기",
        "sliderFree": "그리고 진짜 여유가 이보다 작으면",
        "secOverlay": "오버레이",
        "chkOverlay": "떠 있는 미니 오버레이 표시 (끌어서 이동)",
        "secAutostart": "자동 시작",
        "chkAutostart": "Windows와 함께 시작 (작업 스케줄러, 부팅 시 UAC 확인 없음)",
        "taskErr": "작업 스케줄러 메시지:\n{err}",
        "unknownErr": "알 수 없는 오류",
        "adminHint": "참고: Windows는 이 방법으로만 대기 목록 비우기를 허용하므로 앱에 관리자 권한이 필요합니다.",
        "secLang": "언어 / Language",
        "langAuto": "자동 (Windows)",
        "langSaved": "언어를 저장했습니다. 다음에 앱을 시작할 때 적용됩니다.",
        "alreadyRunning": "이미 실행 중입니다 (트레이를 확인하세요 ❄).",
        "niceDwm": "dwm (데스크톱 창)",
    },
}

# Namen in der eigenen Sprache, Reihenfolge wie auf der Startseite
LANG_NAMES = [("de", "Deutsch"), ("en", "English"), ("es", "Español"), ("fr", "Français"), ("it", "Italiano"), ("nl", "Nederlands"), ("pl", "Polski"), ("pt", "Português"), ("tr", "Türkçe"), ("ru", "Русский"), ("hi", "हिन्दी"), ("zh", "中文"), ("ja", "日本語"), ("ko", "한국어")]
# Windows-Anzeigesprache (primäre LANGID) → Sprachcode
LANGIDS = {0x07: "de", 0x09: "en", 0x0A: "es", 0x0C: "fr", 0x10: "it", 0x13: "nl", 0x15: "pl",
           0x16: "pt", 0x1F: "tr", 0x19: "ru", 0x39: "hi", 0x04: "zh", 0x11: "ja", 0x12: "ko"}

def detect_lang():
    pref = CFG.get("language", "auto")
    if pref in L:
        return pref
    try:  # primäre Sprach-ID der Windows-Anzeigesprache, unbekannte → Englisch
        langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return LANGIDS.get(langid & 0x3FF, "en")
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
    "memory compression": "Memory Compression",  # Win 11 meldet den Namen mit Leerzeichen
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

# Tausender- und Dezimaltrenner je Sprache (ohne locale-Abhängigkeit)
THOUSANDS = {"en": ",", "hi": ",", "zh": ",", "ja": ",", "ko": ",", "fr": "\u202f", "ru": "\u00a0", "pl": "\u00a0"}
DECIMAL_POINT = {"en", "hi", "zh", "ja", "ko"}

def fmt_mb(b):
    """Bytes → 'X.XXX MB' (Tausendertrennung je nach Sprache)."""
    s = f"{b / (1024 * 1024):,.0f}"
    return s.replace(",", THOUSANDS.get(LANG, ".")) + " MB"

def fmt_gb(b):
    s = f"{b / (1024 ** 3):.1f}"
    if LANG not in DECIMAL_POINT:
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
        self.root.geometry("610x770")
        self.root.minsize(540, 700)
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

        # Textzeilen wachsen mit der Fensterbreite mit — nichts wird
        # mehr rechts abgeschnitten, egal wie schmal/breit gezogen wird.
        self.root.bind("<Configure>", self._on_root_resize)

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
            # feste Breite, aber Umbruch statt Abschneiden (Schriftzeichen sind doppelt so breit)
            lbl = tk.Label(row, text="", font=FONT_SMALL, bg=C_BG,
                           fg=C_MUTED, width=34, anchor="w", justify="left")
            lbl.configure(wraplength=tkfont.Font(font=FONT_SMALL).measure("0") * 34)
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
        # 15 Möglichkeiten passen nicht mehr als Knöpfe nebeneinander: eine Auswahlliste
        choices = [("auto", t("langAuto"))] + LANG_NAMES
        label_of = dict(choices)
        current = CFG.get("language", "auto")
        lang_var = tk.StringVar(value=label_of.get(current, label_of["auto"]))

        def on_lang_change(label):
            code = next(c for c, n in choices if n == label)
            if code == CFG.get("language", "auto"):
                return
            CFG["language"] = code
            save_cfg(CFG)
            messagebox.showinfo(APP_NAME, t("langSaved"))
            w.lift()

        lang_menu = tk.OptionMenu(w, lang_var, *[n for _, n in choices], command=on_lang_change)
        lang_menu.configure(font=FONT, bg=C_PANEL, fg=C_TEXT, activebackground=C_PANEL,
                            activeforeground=C_ACCENT, highlightthickness=0, relief="flat", anchor="w")
        lang_menu["menu"].configure(font=FONT, bg=C_PANEL, fg=C_TEXT, activebackground=C_ACCENT,
                                    activeforeground=C_BG)
        lang_menu.pack(anchor="w", **pad)

        tk.Label(w, text=t("adminHint"),
                 font=FONT_SMALL, bg=C_BG, fg=C_MUTED, wraplength=420,
                 justify="left").pack(anchor="w", pady=(16, 0), **pad)

        tk.Label(w, text="© 2026 Dennis_mit_2n",
                 font=FONT_SMALL, bg=C_BG, fg=C_MUTED
                 ).pack(anchor="w", pady=(10, 4), **pad)

        # Längere Sprachen brechen öfter um: das Fenster wächst mit, statt unten abzuschneiden
        w.update_idletasks()
        w.geometry(f"500x{max(560, w.winfo_reqheight())}")

    def _on_root_resize(self, e):
        # Bindings am Toplevel feuern auch für Kinder (bindtags) —
        # nur auf das Fenster selbst reagieren.
        if e.widget is not self.root:
            return
        wide = max(300, e.width - 40)    # Banner + Fußnote (padx 16 je Seite)
        self.banner.configure(wraplength=wide)
        self.lbl_cookbook.configure(wraplength=wide)
        self.lbl_legend.configure(wraplength=max(300, e.width - 60),
                                  justify="left")

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
