; *** Inno Setup version 6.5.0+ Hindi messages ***
;
; Machine translation made for the setups of Real_RAM_cooler and Fadenkreuz
; (github.com/Dennismit2n), November 2026. Based on Default.isl of Inno Setup 6.7.3.
; Corrections are welcome.
;
; Note: When translating this text, do not add periods (.) to the end of
; messages that didn't have them already, because on those messages Inno
; Setup adds the periods automatically (appending a period would result in
; two periods being displayed).

[LangOptions]
; The following three entries are very important. Be sure to read and
; understand the '[LangOptions] section' topic in the help file.
LanguageName=हिन्दी
LanguageID=$0439
; Hindi has no ANSI code page, this file is Unicode only
LanguageCodePage=0
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
SetupAppTitle=सेटअप
SetupWindowTitle=सेटअप - %1
UninstallAppTitle=अनइंस्टॉल
UninstallAppFullTitle=%1 अनइंस्टॉल

; *** Misc. common
InformationTitle=जानकारी
ConfirmTitle=पुष्टि करें
ErrorTitle=त्रुटि

; *** SetupLdr messages
SetupLdrStartupMessage=यह %1 को इंस्टॉल करेगा। क्या आप जारी रखना चाहते हैं?
LdrCannotCreateTemp=अस्थायी फ़ाइल नहीं बनाई जा सकी। सेटअप रोक दिया गया
LdrCannotExecTemp=अस्थायी फ़ोल्डर में फ़ाइल नहीं चलाई जा सकी। सेटअप रोक दिया गया
HelpTextNote=

; *** Startup error messages
LastErrorMessage=%1.%n%nत्रुटि %2: %3
SetupFileMissing=इंस्टॉलेशन फ़ोल्डर में फ़ाइल %1 नहीं है। कृपया समस्या ठीक करें या प्रोग्राम की नई प्रति लें।
SetupFileCorrupt=सेटअप फ़ाइलें खराब हैं। कृपया प्रोग्राम की नई प्रति लें।
SetupFileCorruptOrWrongVer=सेटअप फ़ाइलें खराब हैं या सेटअप के इस संस्करण के साथ काम नहीं करतीं। कृपया समस्या ठीक करें या प्रोग्राम की नई प्रति लें।
InvalidParameter=कमांड लाइन में एक अमान्य पैरामीटर दिया गया:%n%n%1
SetupAlreadyRunning=सेटअप पहले से चल रहा है।
WindowsVersionNotSupported=यह प्रोग्राम आपके कंप्यूटर पर चल रहे Windows संस्करण का समर्थन नहीं करता।
WindowsServicePackRequired=इस प्रोग्राम के लिए %1 सर्विस पैक %2 या उसके बाद का संस्करण चाहिए।
NotOnThisPlatform=यह प्रोग्राम %1 पर नहीं चलेगा।
OnlyOnThisPlatform=यह प्रोग्राम केवल %1 पर चलाया जा सकता है।
OnlyOnTheseArchitectures=यह प्रोग्राम केवल उन Windows संस्करणों पर इंस्टॉल हो सकता है जो इन प्रोसेसर आर्किटेक्चर के लिए बने हैं:%n%n%1
WinVersionTooLowError=इस प्रोग्राम के लिए %1 संस्करण %2 या उसके बाद का संस्करण चाहिए।
WinVersionTooHighError=यह प्रोग्राम %1 संस्करण %2 या उसके बाद के संस्करण पर इंस्टॉल नहीं किया जा सकता।
AdminPrivilegesRequired=यह प्रोग्राम इंस्टॉल करने के लिए आपको व्यवस्थापक के रूप में लॉग इन होना चाहिए।
PowerUserPrivilegesRequired=यह प्रोग्राम इंस्टॉल करने के लिए आपको व्यवस्थापक या Power Users समूह के सदस्य के रूप में लॉग इन होना चाहिए।
SetupAppRunningError=सेटअप ने पाया है कि %1 अभी चल रहा है।%n%nकृपया इसे पूरी तरह बंद करें, फिर जारी रखने के लिए “ठीक है” पर क्लिक करें, या बाहर निकलने के लिए “रद्द करें” पर।
UninstallAppRunningError=अनइंस्टॉल ने पाया है कि %1 अभी चल रहा है।%n%nकृपया इसे पूरी तरह बंद करें, फिर जारी रखने के लिए “ठीक है” पर क्लिक करें, या बाहर निकलने के लिए “रद्द करें” पर।

; *** Startup questions
PrivilegesRequiredOverrideTitle=सेटअप का इंस्टॉल मोड चुनें
PrivilegesRequiredOverrideInstruction=इंस्टॉल मोड चुनें
PrivilegesRequiredOverrideText1=%1 को सभी उपयोगकर्ताओं के लिए (व्यवस्थापक अधिकार चाहिए) या केवल आपके लिए इंस्टॉल किया जा सकता है।
PrivilegesRequiredOverrideText2=%1 को केवल आपके लिए या सभी उपयोगकर्ताओं के लिए (व्यवस्थापक अधिकार चाहिए) इंस्टॉल किया जा सकता है।
PrivilegesRequiredOverrideAllUsers=सभी उपयोगकर्ताओं के लिए इंस्टॉल करें(&A)
PrivilegesRequiredOverrideAllUsersRecommended=सभी उपयोगकर्ताओं के लिए इंस्टॉल करें(&A) (अनुशंसित)
PrivilegesRequiredOverrideCurrentUser=केवल मेरे लिए इंस्टॉल करें(&M)
PrivilegesRequiredOverrideCurrentUserRecommended=केवल मेरे लिए इंस्टॉल करें(&M) (अनुशंसित)

; *** Misc. errors
ErrorCreatingDir=सेटअप फ़ोल्डर "%1" नहीं बना सका
ErrorTooManyFilesInDir=फ़ोल्डर "%1" में फ़ाइल नहीं बनाई जा सकी, क्योंकि उसमें बहुत अधिक फ़ाइलें हैं

; *** Setup common messages
ExitSetupTitle=सेटअप से बाहर निकलें
ExitSetupMessage=सेटअप पूरा नहीं हुआ है। अगर आप अभी बाहर निकलते हैं, तो प्रोग्राम इंस्टॉल नहीं होगा।%n%nइंस्टॉलेशन पूरा करने के लिए आप सेटअप को बाद में फिर से चला सकते हैं।%n%nसेटअप से बाहर निकलें?
AboutSetupMenuItem=सेटअप के बारे में(&A)...
AboutSetupTitle=सेटअप के बारे में
AboutSetupMessage=%1 संस्करण %2%n%3%n%n%1 का होम पेज:%n%4
AboutSetupNote=
TranslatorNote=

; *** Buttons
ButtonBack=< पीछे(&B)
ButtonNext=आगे(&N) >
ButtonInstall=इंस्टॉल करें(&I)
ButtonOK=ठीक है
ButtonCancel=रद्द करें
ButtonYes=हाँ(&Y)
ButtonYesToAll=सभी के लिए हाँ(&A)
ButtonNo=नहीं(&N)
ButtonNoToAll=सभी के लिए नहीं(&O)
ButtonFinish=समाप्त(&F)
ButtonBrowse=ब्राउज़ करें(&B)...
ButtonWizardBrowse=ब्राउज़ करें(&R)...
ButtonNewFolder=नया फ़ोल्डर बनाएँ(&M)

; *** "Select Language" dialog messages
SelectLanguageTitle=सेटअप की भाषा चुनें
SelectLanguageLabel=इंस्टॉलेशन के दौरान इस्तेमाल होने वाली भाषा चुनें।

; *** Common wizard text
ClickNext=जारी रखने के लिए “आगे” पर क्लिक करें, या सेटअप से बाहर निकलने के लिए “रद्द करें” पर।
BeveledLabel=
BrowseDialogTitle=फ़ोल्डर ब्राउज़ करें
BrowseDialogLabel=नीचे दी गई सूची से एक फ़ोल्डर चुनें, फिर “ठीक है” पर क्लिक करें।
NewFolderName=नया फ़ोल्डर

; *** "Welcome" wizard page
WelcomeLabel1=[name] सेटअप विज़ार्ड में आपका स्वागत है
WelcomeLabel2=यह आपके कंप्यूटर पर [name/ver] इंस्टॉल करेगा।%n%nजारी रखने से पहले बाकी सभी ऐप्लिकेशन बंद करने की सलाह दी जाती है।

; *** "Password" wizard page
WizardPassword=पासवर्ड
PasswordLabel1=यह इंस्टॉलेशन पासवर्ड से सुरक्षित है।
PasswordLabel3=कृपया पासवर्ड दर्ज करें, फिर जारी रखने के लिए “आगे” पर क्लिक करें। पासवर्ड में छोटे और बड़े अक्षरों का अंतर मायने रखता है।
PasswordEditLabel=पासवर्ड(&P):
IncorrectPassword=आपने जो पासवर्ड दर्ज किया है, वह सही नहीं है। कृपया फिर से कोशिश करें।

; *** "License Agreement" wizard page
WizardLicense=लाइसेंस अनुबंध
LicenseLabel=जारी रखने से पहले कृपया नीचे दी गई ज़रूरी जानकारी पढ़ें।
LicenseLabel3=कृपया नीचे दिया गया लाइसेंस अनुबंध पढ़ें। इंस्टॉलेशन जारी रखने से पहले आपको इस अनुबंध की शर्तें स्वीकार करनी होंगी।
LicenseAccepted=मुझे अनुबंध स्वीकार है(&A)
LicenseNotAccepted=मुझे अनुबंध स्वीकार नहीं है(&D)

; *** "Information" wizard pages
WizardInfoBefore=जानकारी
InfoBeforeLabel=जारी रखने से पहले कृपया नीचे दी गई ज़रूरी जानकारी पढ़ें।
InfoBeforeClickLabel=जब आप सेटअप जारी रखने के लिए तैयार हों, तो “आगे” पर क्लिक करें।
WizardInfoAfter=जानकारी
InfoAfterLabel=जारी रखने से पहले कृपया नीचे दी गई ज़रूरी जानकारी पढ़ें।
InfoAfterClickLabel=जब आप सेटअप जारी रखने के लिए तैयार हों, तो “आगे” पर क्लिक करें।

; *** "User Information" wizard page
WizardUserInfo=उपयोगकर्ता की जानकारी
UserInfoDesc=कृपया अपनी जानकारी दर्ज करें।
UserInfoName=उपयोगकर्ता नाम(&U):
UserInfoOrg=संगठन(&O):
UserInfoSerial=सीरियल नंबर(&S):
UserInfoNameRequired=आपको एक नाम दर्ज करना होगा।

; *** "Select Destination Location" wizard page
WizardSelectDir=इंस्टॉल करने की जगह चुनें
SelectDirDesc=[name] को कहाँ इंस्टॉल किया जाए?
SelectDirLabel3=सेटअप [name] को नीचे दिए फ़ोल्डर में इंस्टॉल करेगा।
SelectDirBrowseLabel=जारी रखने के लिए “आगे” पर क्लिक करें। कोई दूसरा फ़ोल्डर चुनने के लिए “ब्राउज़ करें” पर क्लिक करें।
DiskSpaceGBLabel=कम से कम [gb] GB खाली डिस्क स्थान चाहिए।
DiskSpaceMBLabel=कम से कम [mb] MB खाली डिस्क स्थान चाहिए।
CannotInstallToNetworkDrive=सेटअप नेटवर्क ड्राइव पर इंस्टॉल नहीं कर सकता।
CannotInstallToUNCPath=सेटअप UNC पथ पर इंस्टॉल नहीं कर सकता।
InvalidPath=आपको ड्राइव अक्षर के साथ पूरा पथ दर्ज करना होगा, उदाहरण के लिए:%n%nC:\APP%n%nया इस रूप में UNC पथ:%n%n\\server\share
InvalidDrive=आपने जो ड्राइव या UNC शेयर चुना है, वह मौजूद नहीं है या उस तक पहुँच नहीं है। कृपया कोई दूसरा चुनें।
DiskSpaceWarningTitle=डिस्क में पर्याप्त जगह नहीं है
DiskSpaceWarning=इंस्टॉल करने के लिए सेटअप को कम से कम %1 KB खाली जगह चाहिए, लेकिन चुनी गई ड्राइव पर केवल %2 KB उपलब्ध है।%n%nक्या आप फिर भी जारी रखना चाहते हैं?
DirNameTooLong=फ़ोल्डर का नाम या पथ बहुत लंबा है।
InvalidDirName=फ़ोल्डर का नाम मान्य नहीं है।
BadDirName32=फ़ोल्डर के नाम में इनमें से कोई भी अक्षर नहीं हो सकता:%n%n%1
DirExistsTitle=फ़ोल्डर मौजूद है
DirExists=फ़ोल्डर:%n%n%1%n%nपहले से मौजूद है। क्या आप फिर भी इसी फ़ोल्डर में इंस्टॉल करना चाहते हैं?
DirDoesntExistTitle=फ़ोल्डर मौजूद नहीं है
DirDoesntExist=फ़ोल्डर:%n%n%1%n%nमौजूद नहीं है। क्या यह फ़ोल्डर बनाया जाए?

; *** "Select Components" wizard page
WizardSelectComponents=घटक चुनें
SelectComponentsDesc=कौन-से घटक इंस्टॉल किए जाएँ?
SelectComponentsLabel2=जिन घटकों को इंस्टॉल करना है, उन्हें चुनें, और बाकी का निशान हटा दें। तैयार होने पर “आगे” पर क्लिक करें।
FullInstallation=पूरा इंस्टॉलेशन
; if possible don't translate 'Compact' as 'Minimal' (I mean 'Minimal' in your language)
CompactInstallation=संक्षिप्त इंस्टॉलेशन
CustomInstallation=अपनी पसंद का इंस्टॉलेशन
NoUninstallWarningTitle=घटक मौजूद हैं
NoUninstallWarning=सेटअप ने पाया है कि ये घटक आपके कंप्यूटर पर पहले से इंस्टॉल हैं:%n%n%1%n%nइनका चुनाव हटाने से ये अनइंस्टॉल नहीं होंगे।%n%nक्या आप फिर भी जारी रखना चाहते हैं?
ComponentSize1=%1 KB
ComponentSize2=%1 MB
ComponentsDiskSpaceGBLabel=मौजूदा चुनाव के लिए कम से कम [gb] GB डिस्क स्थान चाहिए।
ComponentsDiskSpaceMBLabel=मौजूदा चुनाव के लिए कम से कम [mb] MB डिस्क स्थान चाहिए।

; *** "Select Additional Tasks" wizard page
WizardSelectTasks=अतिरिक्त कार्य चुनें
SelectTasksDesc=कौन-से अतिरिक्त कार्य किए जाएँ?
SelectTasksLabel2=[name] इंस्टॉल करते समय सेटअप जो अतिरिक्त कार्य करे, उन्हें चुनें, फिर “आगे” पर क्लिक करें।

; *** "Select Start Menu Folder" wizard page
WizardSelectProgramGroup=स्टार्ट मेनू फ़ोल्डर चुनें
SelectStartMenuFolderDesc=सेटअप प्रोग्राम के शॉर्टकट कहाँ रखे?
SelectStartMenuFolderLabel3=सेटअप प्रोग्राम के शॉर्टकट नीचे दिए स्टार्ट मेनू फ़ोल्डर में बनाएगा।
SelectStartMenuFolderBrowseLabel=जारी रखने के लिए “आगे” पर क्लिक करें। कोई दूसरा फ़ोल्डर चुनने के लिए “ब्राउज़ करें” पर क्लिक करें।
MustEnterGroupName=आपको फ़ोल्डर का नाम दर्ज करना होगा।
GroupNameTooLong=फ़ोल्डर का नाम या पथ बहुत लंबा है।
InvalidGroupName=फ़ोल्डर का नाम मान्य नहीं है।
BadGroupName=फ़ोल्डर के नाम में इनमें से कोई भी अक्षर नहीं हो सकता:%n%n%1
NoProgramGroupCheck2=स्टार्ट मेनू फ़ोल्डर न बनाएँ(&D)

; *** "Ready to Install" wizard page
WizardReady=इंस्टॉल करने के लिए तैयार
ReadyLabel1=सेटअप अब आपके कंप्यूटर पर [name] इंस्टॉल करना शुरू करने के लिए तैयार है।
ReadyLabel2a=इंस्टॉलेशन जारी रखने के लिए “इंस्टॉल करें” पर क्लिक करें, या कोई सेटिंग देखने या बदलने के लिए “पीछे” पर।
ReadyLabel2b=इंस्टॉलेशन जारी रखने के लिए “इंस्टॉल करें” पर क्लिक करें।
ReadyMemoUserInfo=उपयोगकर्ता की जानकारी:
ReadyMemoDir=इंस्टॉल करने की जगह:
ReadyMemoType=सेटअप का प्रकार:
ReadyMemoComponents=चुने गए घटक:
ReadyMemoGroup=स्टार्ट मेनू फ़ोल्डर:
ReadyMemoTasks=अतिरिक्त कार्य:

; *** TDownloadWizardPage wizard page and DownloadTemporaryFile
DownloadingLabel2=फ़ाइलें डाउनलोड हो रही हैं...
ButtonStopDownload=डाउनलोड रोकें(&S)
StopDownload=क्या आप सचमुच डाउनलोड रोकना चाहते हैं?
ErrorDownloadAborted=डाउनलोड रोक दिया गया
ErrorDownloadFailed=डाउनलोड नहीं हो सका: %1 %2
ErrorDownloadSizeFailed=आकार पता नहीं चल सका: %1 %2
ErrorProgress=अमान्य प्रगति: %2 में से %1
ErrorFileSize=अमान्य फ़ाइल आकार: अपेक्षित %1, मिला %2

; *** TExtractionWizardPage wizard page and ExtractArchive
ExtractingLabel=फ़ाइलें निकाली जा रही हैं...
ButtonStopExtraction=निकालना रोकें(&S)
StopExtraction=क्या आप सचमुच फ़ाइलें निकालना रोकना चाहते हैं?
ErrorExtractionAborted=फ़ाइलें निकालना रोक दिया गया
ErrorExtractionFailed=फ़ाइलें नहीं निकाली जा सकीं: %1

; *** Archive extraction failure details
ArchiveIncorrectPassword=पासवर्ड गलत है
ArchiveIsCorrupted=आर्काइव खराब है
ArchiveUnsupportedFormat=आर्काइव का फ़ॉर्मैट समर्थित नहीं है

; *** "Preparing to Install" wizard page
WizardPreparing=इंस्टॉल करने की तैयारी
PreparingDesc=सेटअप आपके कंप्यूटर पर [name] इंस्टॉल करने की तैयारी कर रहा है।
PreviousInstallNotCompleted=पिछले किसी प्रोग्राम को इंस्टॉल करना या हटाना पूरा नहीं हुआ था। उसे पूरा करने के लिए आपको कंप्यूटर फिर से चालू करना होगा।%n%nकंप्यूटर फिर से चालू होने के बाद [name] का इंस्टॉलेशन पूरा करने के लिए सेटअप फिर से चलाएँ।
CannotContinue=सेटअप जारी नहीं रह सकता। बाहर निकलने के लिए कृपया “रद्द करें” पर क्लिक करें।
ApplicationsFound=ये ऐप्लिकेशन ऐसी फ़ाइलों का इस्तेमाल कर रहे हैं जिन्हें सेटअप को अपडेट करना है। बेहतर है कि आप सेटअप को इन्हें अपने आप बंद करने दें।
ApplicationsFound2=ये ऐप्लिकेशन ऐसी फ़ाइलों का इस्तेमाल कर रहे हैं जिन्हें सेटअप को अपडेट करना है। बेहतर है कि आप सेटअप को इन्हें अपने आप बंद करने दें। इंस्टॉलेशन पूरा होने के बाद सेटअप इन्हें फिर से शुरू करने की कोशिश करेगा।
CloseApplications=ऐप्लिकेशन अपने आप बंद करें(&A)
DontCloseApplications=ऐप्लिकेशन बंद न करें(&D)
ErrorCloseApplications=सेटअप सभी ऐप्लिकेशन अपने आप बंद नहीं कर सका। जारी रखने से पहले उन सभी ऐप्लिकेशन को बंद कर दें जो ऐसी फ़ाइलों का इस्तेमाल कर रहे हैं जिन्हें सेटअप को अपडेट करना है।
PrepareToInstallNeedsRestart=सेटअप को आपका कंप्यूटर फिर से चालू करना होगा। कंप्यूटर फिर से चालू होने के बाद [name] का इंस्टॉलेशन पूरा करने के लिए सेटअप फिर से चलाएँ।%n%nक्या आप अभी फिर से चालू करना चाहते हैं?

; *** "Installing" wizard page
WizardInstalling=इंस्टॉल हो रहा है
InstallingLabel=कृपया प्रतीक्षा करें, सेटअप आपके कंप्यूटर पर [name] इंस्टॉल कर रहा है।

; *** "Setup Completed" wizard page
FinishedHeadingLabel=[name] सेटअप विज़ार्ड पूरा हो रहा है
FinishedLabelNoIcons=सेटअप ने आपके कंप्यूटर पर [name] इंस्टॉल कर दिया है।
FinishedLabel=सेटअप ने आपके कंप्यूटर पर [name] इंस्टॉल कर दिया है। इसे इंस्टॉल किए गए शॉर्टकट से शुरू किया जा सकता है।
ClickFinish=सेटअप से बाहर निकलने के लिए “समाप्त” पर क्लिक करें।
FinishedRestartLabel=[name] का इंस्टॉलेशन पूरा करने के लिए सेटअप को आपका कंप्यूटर फिर से चालू करना होगा। क्या आप अभी फिर से चालू करना चाहते हैं?
FinishedRestartMessage=[name] का इंस्टॉलेशन पूरा करने के लिए सेटअप को आपका कंप्यूटर फिर से चालू करना होगा।%n%nक्या आप अभी फिर से चालू करना चाहते हैं?
ShowReadmeCheck=हाँ, README फ़ाइल दिखाएँ
YesRadio=हाँ, कंप्यूटर अभी फिर से चालू करें(&Y)
NoRadio=नहीं, कंप्यूटर बाद में फिर से चालू किया जाएगा(&N)
; used for example as 'Run MyProg.exe'
RunEntryExec=%1 चलाएँ
; used for example as 'View Readme.txt'
RunEntryShellExec=%1 देखें

; *** "Setup Needs the Next Disk" stuff
ChangeDiskTitle=सेटअप को अगली डिस्क चाहिए
SelectDiskLabel2=कृपया डिस्क %1 डालें और “ठीक है” पर क्लिक करें।%n%nअगर इस डिस्क की फ़ाइलें नीचे दिखाए गए फ़ोल्डर के बजाय किसी दूसरे फ़ोल्डर में हैं, तो सही पथ दर्ज करें या “ब्राउज़ करें” पर क्लिक करें।
PathLabel=पथ(&P):
FileNotInDir2=फ़ाइल "%1" फ़ोल्डर "%2" में नहीं मिली। कृपया सही डिस्क डालें या कोई दूसरा फ़ोल्डर चुनें।
SelectDirectoryLabel=कृपया बताएँ कि अगली डिस्क कहाँ है।

; *** Installation phase messages
SetupAborted=सेटअप पूरा नहीं हुआ।%n%nकृपया समस्या ठीक करें और सेटअप फिर से चलाएँ।
AbortRetryIgnoreSelectAction=कार्रवाई चुनें
AbortRetryIgnoreRetry=फिर से कोशिश करें(&T)
AbortRetryIgnoreIgnore=त्रुटि को अनदेखा करें और जारी रखें(&I)
AbortRetryIgnoreCancel=इंस्टॉलेशन रद्द करें
RetryCancelSelectAction=कार्रवाई चुनें
RetryCancelRetry=फिर से कोशिश करें(&T)
RetryCancelCancel=रद्द करें

; *** Installation status messages
StatusClosingApplications=ऐप्लिकेशन बंद किए जा रहे हैं...
StatusCreateDirs=फ़ोल्डर बनाए जा रहे हैं...
StatusExtractFiles=फ़ाइलें निकाली जा रही हैं...
StatusDownloadFiles=फ़ाइलें डाउनलोड हो रही हैं...
StatusCreateIcons=शॉर्टकट बनाए जा रहे हैं...
StatusCreateIniEntries=INI प्रविष्टियाँ बनाई जा रही हैं...
StatusCreateRegistryEntries=रजिस्ट्री प्रविष्टियाँ बनाई जा रही हैं...
StatusRegisterFiles=फ़ाइलें रजिस्टर की जा रही हैं...
StatusSavingUninstall=अनइंस्टॉल की जानकारी सहेजी जा रही है...
StatusRunProgram=इंस्टॉलेशन पूरा किया जा रहा है...
StatusRestartingApplications=ऐप्लिकेशन फिर से शुरू किए जा रहे हैं...
StatusRollback=बदलाव वापस लिए जा रहे हैं...

; *** Misc. errors
ErrorInternal2=आंतरिक त्रुटि: %1
ErrorFunctionFailedNoCode=%1 विफल रहा
ErrorFunctionFailed=%1 विफल रहा, कोड %2
ErrorFunctionFailedWithMessage=%1 विफल रहा, कोड %2।%n%3
ErrorExecutingProgram=फ़ाइल नहीं चलाई जा सकी:%n%1

; *** Registry errors
ErrorRegOpenKey=रजिस्ट्री कुंजी खोलने में त्रुटि:%n%1\%2
ErrorRegCreateKey=रजिस्ट्री कुंजी बनाने में त्रुटि:%n%1\%2
ErrorRegWriteKey=रजिस्ट्री कुंजी में लिखने में त्रुटि:%n%1\%2

; *** INI errors
ErrorIniEntry=फ़ाइल "%1" में INI प्रविष्टि बनाने में त्रुटि।

; *** File copying errors
FileAbortRetryIgnoreSkipNotRecommended=यह फ़ाइल छोड़ दें(&S) (अनुशंसित नहीं)
FileAbortRetryIgnoreIgnoreNotRecommended=त्रुटि को अनदेखा करें और जारी रखें(&I) (अनुशंसित नहीं)
SourceIsCorrupted=स्रोत फ़ाइल खराब है
SourceDoesntExist=स्रोत फ़ाइल "%1" मौजूद नहीं है
SourceVerificationFailed=स्रोत फ़ाइल की जाँच विफल रही: %1
VerificationSignatureDoesntExist=हस्ताक्षर फ़ाइल "%1" मौजूद नहीं है
VerificationSignatureInvalid=हस्ताक्षर फ़ाइल "%1" अमान्य है
VerificationKeyNotFound=हस्ताक्षर फ़ाइल "%1" एक अज्ञात कुंजी का इस्तेमाल करती है
VerificationFileNameIncorrect=फ़ाइल का नाम गलत है
VerificationFileTagIncorrect=फ़ाइल का टैग गलत है
VerificationFileSizeIncorrect=फ़ाइल का आकार गलत है
VerificationFileHashIncorrect=फ़ाइल का हैश गलत है
ExistingFileReadOnly2=मौजूदा फ़ाइल बदली नहीं जा सकी, क्योंकि वह केवल पढ़ने के लिए है।
ExistingFileReadOnlyRetry=“केवल पढ़ने के लिए” हटाएँ और फिर से कोशिश करें(&R)
ExistingFileReadOnlyKeepExisting=मौजूदा फ़ाइल रखें(&K)
ErrorReadingExistingDest=मौजूदा फ़ाइल पढ़ते समय एक त्रुटि हुई:
FileExistsSelectAction=कार्रवाई चुनें
FileExists2=फ़ाइल पहले से मौजूद है।
FileExistsOverwriteExisting=मौजूदा फ़ाइल को बदल दें(&O)
FileExistsKeepExisting=मौजूदा फ़ाइल रखें(&K)
FileExistsOverwriteOrKeepAll=अगले टकरावों में भी यही करें(&D)
ExistingFileNewerSelectAction=कार्रवाई चुनें
ExistingFileNewer2=मौजूदा फ़ाइल उस फ़ाइल से नई है जिसे सेटअप इंस्टॉल करना चाहता है।
ExistingFileNewerOverwriteExisting=मौजूदा फ़ाइल को बदल दें(&O)
ExistingFileNewerKeepExisting=मौजूदा फ़ाइल रखें(&K) (अनुशंसित)
ExistingFileNewerOverwriteOrKeepAll=अगले टकरावों में भी यही करें(&D)
ErrorChangingAttr=मौजूदा फ़ाइल की विशेषताएँ बदलते समय एक त्रुटि हुई:
ErrorCreatingTemp=लक्ष्य फ़ोल्डर में फ़ाइल बनाते समय एक त्रुटि हुई:
ErrorReadingSource=स्रोत फ़ाइल पढ़ते समय एक त्रुटि हुई:
ErrorCopying=फ़ाइल कॉपी करते समय एक त्रुटि हुई:
ErrorDownloading=फ़ाइल डाउनलोड करते समय एक त्रुटि हुई:
ErrorExtracting=आर्काइव निकालते समय एक त्रुटि हुई:
ErrorReplacingExistingFile=मौजूदा फ़ाइल बदलते समय एक त्रुटि हुई:
ErrorRestartReplace=RestartReplace विफल रहा:
ErrorRenamingTemp=लक्ष्य फ़ोल्डर में फ़ाइल का नाम बदलते समय एक त्रुटि हुई:
ErrorRegisterServer=DLL/OCX रजिस्टर नहीं किया जा सका: %1
ErrorRegSvr32Failed=RegSvr32 निकास कोड %1 के साथ विफल रहा
ErrorRegisterTypeLib=टाइप लाइब्रेरी रजिस्टर नहीं की जा सकी: %1

; *** Uninstall display name markings
; used for example as 'My Program (32-bit)'
UninstallDisplayNameMark=%1 (%2)
; used for example as 'My Program (32-bit, All users)'
UninstallDisplayNameMarks=%1 (%2, %3)
UninstallDisplayNameMark32Bit=32-बिट
UninstallDisplayNameMark64Bit=64-बिट
UninstallDisplayNameMarkAllUsers=सभी उपयोगकर्ता
UninstallDisplayNameMarkCurrentUser=मौजूदा उपयोगकर्ता

; *** Post-installation errors
ErrorOpeningReadme=README फ़ाइल खोलते समय एक त्रुटि हुई।
ErrorRestartingComputer=सेटअप कंप्यूटर को फिर से चालू नहीं कर सका। कृपया इसे खुद करें।

; *** Uninstaller messages
UninstallNotFound=फ़ाइल "%1" मौजूद नहीं है। अनइंस्टॉल नहीं किया जा सकता।
UninstallOpenError=फ़ाइल "%1" खोली नहीं जा सकी। अनइंस्टॉल नहीं किया जा सकता
UninstallUnsupportedVer=अनइंस्टॉल लॉग फ़ाइल "%1" ऐसे फ़ॉर्मैट में है जिसे अनइंस्टॉलर का यह संस्करण नहीं पहचानता। अनइंस्टॉल नहीं किया जा सकता
UninstallUnknownEntry=अनइंस्टॉल लॉग में एक अज्ञात प्रविष्टि (%1) मिली
ConfirmUninstall=क्या आप सचमुच %1 और उसके सभी घटकों को पूरी तरह हटाना चाहते हैं?
UninstallOnlyOnWin64=यह इंस्टॉलेशन केवल 64-बिट Windows पर अनइंस्टॉल किया जा सकता है।
OnlyAdminCanUninstall=यह इंस्टॉलेशन केवल व्यवस्थापक अधिकार वाला उपयोगकर्ता अनइंस्टॉल कर सकता है।
UninstallStatusLabel=कृपया प्रतीक्षा करें, %1 को आपके कंप्यूटर से हटाया जा रहा है।
UninstalledAll=%1 को आपके कंप्यूटर से हटा दिया गया।
UninstalledMost=%1 का अनइंस्टॉल पूरा हुआ।%n%nकुछ हिस्से हटाए नहीं जा सके। इन्हें आप खुद हटा सकते हैं।
UninstalledAndNeedsRestart=%1 का अनइंस्टॉल पूरा करने के लिए आपके कंप्यूटर को फिर से चालू करना होगा।%n%nक्या आप अभी फिर से चालू करना चाहते हैं?
UninstallDataCorrupted=फ़ाइल "%1" खराब है। अनइंस्टॉल नहीं किया जा सकता

; *** Uninstallation phase messages
ConfirmDeleteSharedFileTitle=साझा फ़ाइल हटाएँ?
ConfirmDeleteSharedFile2=सिस्टम के अनुसार यह साझा फ़ाइल अब किसी प्रोग्राम के इस्तेमाल में नहीं है। क्या अनइंस्टॉल इस साझा फ़ाइल को हटा दे?%n%nअगर कोई प्रोग्राम अब भी इस फ़ाइल का इस्तेमाल करता है और इसे हटा दिया जाता है, तो वह प्रोग्राम ठीक से काम नहीं कर पाएगा। अगर आप पक्का नहीं जानते, तो “नहीं” चुनें। फ़ाइल को सिस्टम पर छोड़ने से कोई नुकसान नहीं होता।
SharedFileNameLabel=फ़ाइल का नाम:
SharedFileLocationLabel=जगह:
WizardUninstalling=अनइंस्टॉल की स्थिति
StatusUninstalling=%1 अनइंस्टॉल हो रहा है...

; *** Shutdown block reasons
ShutdownBlockReasonInstallingApp=%1 इंस्टॉल हो रहा है।
ShutdownBlockReasonUninstallingApp=%1 अनइंस्टॉल हो रहा है।

; The custom messages below aren't used by Setup itself, but if you make
; use of them in your scripts, you'll want to translate them.

[CustomMessages]

NameAndVersion=%1 संस्करण %2
AdditionalIcons=अतिरिक्त शॉर्टकट:
CreateDesktopIcon=डेस्कटॉप शॉर्टकट बनाएँ(&D)
CreateQuickLaunchIcon=क्विक लॉन्च शॉर्टकट बनाएँ(&Q)
ProgramOnTheWeb=वेब पर %1
UninstallProgram=%1 अनइंस्टॉल करें
LaunchProgram=%1 शुरू करें
AssocFileExtension=%1 को फ़ाइल एक्सटेंशन %2 से जोड़ें(&A)
AssocingFileExtension=%1 को फ़ाइल एक्सटेंशन %2 से जोड़ा जा रहा है...
AutoStartProgramGroupDescription=स्टार्टअप:
AutoStartProgram=%1 को अपने आप शुरू करें
AddonHostProgramNotFound=आपके चुने गए फ़ोल्डर में %1 नहीं मिला।%n%nक्या आप फिर भी जारी रखना चाहते हैं?
