@echo off
call "C:\Program Files\QGIS 3.10\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.10\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.10\bin\py3_env.bat"

@echo on
pyuic5 estatusClaves_dialog_base.ui -o estatusClaves_dialog_base.py