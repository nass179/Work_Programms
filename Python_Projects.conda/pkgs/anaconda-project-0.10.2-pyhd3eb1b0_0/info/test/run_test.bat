



echo "First of test commands"
IF %ERRORLEVEL% NEQ 0 exit /B 1
anaconda-project --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
anaconda-project --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
echo "Last of test commands"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
