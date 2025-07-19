@echo off
REM --- Nettoyage des anciens fichiers ---
echo 🔄 Nettoyage...
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del /q *.spec >nul 2>&1

REM --- Compilation ---
echo 🚀 Compilation avec PyInstaller...
pyinstaller ^
--noconfirm ^
--onefile ^
--windowed ^
--name "Protocoles QT" ^
--icon=resources\logo.ico ^
--add-data "resources;resources" ^
--add-data "ui;ui" ^
--add-data "core;core" ^
main.py

echo ✅ Compilation terminée !
echo 📁 Le fichier exécutable est dans le dossier: dist\
pause
