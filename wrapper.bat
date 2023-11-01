@ECHO OFF
TITLE CyberCrusader
REM The implementation of %~dp0 is *critically broken* and will not work if the bat script is invoked via a path that is enclosed in quotes. Microsoft is refusing to fix this bug due to cmd.exe being a legacy product. See https://github.com/microsoft/terminal/issues/15212 for details.
cd /D %~d0
cd %~dp0
python main.py %*
PAUSE>NUL