@ECHO OFF

call virtual\scripts\activate.bat

echo 'Ambiente activo....'
echo 'Creando Variables Flask'
set FLASK_APP=main.py
set FLASK_DEBUG=1
set FLASK_ENV=development
