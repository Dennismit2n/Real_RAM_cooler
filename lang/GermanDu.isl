; ******************************************************
; ***                                                ***
; *** Inno Setup version 6.5.0+ German messages      ***
; ***                                                ***
; *** Changes 6.0.0+ Author:                         ***
; ***                                                ***
; ***   Jens Brand (jens.brand@wolf-software.de)     ***
; ***                                                ***
; *** Original Authors:                              ***
; ***                                                ***
; ***   Peter Stadler (Peter.Stadler@univie.ac.at)   ***
; ***   Michael Reitz (innosetup@assimilate.de)      ***
; ***                                                ***
; *** Contributors:                                  ***
; ***                                                ***
; ***   Roland Ruder (info@rr4u.de)                  ***
; ***   Hans Sperber (Hans.Sperber@de.bosch.com)     ***
; ***   LaughingMan (puma.d@web.de)                  ***
; ***                                                ***
; ******************************************************
;
; Diese Übersetzung hält sich an die neue deutsche Rechtschreibung.
; Du-Form: angepasst für die Setups von Real_RAM_cooler und Fadenkreuz
; (github.com/Dennismit2n), November 2026. Grundlage ist German.isl aus Inno Setup 6.7.3
; mit den Autoren oben, umgeschrieben wurden nur die Stellen mit Sie, Ihr und Ihnen,
; dazu deutsche Anführungszeichen „…“ statt "…" und zwei Kommas statt Semikolon.

; To download user-contributed translations of this file, go to:
; https://jrsoftware.org/files/istrans/

; Note: When translating this text, do not add periods (.) to the end of
; messages that didn't have them already, because on those messages Inno
; Setup adds the periods automatically (appending a period would result in
; two periods being displayed).

[LangOptions]
; The following three entries are very important. Be sure to read and 
; understand the '[LangOptions] section' topic in the help file.
LanguageName=Deutsch
LanguageID=$0407
LanguageCodePage=1252
; If the language you are translating to requires special font faces or
; sizes, uncomment any of the following entries and change them accordingly.
;DialogFontName=
;DialogFontSize=9
;DialogFontBaseScaleWidth=7
;DialogFontBaseScaleHeight=15
;WelcomeFontName=Segoe UI
;WelcomeFontSize=14

[Messages]

; *** Application titles
SetupAppTitle=Setup
SetupWindowTitle=Setup - %1
UninstallAppTitle=Entfernen
UninstallAppFullTitle=%1 entfernen

; *** Misc. common
InformationTitle=Information
ConfirmTitle=Bestätigen
ErrorTitle=Fehler

; *** SetupLdr messages
SetupLdrStartupMessage=%1 wird jetzt installiert. Möchtest du fortfahren?
LdrCannotCreateTemp=Es konnte keine temporäre Datei erstellt werden. Das Setup wurde abgebrochen
LdrCannotExecTemp=Die Datei konnte nicht im temporären Ordner ausgeführt werden. Das Setup wurde abgebrochen
HelpTextNote=

; *** Startup error messages
LastErrorMessage=%1.%n%nFehler %2: %3
SetupFileMissing=Die Datei %1 fehlt im Installationsordner. Bitte behebe das Problem oder besorge dir eine neue Kopie des Programms.
SetupFileCorrupt=Die Setup-Dateien sind beschädigt. Besorge dir bitte eine neue Kopie des Programms.
SetupFileCorruptOrWrongVer=Die Setup-Dateien sind beschädigt oder inkompatibel zu dieser Version des Setups. Bitte behebe das Problem oder besorge dir eine neue Kopie des Programms.
InvalidParameter=Ein ungültiger Parameter wurde auf der Kommandozeile übergeben:%n%n%1
SetupAlreadyRunning=Setup läuft bereits.
WindowsVersionNotSupported=Dieses Programm unterstützt die auf deinem Computer installierte Windows-Version nicht.
WindowsServicePackRequired=Dieses Programm benötigt %1 Service Pack %2 oder höher.
NotOnThisPlatform=Dieses Programm kann nicht unter %1 ausgeführt werden.
OnlyOnThisPlatform=Dieses Programm muss unter %1 ausgeführt werden.
OnlyOnTheseArchitectures=Dieses Programm kann nur auf Windows-Versionen installiert werden, die folgende Prozessor-Architekturen unterstützen:%n%n%1
WinVersionTooLowError=Dieses Programm benötigt %1 Version %2 oder höher.
WinVersionTooHighError=Dieses Programm kann nicht unter %1 Version %2 oder höher installiert werden.
AdminPrivilegesRequired=Du musst als Administrator angemeldet sein, um dieses Programm installieren zu können.
PowerUserPrivilegesRequired=Du musst als Administrator oder als Mitglied der Hauptbenutzer-Gruppe angemeldet sein, um dieses Programm installieren zu können.
SetupAppRunningError=Das Setup hat entdeckt, dass %1 zurzeit ausgeführt wird.%n%nBitte schließe jetzt alle laufenden Instanzen und klicke auf „OK“, um fortzufahren, oder auf „Abbrechen“, um zu beenden.
UninstallAppRunningError=Die Deinstallation hat entdeckt, dass %1 zurzeit ausgeführt wird.%n%nBitte schließe jetzt alle laufenden Instanzen und klicke auf „OK“, um fortzufahren, oder auf „Abbrechen“, um zu beenden.

; *** Startup questions
PrivilegesRequiredOverrideTitle=Installationsmodus auswählen
PrivilegesRequiredOverrideInstruction=Bitte wähle den Installationsmodus
PrivilegesRequiredOverrideText1=%1 kann für alle Benutzer (erfordert Administrationsrechte) oder nur für dich installiert werden.
PrivilegesRequiredOverrideText2=%1 kann nur für dich oder für alle Benutzer (erfordert Administrationsrechte) installiert werden.
PrivilegesRequiredOverrideAllUsers=Installation für &alle Benutzer
PrivilegesRequiredOverrideAllUsersRecommended=Installation für &alle Benutzer (empfohlen)
PrivilegesRequiredOverrideCurrentUser=Installation nur für &dich
PrivilegesRequiredOverrideCurrentUserRecommended=Installation nur für &dich (empfohlen)

; *** Misc. errors
ErrorCreatingDir=Das Setup konnte den Ordner „%1“ nicht erstellen.
ErrorTooManyFilesInDir=Das Setup konnte eine Datei im Ordner „%1“ nicht erstellen, weil er zu viele Dateien enthält.

; *** Setup common messages
ExitSetupTitle=Setup verlassen
ExitSetupMessage=Das Setup ist noch nicht abgeschlossen. Wenn du jetzt beendest, wird das Programm nicht installiert.%n%nDu kannst das Setup zu einem späteren Zeitpunkt nochmals ausführen, um die Installation zu vervollständigen.%n%nSetup verlassen?
AboutSetupMenuItem=&Über das Setup ...
AboutSetupTitle=Über das Setup
AboutSetupMessage=%1 Version %2%n%3%n%n%1 Webseite:%n%4
AboutSetupNote=
TranslatorNote=German translation maintained by Jens Brand (jens.brand@wolf-software.de)

; *** Buttons
ButtonBack=< &Zurück
ButtonNext=&Weiter >
ButtonInstall=&Installieren
ButtonOK=OK
ButtonCancel=Abbrechen
ButtonYes=&Ja
ButtonYesToAll=J&a für Alle
ButtonNo=&Nein
ButtonNoToAll=N&ein für Alle
ButtonFinish=&Fertigstellen
ButtonBrowse=&Durchsuchen ...
ButtonWizardBrowse=Du&rchsuchen ...
ButtonNewFolder=&Neuen Ordner erstellen

; *** "Select Language" dialog messages
SelectLanguageTitle=Setup-Sprache auswählen
SelectLanguageLabel=Wähle die Sprache aus, die während der Installation benutzt werden soll:

; *** Common wizard text
ClickNext=„Weiter“ zum Fortfahren, „Abbrechen“ zum Verlassen.
BeveledLabel=
BrowseDialogTitle=Ordner suchen
BrowseDialogLabel=Wähle einen Ordner aus und klicke danach auf „OK“.
NewFolderName=Neuer Ordner

; *** "Welcome" wizard page
WelcomeLabel1=Willkommen zum [name] Setup-Assistenten
WelcomeLabel2=Dieser Assistent wird jetzt [name/ver] auf deinem Computer installieren.%n%nDu solltest alle anderen Anwendungen beenden, bevor du mit dem Setup fortfährst.

; *** "Password" wizard page
WizardPassword=Passwort
PasswordLabel1=Diese Installation wird durch ein Passwort geschützt.
PasswordLabel3=Bitte gib das Passwort ein und klicke danach auf „Weiter“. Achte auf korrekte Groß-/Kleinschreibung.
PasswordEditLabel=&Passwort:
IncorrectPassword=Das eingegebene Passwort ist nicht korrekt. Bitte versuche es noch einmal.

; *** "License Agreement" wizard page
WizardLicense=Lizenzvereinbarung
LicenseLabel=Lies bitte folgende wichtige Informationen, bevor du fortfährst.
LicenseLabel3=Lies bitte die folgenden Lizenzvereinbarungen. Benutze bei Bedarf die Bildlaufleiste oder drücke die „Bild Ab“-Taste.
LicenseAccepted=Ich &akzeptiere die Vereinbarung
LicenseNotAccepted=Ich &lehne die Vereinbarung ab

; *** "Information" wizard pages
WizardInfoBefore=Information
InfoBeforeLabel=Lies bitte folgende wichtige Informationen, bevor du fortfährst.
InfoBeforeClickLabel=Klicke auf „Weiter“, sobald du bereit bist, mit dem Setup fortzufahren.
WizardInfoAfter=Information
InfoAfterLabel=Lies bitte folgende wichtige Informationen, bevor du fortfährst.
InfoAfterClickLabel=Klicke auf „Weiter“, sobald du bereit bist, mit dem Setup fortzufahren.

; *** "User Information" wizard page
WizardUserInfo=Benutzerinformationen
UserInfoDesc=Bitte trage deine Daten ein.
UserInfoName=&Name:
UserInfoOrg=&Organisation:
UserInfoSerial=&Seriennummer:
UserInfoNameRequired=Du musst einen Namen eintragen.

; *** "Select Destination Location" wizard page
WizardSelectDir=Ziel-Ordner wählen
SelectDirDesc=Wohin soll [name] installiert werden?
SelectDirLabel3=Das Setup wird [name] in den folgenden Ordner installieren.
SelectDirBrowseLabel=Klicke auf „Weiter“, um fortzufahren. Klicke auf „Durchsuchen“, falls du einen anderen Ordner auswählen möchtest.
DiskSpaceGBLabel=Mindestens [gb] GB freier Speicherplatz ist erforderlich.
DiskSpaceMBLabel=Mindestens [mb] MB freier Speicherplatz ist erforderlich.
CannotInstallToNetworkDrive=Das Setup kann nicht in einen Netzwerk-Pfad installieren.
CannotInstallToUNCPath=Das Setup kann nicht in einen UNC-Pfad installieren. Wenn du auf ein Netzlaufwerk installieren möchtest, musst du dem Netzwerkpfad einen Laufwerksbuchstaben zuordnen.
InvalidPath=Du musst einen vollständigen Pfad mit einem Laufwerksbuchstaben angeben, z. B.:%n%nC:\Beispiel%n%noder einen UNC-Pfad in der Form:%n%n\\Server\Freigabe
InvalidDrive=Das angegebene Laufwerk bzw. der UNC-Pfad existiert nicht oder es kann nicht darauf zugegriffen werden. Wähle bitte einen anderen Ordner.
DiskSpaceWarningTitle=Nicht genug freier Speicherplatz
DiskSpaceWarning=Das Setup benötigt mindestens %1 KB freien Speicherplatz zum Installieren, aber auf dem ausgewählten Laufwerk sind nur %2 KB verfügbar.%n%nMöchtest du trotzdem fortfahren?
DirNameTooLong=Der Ordnername/Pfad ist zu lang.
InvalidDirName=Der Ordnername ist nicht gültig.
BadDirName32=Ordnernamen dürfen keine der folgenden Zeichen enthalten:%n%n%1
DirExistsTitle=Ordner existiert bereits
DirExists=Der Ordner:%n%n%1%n%n existiert bereits. Möchtest du trotzdem in diesen Ordner installieren?
DirDoesntExistTitle=Ordner ist nicht vorhanden
DirDoesntExist=Der Ordner:%n%n%1%n%nist nicht vorhanden. Soll der Ordner erstellt werden?

; *** "Select Components" wizard page
WizardSelectComponents=Komponenten auswählen
SelectComponentsDesc=Welche Komponenten sollen installiert werden?
SelectComponentsLabel2=Wähle die Komponenten aus, die du installieren möchtest. Klicke auf „Weiter“, wenn du bereit bist, fortzufahren.
FullInstallation=Vollständige Installation
; if possible don't translate 'Compact' as 'Minimal' (I mean 'Minimal' in your language)
CompactInstallation=Kompakte Installation
CustomInstallation=Benutzerdefinierte Installation
NoUninstallWarningTitle=Komponenten vorhanden
NoUninstallWarning=Das Setup hat festgestellt, dass die folgenden Komponenten bereits auf deinem Computer installiert sind:%n%n%1%n%nDiese nicht mehr ausgewählten Komponenten werden nicht vom Computer entfernt.%n%nMöchtest du trotzdem fortfahren?
ComponentSize1=%1 KB
ComponentSize2=%1 MB
ComponentsDiskSpaceGBLabel=Die aktuelle Auswahl erfordert mindestens [gb] GB Speicherplatz.
ComponentsDiskSpaceMBLabel=Die aktuelle Auswahl erfordert mindestens [mb] MB Speicherplatz.

; *** "Select Additional Tasks" wizard page
WizardSelectTasks=Zusätzliche Aufgaben auswählen
SelectTasksDesc=Welche zusätzlichen Aufgaben sollen ausgeführt werden?
SelectTasksLabel2=Wähle die zusätzlichen Aufgaben aus, die das Setup während der Installation von [name] ausführen soll, und klicke danach auf „Weiter“.

; *** "Select Start Menu Folder" wizard page
WizardSelectProgramGroup=Startmenü-Ordner auswählen
SelectStartMenuFolderDesc=Wo soll das Setup die Programm-Verknüpfungen erstellen?
SelectStartMenuFolderLabel3=Das Setup wird die Programm-Verknüpfungen im folgenden Startmenü-Ordner erstellen.
SelectStartMenuFolderBrowseLabel=Klicke auf „Weiter“, um fortzufahren. Klicke auf „Durchsuchen“, falls du einen anderen Ordner auswählen möchtest.
MustEnterGroupName=Du musst einen Ordnernamen eingeben.
GroupNameTooLong=Der Ordnername/Pfad ist zu lang.
InvalidGroupName=Der Ordnername ist nicht gültig.
BadGroupName=Der Ordnername darf keine der folgenden Zeichen enthalten:%n%n%1
NoProgramGroupCheck2=&Keinen Ordner im Startmenü erstellen

; *** "Ready to Install" wizard page
WizardReady=Bereit zur Installation.
ReadyLabel1=Das Setup ist jetzt bereit, [name] auf deinem Computer zu installieren.
ReadyLabel2a=Klicke auf „Installieren“, um mit der Installation zu beginnen, oder auf „Zurück“, um deine Einstellungen zu überprüfen oder zu ändern.
ReadyLabel2b=Klicke auf „Installieren“, um mit der Installation zu beginnen.
ReadyMemoUserInfo=Benutzerinformationen:
ReadyMemoDir=Ziel-Ordner:
ReadyMemoType=Setup-Typ:
ReadyMemoComponents=Ausgewählte Komponenten:
ReadyMemoGroup=Startmenü-Ordner:
ReadyMemoTasks=Zusätzliche Aufgaben:

; *** TDownloadWizardPage wizard page and DownloadTemporaryFile
DownloadingLabel2=Lade Dateien herunter...
ButtonStopDownload=Download &abbrechen
StopDownload=Bist du sicher, dass du den Download abbrechen willst?
ErrorDownloadAborted=Download abgebrochen
ErrorDownloadFailed=Download fehlgeschlagen: %1 %2
ErrorDownloadSizeFailed=Fehler beim Ermitteln der Größe: %1 %2
ErrorProgress=Ungültiger Fortschritt: %1 von %2
ErrorFileSize=Ungültige Dateigröße: erwartet %1, gefunden %2

; *** TExtractionWizardPage wizard page and Extract7ZipArchive
ExtractingLabel=Entpacke Dateien...
ButtonStopExtraction=Entpacken &abbrechen
StopExtraction=Bist du sicher, dass du das Entpacken abbrechen willst?
ErrorExtractionAborted=Entpacken abgebrochen
ErrorExtractionFailed=Entpacken fehlgeschlagen: %1

; *** Archive extraction failure details
ArchiveIncorrectPassword=Ungültiges Passwort
ArchiveIsCorrupted=Das Archiv ist defekt
ArchiveUnsupportedFormat=Das Archivformat wird nicht unterstützt

; *** "Preparing to Install" wizard page
WizardPreparing=Vorbereitung der Installation
PreparingDesc=Das Setup bereitet die Installation von [name] auf diesem Computer vor.
PreviousInstallNotCompleted=Eine vorherige Installation/Deinstallation eines Programms wurde nicht abgeschlossen. Der Computer muss neu gestartet werden, um die Installation/Deinstallation zu beenden.%n%nStarte das Setup nach dem Neustart deines Computers erneut, um die Installation von [name] durchzuführen.
CannotContinue=Das Setup kann nicht fortfahren. Bitte klicke auf „Abbrechen“ zum Verlassen.
ApplicationsFound=Die folgenden Anwendungen benutzen Dateien, die aktualisiert werden müssen. Es wird empfohlen, Setup zu erlauben, diese Anwendungen zu schließen.
ApplicationsFound2=Die folgenden Anwendungen benutzen Dateien, die aktualisiert werden müssen. Es wird empfohlen, Setup zu erlauben, diese Anwendungen zu schließen. Nachdem die Installation fertiggestellt wurde, versucht Setup, diese Anwendungen wieder zu starten.
CloseApplications=&Schließe die Anwendungen automatisch
DontCloseApplications=Schließe die A&nwendungen nicht
ErrorCloseApplications=Das Setup konnte nicht alle Anwendungen automatisch schließen. Es wird empfohlen, alle Anwendungen zu schließen, die Dateien benutzen, die vom Setup vor einer Fortsetzung aktualisiert werden müssen.  
PrepareToInstallNeedsRestart=Das Setup muss deinen Computer neu starten. Führe nach dem Neustart das Setup erneut aus, um die Installation von [name] abzuschließen.%n%nWillst du jetzt neu starten?

; *** "Installing" wizard page
WizardInstalling=Installiere ...
InstallingLabel=Warte bitte, während [name] auf deinem Computer installiert wird.

; *** "Setup Completed" wizard page
FinishedHeadingLabel=Beenden des [name] Setup-Assistenten
FinishedLabelNoIcons=Das Setup hat die Installation von [name] auf deinem Computer abgeschlossen.
FinishedLabel=Das Setup hat die Installation von [name] auf deinem Computer abgeschlossen. Die Anwendung kann über die installierten Programm-Verknüpfungen gestartet werden.
ClickFinish=Klicke auf „Fertigstellen“, um das Setup zu beenden.
FinishedRestartLabel=Um die Installation von [name] abzuschließen, muss das Setup deinen Computer neu starten. Möchtest du jetzt neu starten?
FinishedRestartMessage=Um die Installation von [name] abzuschließen, muss das Setup deinen Computer neu starten.%n%nMöchtest du jetzt neu starten?
ShowReadmeCheck=Ja, ich möchte die LIESMICH-Datei sehen
YesRadio=&Ja, Computer jetzt neu starten
NoRadio=&Nein, ich werde den Computer später neu starten
; used for example as 'Run MyProg.exe'
RunEntryExec=%1 starten
; used for example as 'View Readme.txt'
RunEntryShellExec=%1 anzeigen

; *** "Setup Needs the Next Disk" stuff
ChangeDiskTitle=Nächsten Datenträger einlegen
SelectDiskLabel2=Lege bitte Datenträger %1 ein und klicke auf „OK“.%n%nWenn sich die Dateien von diesem Datenträger in einem anderen als dem angezeigten Ordner befinden, dann gib bitte den korrekten Pfad ein oder klicke auf „Durchsuchen“.
PathLabel=&Pfad:
FileNotInDir2=Die Datei „%1“ befindet sich nicht in „%2“. Bitte Ordner ändern oder richtigen Datenträger einlegen.
SelectDirectoryLabel=Gib bitte an, wo der nächste Datenträger eingelegt wird.

; *** Installation phase messages
SetupAborted=Das Setup konnte nicht abgeschlossen werden.%n%nBehebe bitte das Problem und starte das Setup erneut.
AbortRetryIgnoreSelectAction=Bitte auswählen
AbortRetryIgnoreRetry=&Nochmals versuchen
AbortRetryIgnoreIgnore=&Den Fehler ignorieren und fortfahren
AbortRetryIgnoreCancel=Installation abbrechen
RetryCancelSelectAction=Bitte auswählen
RetryCancelRetry=&Wiederholen
RetryCancelCancel=&Abbrechen

; *** Installation status messages
StatusClosingApplications=Anwendungen werden geschlossen ...
StatusCreateDirs=Ordner werden erstellt ...
StatusExtractFiles=Dateien werden entpackt ...
StatusDownloadFiles=Dateien werden herunter geladen...
StatusCreateIcons=Verknüpfungen werden erstellt ...
StatusCreateIniEntries=INI-Einträge werden erstellt ...
StatusCreateRegistryEntries=Registry-Einträge werden erstellt ...
StatusRegisterFiles=Dateien werden registriert ...
StatusSavingUninstall=Deinstallationsinformationen werden gespeichert ...
StatusRunProgram=Installation wird beendet ...
StatusRestartingApplications=Neustart der Anwendungen ...
StatusRollback=Änderungen werden rückgängig gemacht ...

; *** Misc. errors
ErrorInternal2=Interner Fehler: %1
ErrorFunctionFailedNoCode=%1 schlug fehl
ErrorFunctionFailed=%1 schlug fehl, Code %2
ErrorFunctionFailedWithMessage=%1 schlug fehl, Code %2.%n%3
ErrorExecutingProgram=Datei kann nicht ausgeführt werden:%n%1

; *** Registry errors
ErrorRegOpenKey=Registry-Schlüssel konnte nicht geöffnet werden:%n%1\%2
ErrorRegCreateKey=Registry-Schlüssel konnte nicht erstellt werden:%n%1\%2
ErrorRegWriteKey=Fehler beim Schreiben des Registry-Schlüssels:%n%1\%2

; *** INI errors
ErrorIniEntry=Fehler beim Erstellen eines INI-Eintrages in der Datei „%1“.

; *** File copying errors
FileAbortRetryIgnoreSkipNotRecommended=Diese Datei &überspringen (nicht empfohlen)
FileAbortRetryIgnoreIgnoreNotRecommended=Den Fehler &ignorieren und fortfahren (nicht empfohlen)
SourceIsCorrupted=Die Quelldatei ist beschädigt
SourceDoesntExist=Die Quelldatei „%1“ existiert nicht
SourceVerificationFailed=Überprüfung der Quelldatei fehlgeschlagen: %1
VerificationSignatureDoesntExist=Die Signaturdatei „%1“ existiert nicht
VerificationSignatureInvalid=Die Signaturdatei „%1“ ist ungültig
VerificationKeyNotFound=Die Signaturdatei „%1“ verwendet einen unbekannten Schlüssel
VerificationFileNameIncorrect=Der Name der Datei ist ungültig
VerificationFileTagIncorrect=Der Tag der Datei ist ungültig
VerificationFileSizeIncorrect=Die Größe der Datei ist ungültig
VerificationFileHashIncorrect=Der Hashwert der Datei ist ungültig
ExistingFileReadOnly2=Die vorhandene Datei kann nicht ersetzt werden, da sie schreibgeschützt ist.
ExistingFileReadOnlyRetry=&Den Schreibschutz entfernen und noch einmal versuchen
ExistingFileReadOnlyKeepExisting=Die &vorhandene Datei behalten
ErrorReadingExistingDest=Lesefehler in Datei:
FileExistsSelectAction=Aktion auswählen
FileExists2=Die Datei ist bereits vorhanden.
FileExistsOverwriteExisting=Vorhandene Datei &überschreiben
FileExistsKeepExisting=Vorhandene Datei &behalten
FileExistsOverwriteOrKeepAll=&Dies auch für die nächsten Konflikte ausführen
ExistingFileNewerSelectAction=Aktion auswählen
ExistingFileNewer2=Die vorhandene Datei ist neuer als die Datei, die installiert werden soll.
ExistingFileNewerOverwriteExisting=Vorhandene Datei &überschreiben
ExistingFileNewerKeepExisting=Vorhandene Datei &behalten (empfohlen)
ExistingFileNewerOverwriteOrKeepAll=&Dies auch für die nächsten Konflikte ausführen
ErrorChangingAttr=Fehler beim Ändern der Datei-Attribute:
ErrorCreatingTemp=Fehler beim Erstellen einer Datei im Ziel-Ordner:
ErrorReadingSource=Fehler beim Lesen der Quelldatei:
ErrorCopying=Fehler beim Kopieren einer Datei:
ErrorDownloading=Beim Download der Datei ist ein Fehler aufgetreten:
ErrorExtracting=Beim Entpacken eines Archivs ist ein Fehler aufgetreten:
ErrorReplacingExistingFile=Fehler beim Ersetzen einer vorhandenen Datei:
ErrorRestartReplace=„Ersetzen nach Neustart“ fehlgeschlagen:
ErrorRenamingTemp=Fehler beim Umbenennen einer Datei im Ziel-Ordner:
ErrorRegisterServer=DLL/OCX konnte nicht registriert werden: %1
ErrorRegSvr32Failed=RegSvr32-Aufruf scheiterte mit Exit-Code %1
ErrorRegisterTypeLib=Typen-Bibliothek konnte nicht registriert werden: %1

; *** Uninstall display name markings
; used for example as 'Mein Programm (32 Bit)'
UninstallDisplayNameMark=%1 (%2)
; used for example as 'Mein Programm (32 Bit, Alle Benutzer)'
UninstallDisplayNameMarks=%1 (%2, %3)
UninstallDisplayNameMark32Bit=32 Bit
UninstallDisplayNameMark64Bit=64 Bit
UninstallDisplayNameMarkAllUsers=Alle Benutzer
UninstallDisplayNameMarkCurrentUser=Aktueller Benutzer

; *** Post-installation errors
ErrorOpeningReadme=Fehler beim Öffnen der LIESMICH-Datei.
ErrorRestartingComputer=Das Setup konnte den Computer nicht neu starten. Bitte führe den Neustart manuell durch.

; *** Uninstaller messages
UninstallNotFound=Die Datei „%1“ existiert nicht. Entfernen der Anwendung fehlgeschlagen.
UninstallOpenError=Die Datei „%1“ konnte nicht geöffnet werden. Entfernen der Anwendung fehlgeschlagen.
UninstallUnsupportedVer=Das Format der Deinstallationsdatei „%1“ konnte nicht erkannt werden. Entfernen der Anwendung fehlgeschlagen.
UninstallUnknownEntry=In der Deinstallationsdatei wurde ein unbekannter Eintrag (%1) gefunden.
ConfirmUninstall=Bist du sicher, dass du %1 und alle zugehörigen Komponenten entfernen möchtest?
UninstallOnlyOnWin64=Diese Installation kann nur unter 64-Bit-Windows-Versionen entfernt werden.
OnlyAdminCanUninstall=Diese Installation kann nur von einem Benutzer mit Administrator-Rechten entfernt werden.
UninstallStatusLabel=Warte bitte, während %1 von deinem Computer entfernt wird.
UninstalledAll=%1 wurde erfolgreich von deinem Computer entfernt.
UninstalledMost=Entfernen von %1 beendet.%n%nEinige Komponenten konnten nicht entfernt werden. Diese kannst du manuell löschen.
UninstalledAndNeedsRestart=Um die Deinstallation von %1 abzuschließen, muss dein Computer neu gestartet werden.%n%nMöchtest du jetzt neu starten?
UninstallDataCorrupted=„%1“-Datei ist beschädigt. Entfernen der Anwendung fehlgeschlagen.

; *** Uninstallation phase messages
ConfirmDeleteSharedFileTitle=Gemeinsame Datei entfernen?
ConfirmDeleteSharedFile2=Das System zeigt an, dass die folgende gemeinsame Datei von keinem anderen Programm mehr benutzt wird. Möchtest du diese Datei entfernen lassen?%nSollte es doch noch Programme geben, die diese Datei benutzen und sie wird entfernt, funktionieren diese Programme vielleicht nicht mehr richtig. Wenn du unsicher bist, wähle „Nein“, um die Datei im System zu belassen. Es schadet deinem System nicht, wenn du die Datei behältst.
SharedFileNameLabel=Dateiname:
SharedFileLocationLabel=Ordner:
WizardUninstalling=Entfernen (Status)
StatusUninstalling=Entferne %1 ...

; *** Shutdown block reasons
ShutdownBlockReasonInstallingApp=Installation von %1.
ShutdownBlockReasonUninstallingApp=Deinstallation von %1.

; The custom messages below aren't used by Setup itself, but if you make
; use of them in your scripts, you'll want to translate them.

[CustomMessages]

NameAndVersion=%1 Version %2
AdditionalIcons=Zusätzliche Symbole:
CreateDesktopIcon=&Desktop-Symbol erstellen
CreateQuickLaunchIcon=Symbol in der Schnellstartleiste erstellen
ProgramOnTheWeb=%1 im Internet
UninstallProgram=%1 entfernen
LaunchProgram=%1 starten
AssocFileExtension=&Registriere %1 mit der %2-Dateierweiterung
AssocingFileExtension=%1 wird mit der %2-Dateierweiterung registriert...
AutoStartProgramGroupDescription=Beginn des Setups:
AutoStartProgram=Starte automatisch %1
AddonHostProgramNotFound=%1 konnte im ausgewählten Ordner nicht gefunden werden.%n%nMöchtest du dennoch fortfahren?

