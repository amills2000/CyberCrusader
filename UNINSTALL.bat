@ECHO OFF
TITLE CyberCrusader Uninstaller
REM Force Admin
>NUL 2>&1 "%SystemRoot%\system32\cacls.exe" "%SystemRoot%\system32\config\system"
IF %ERRORLEVEL% NEQ 0 (
  ECHO Error: Run as Admin
  PAUSE>NUL
  EXIT
)
ECHO Running as Admin!
TITLE CyberCrusader Installer
REG delete "HKEY_CLASSES_ROOT\Directory\shell\CyberCrusader" /f
ECHO Done.
PAUSE>NUL