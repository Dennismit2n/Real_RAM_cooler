=====================================================================
  Real_RAM_cooler v1.1  (Eisblau Neon)
  Ein ehrliches RAM-Tool fuer Windows 10/11
=====================================================================

WAS ES MACHT
------------
* "Fuers Gaming bereinigen": leert die Windows-Standby-Liste ueber
  die native API - derselbe Mechanismus wie RAMMap und ISLC.
  Hilft real gegen Mikroruckler nach langen Gaming-Sessions.
* "Placebo-Modus": trimmt Working-Sets. Macht die Zahlen im
  Task-Manager huebsch, den PC NICHT schneller. Ist als ehrlicher
  Gag eingebaut - genau DAS verkaufen die meisten "RAM-Booster"
  als Hauptfeature. ;)
* Automatik (optional, standardmaessig AUS): leert selbststaendig,
  wenn Standby-Liste und freier RAM die Schwellwerte reissen.

INSTALLATION
------------
1. Real_RAM_cooler_Setup_v1.1.exe doppelklicken
2. Assistent durchklicken - fertig
3. Die App liegt danach im Startmenue (optional: Desktop-Icon)

WICHTIG ZU WISSEN
-----------------
* "Unbekannter Herausgeber" / blauer SmartScreen-Hinweis beim
  ersten Start? Normal - die App ist nicht code-signiert
  (Zertifikate kosten mehrere hundert Euro/Jahr). Der komplette
  Quellcode ist offen einsehbar:
  https://github.com/Dennismit2n
  Bei der Warnung: "Weitere Informationen" -> "Trotzdem ausfuehren"

* Admin-Rechte (ein UAC-Klick bei jedem Start) sind Pflicht:
  Windows erlaubt das Leeren der Standby-Liste nur so. Dieselbe
  Anforderung haben auch RAMMap und ISLC.

FUER GAMER - SCHNELLSTART
-------------------------
1. Vor dem Zocken: Rechtsklick auf die Schneeflocke im System-Tray
   -> "Fuers Gaming bereinigen". Das war's.
2. Lange Sessions / Ruckler nach 2-3 Stunden? In den Einstellungen
   (Zahnrad) die Automatik aktivieren.
   Empfohlen bei 16 GB RAM:  Standby groesser als 1024 MB
                             und frei kleiner als 1536 MB
   Bei 32 GB RAM: beide Werte verdoppeln.
3. Ehrliche Erwartung: Das Tool behebt Stutter durch vollgelaufenen
   Standby-Cache. Es zaubert keine FPS und ersetzt kein
   RAM-Upgrade.

BEDIENUNG
---------
* Linksklick auf das Tray-Icon      -> Dashboard oeffnen
* Fenster schliessen (X)            -> minimiert ins Tray
* Beenden                           -> Rechtsklick Tray -> Beenden
* Overlay (halbtransparent, ziehbar) in den Einstellungen
  aktivierbar; Deckkraft aenderbar in der config.json neben der
  .exe ("overlay_alpha": 0.28 -> Werte von 0.15 bis 1.0)

DASHBOARD VERSTEHEN
-------------------
* RAM-Balken: In Benutzung / Standby / wirklich frei
* Fresser-Liste, zwei Spalten:
  "Beruehrt" = alles was der Prozess nutzt (inkl. geteilter DLLs)
  "Besitzt"  = nur seine eigenen Seiten (die Task-Manager-Zahl)
  Beide Zahlen stimmen - sie beantworten verschiedene Fragen.

DEINSTALLATION
--------------
Systemsteuerung / Einstellungen -> Apps -> Real_RAM_cooler.
Der Deinstallierer entfernt auch die Autostart-Aufgabe und die
Konfigurationsdatei. Nichts bleibt zurueck.

LIZENZ & QUELLCODE
------------------
MIT-Lizenz - frei nutzen, lesen, verbessern.
Quellcode: https://github.com/Dennismit2n

Gebaut von Dennis (Dennismit2n) mit Claude.        (v1.1, 2026)
=====================================================================
