@echo off
call "C:\Program Files\QGIS 3.2\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.2\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.2\bin\py3_env.bat"

@echo on
pyuic5 nuevoRol.ui -o nuevoRol.py
