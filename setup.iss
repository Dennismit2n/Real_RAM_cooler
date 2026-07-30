; ═══════════════════════════════════════════════════════════════════
;  Real_RAM_cooler — Installer-Skript für Inno Setup 6  ❄
;  Kompilieren: Datei in Inno Setup öffnen → Build → Compile (Strg+F9)
;  Ergebnis:    installer\Real_RAM_cooler_Setup_v1.2.exe
; ═══════════════════════════════════════════════════════════════════

#define MyAppName "Real_RAM_cooler"
#define MyAppVersion "1.2"
#define MyAppPublisher "Dennis"
#define MyAppExeName "Real_RAM_cooler.exe"

[Setup]
; Eindeutige ID — NIE ändern, sonst erkennt Windows Updates nicht
; als dieselbe App (frisch für dich gewürfelt):
AppId={{2A6CD8B2-AAFA-4B9A-849D-D67B89B7CB83}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=Real_RAM_cooler_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Installer braucht Admin (schreibt nach Program Files) — passt zur
; App, die sowieso immer mit Admin-Rechten läuft (Entscheidung 4A):
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
; Installer folgt der Windows-Sprache (Englisch als Standard/Fallback):
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Die fertige .exe aus deinem PyInstaller-Build:
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
; "Real_RAM_cooler jetzt starten"-Häkchen am Ende des Setups:
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#MyAppName}}"; \
    Flags: nowait postinstall skipifsilent

[UninstallRun]
; Sauber gehen: die Autostart-Aufgabe mit abräumen (falls gesetzt).
Filename: "schtasks"; \
    Parameters: "/Delete /TN ""Real_RAM_cooler_Autostart"" /F"; \
    Flags: runhidden; RunOnceId: "DelAutostart"

[UninstallDelete]
; …und die config.json, damit nichts zurückbleibt:
Type: files; Name: "{app}\config.json"
