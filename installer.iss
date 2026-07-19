; Inno Setup script — builds "VideoStudioSetup.exe" from the PyInstaller
; one-folder build in dist\Video Studio\.
;
; Version is passed in by CI (iscc /DAppVer=1.2.3) so it stays in lockstep with
; videostudio.__version__; defaults here for local builds.

#ifndef AppVer
  #define AppVer "1.0.0"
#endif

[Setup]
AppName=Video Studio
AppVersion={#AppVer}
AppPublisher=Water Resources
; Let the silent auto-updater replace a running install cleanly.
CloseApplications=yes
RestartApplications=no
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
