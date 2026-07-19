; Inno Setup script — builds "VideoStudioSetup.exe" from the PyInstaller
; one-folder build in dist\Video Studio\.

[Setup]
AppName=Video Studio
AppVersion=1.0.0
AppPublisher=Water Resources
DefaultDirName={autopf}\Video Studio
DefaultGroupName=Video Studio
DisableProgramGroupPage=yes
OutputDir=installer_out
OutputBaseFilename=VideoStudioSetup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile=packaging\icon.ico
UninstallDisplayIcon={app}\Video Studio.exe
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\Video Studio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Video Studio"; Filename: "{app}\Video Studio.exe"
Name: "{group}\Uninstall Video Studio"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Video Studio"; Filename: "{app}\Video Studio.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Video Studio.exe"; Description: "Launch Video Studio"; Flags: nowait postinstall skipifsilent
