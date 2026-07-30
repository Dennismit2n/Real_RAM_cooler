=====================================================================
  Real_RAM_cooler v1.2  (Ice Blue Neon / Eisblau Neon)
  An honest RAM tool for Windows 10/11
  Ein ehrliches RAM-Tool fuer Windows 10/11
=====================================================================

--- ENGLISH ---------------------------------------------------------

WHAT IT DOES
------------
* "Clean up for gaming": purges the Windows standby list via the
  native API - the same mechanism as RAMMap and ISLC. Genuinely
  helps against micro-stutter after long gaming sessions.
* "Placebo mode": trims working sets. Makes the Task Manager
  numbers pretty, does NOT make your PC faster. Built in as an
  honest joke - most "RAM boosters" sell exactly THAT as their
  main feature. ;)
* Automatic (optional, OFF by default): purges on its own when
  standby list and free RAM cross the thresholds.
* Bilingual: starts in your Windows language (English/German),
  switchable in the settings.

INSTALLATION
------------
1. Double-click Real_RAM_cooler_Setup_v1.2.exe
2. Click through the wizard - done
3. The app is in the Start menu (optional: desktop icon)

GOOD TO KNOW
------------
* "Unknown publisher" / SmartScreen warning at first start?
  Normal - the app is not code-signed (certificates cost several
  hundred euros per year). The full source code is public:
  https://github.com/Dennismit2n/Real_RAM_cooler
  At the warning: "More info" -> "Run anyway"
* Admin rights (one UAC click at every start) are mandatory:
  Windows only allows purging the standby list this way. RAMMap
  and ISLC have the same requirement.

QUICK START FOR GAMERS
----------------------
1. Before playing: right-click the snowflake in the system tray
   -> "Clean up for gaming". That's it.
2. Long sessions / stutter after 2-3 hours? Enable Automatic in
   the settings (gear icon).
   Recommended for 16 GB RAM:  standby greater than 1024 MB
                               and free below 1536 MB
   For 32 GB RAM: double both values.
3. Honest expectations: fixes stutter from a bloated standby
   cache. No conjured FPS, no substitute for a RAM upgrade.

UNINSTALL
---------
Settings -> Apps -> Real_RAM_cooler. The uninstaller also removes
the autostart task and the config file. Nothing is left behind.

--- DEUTSCH ---------------------------------------------------------

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
* Zweisprachig: startet in deiner Windows-Sprache (Deutsch/
  Englisch), umschaltbar in den Einstellungen.

INSTALLATION
------------
1. Real_RAM_cooler_Setup_v1.2.exe doppelklicken
2. Assistent durchklicken - fertig
3. Die App liegt danach im Startmenue (optional: Desktop-Icon)

WICHTIG ZU WISSEN
-----------------
* "Unbekannter Herausgeber" / SmartScreen-Hinweis beim ersten
  Start? Normal - die App ist nicht code-signiert (Zertifikate
  kosten mehrere hundert Euro/Jahr). Der komplette Quellcode ist
  offen einsehbar:
  https://github.com/Dennismit2n/Real_RAM_cooler
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

DEINSTALLATION
--------------
Einstellungen -> Apps -> Real_RAM_cooler. Der Deinstallierer
entfernt auch die Autostart-Aufgabe und die Konfigurationsdatei.
Nichts bleibt zurueck.

=====================================================================
MIT license - use, read, improve. / MIT-Lizenz - nutzen, lesen,
verbessern.  Source: https://github.com/Dennismit2n/Real_RAM_cooler
Built by Dennis (Dennismit2n) with Claude.          (v1.2, 2026)
=====================================================================
