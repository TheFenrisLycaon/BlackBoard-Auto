echo INITIALIZING
IF EXIST "Data\.setupComp" ( start sysFiles\python.exe sysFiles\main.py ) else ( start sysFiles\python.exe sysFiles\setup.py ) 