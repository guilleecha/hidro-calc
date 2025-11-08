@echo off
REM Script para iniciar el servidor HidroCalc en entorno virtual

echo ========================================
echo   HidroCalc - Inicio de Servidor
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Creando entorno virtual...
    python -m venv .venv
    echo     Entorno virtual creado correctamente!
    echo.
) else (
    echo [!] Entorno virtual ya existe
    echo.
)

REM Activar entorno virtual
echo [2/3] Activando entorno virtual...
call .venv\Scripts\activate.bat
echo     Entorno virtual activado!
echo.

REM Verificar si las dependencias estan instaladas
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [3/3] Instalando dependencias (esto puede tomar unos minutos)...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo     Dependencias instaladas correctamente!
    echo.
) else (
    echo [!] Dependencias ya instaladas
    echo.
)

echo ========================================
echo   Iniciando servidor...
echo ========================================
echo.
echo El servidor se iniciara en: http://localhost:8000
echo Modulo IDF disponible en: http://localhost:8000/idf
echo Documentacion API: http://localhost:8000/docs
echo.
echo Presiona CTRL+C para detener el servidor
echo.
echo ========================================
echo.

REM Iniciar el servidor
python src/main.py

pause
