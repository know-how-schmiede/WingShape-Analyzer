; Inno Setup Script for WingShape-Analyzer
; Compile this script with Inno Setup to generate a Setup.exe

#define MyAppName "WingShape-Analyzer"
#define MyAppPublisher ""
#define MyAppExeName "WingShape-Analyzer.exe"
#define MyAppDist "..\\..\\dist\\WingShape-Analyzer"
#define MyAppIcon "..\\assets\\app.ico"

#include "version.iss"
#define MyAppVersion APP_VERSION

[Setup]
AppId={{7C4E2A1D-8B30-4B6C-9D16-1A6A3B4E1E11}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\output
OutputBaseFilename=WingShape-Analyzer-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesInstallIn64BitMode=x64
#ifexist MyAppIcon
SetupIconFile={#MyAppIcon}
#endif

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#MyAppDist}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
#ifexist MyAppIcon
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{#MyAppIcon}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{#MyAppIcon}"
#else
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
#endif

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName} starten"; Flags: nowait postinstall skipifsilent
