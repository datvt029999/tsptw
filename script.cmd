@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

pushd "%SCRIPT_DIR%solutions\%~1"

if not exist "%SCRIPT_DIR%output\%~1\%~2" (
    mkdir "%SCRIPT_DIR%output\%~1\%~2"
)

if "%~1" == "gurobi" (
    $env:GRB_LICENSE_FILE = "gurobi.lic"
) 
python "%~2.py" "%~3" > "%SCRIPT_DIR%output\%~1\%~2\%~3.txt"
popd
endlocal