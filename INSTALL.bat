@ECHO OFF
TITLE CyberCrusader Installer
REM Force Admin
>NUL 2>&1 "%SystemRoot%\system32\cacls.exe" "%SystemRoot%\system32\config\system"
IF %ERRORLEVEL% NEQ 0 (
  ECHO Error: Run as Admin
  PAUSE>NUL
  EXIT
)
ECHO Running as Admin!
cd /D %~d0
SET p=%~dp0
ECHO CyberCrusader path: %p%
REG add "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader" /f
REG add "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader" /ve /t REG_SZ /d "CyberCrusader" /f
REG add "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader" /v Icon /t REG_SZ /d "%SystemRoot%\\System32\\SHELL32.dll,209" /f
REG add "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader\command" /f
REG add "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader\command" /ve /t REG_SZ /d "%p%wrapper.bat \"-p\" \"%%1\"" /f
ECHO Done.
PAUSE>NUL