



pip check || 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
bokeh --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
