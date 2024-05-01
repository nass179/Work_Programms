



python -m pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
cd tests && pytest --cov arrow -k "not parse_tz_name_zzz"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
