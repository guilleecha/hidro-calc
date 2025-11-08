# 🚀 Cómo Iniciar el Servidor HidroCalc

## Método Recomendado: Usar el Script Automático

### Windows (Recomendado)

1. **Abre una terminal en el directorio del proyecto:**
   ```
   C:\myprojects\hidro-calc
   ```

2. **Ejecuta el script de inicio:**
   ```cmd
   start-server.bat
   ```

3. **¡Listo!** El script se encargará de:
   - ✅ Crear el entorno virtual (si no existe)
   - ✅ Activar el entorno virtual
   - ✅ Instalar dependencias (si no están instaladas)
   - ✅ Iniciar el servidor

4. **Abre tu navegador en:**
   - Página principal: http://localhost:8000
   - Módulo IDF: http://localhost:8000/idf
   - Documentación API: http://localhost:8000/docs

5. **Para detener el servidor:**
   - Presiona `CTRL + C` en la terminal
   - Cierra la ventana de la terminal

---

## Método Manual: Paso a Paso

Si prefieres hacerlo manualmente o usar PowerShell/Git Bash:

### 1. Detener procesos Python anteriores

**Opción A - PowerShell (como Administrador):**
```powershell
Get-Process python | Stop-Process -Force
```

**Opción B - Administrador de Tareas:**
- Presiona `Ctrl + Shift + Esc`
- Busca todos los procesos `python.exe`
- Finaliza TODOS los procesos de Python

### 2. Crear el entorno virtual (solo la primera vez)

```cmd
python -m venv .venv
```

### 3. Activar el entorno virtual

**CMD (Símbolo del sistema):**
```cmd
.venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Git Bash:**
```bash
source .venv/Scripts/activate
```

Deberías ver `(.venv)` al inicio de tu línea de comandos.

### 4. Instalar dependencias (solo la primera vez o cuando cambien)

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Esto instalará:
- FastAPI
- Uvicorn
- Pydantic
- NumPy
- SciPy
- Pandas
- Matplotlib
- Pytest
- Y otras dependencias

### 5. Iniciar el servidor

```cmd
python src/main.py
```

### 6. Acceder a la aplicación

Abre tu navegador en:
- **Página principal:** http://localhost:8000
- **Módulo IDF:** http://localhost:8000/idf
- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🧪 Ejecutar Tests

Con el entorno virtual activado:

```cmd
# Ejecutar todos los tests
python -m pytest

# Ejecutar solo tests del módulo IDF
python -m pytest tests/test_idf.py -v

# Ejecutar tests con cobertura
python -m pytest --cov=src --cov-report=html
```

---

## ❓ Solución de Problemas

### Error: "No module named 'fastapi'"

**Solución:** Asegúrate de que el entorno virtual está activado y las dependencias instaladas:
```cmd
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### Error: "Puerto 8000 ya está en uso"

**Solución:** Hay otro servidor corriendo. Detén todos los procesos Python:
```powershell
Get-Process python | Stop-Process -Force
```

### Error: "Ruta no encontrada: /idf"

**Solución:** El servidor está usando código viejo. Sigue estos pasos:
1. Detén TODOS los procesos Python
2. Inicia el servidor nuevamente con el entorno virtual activado
3. Verifica que el archivo `src/main.py` esté actualizado

### El entorno virtual no se activa en PowerShell

**Solución:** PowerShell tiene restricciones de ejecución. Ejecuta como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 Notas Importantes

- **Siempre** usa el entorno virtual para ejecutar el servidor
- **No** ejecutes `python src/main.py` fuera del entorno virtual
- Si modificas el código, el servidor se recargará automáticamente (modo desarrollo)
- Para producción, desactiva el modo `reload` en `src/main.py`

---

## 🎯 Resumen Rápido

```cmd
# Cada vez que quieras trabajar en el proyecto:

1. cd C:\myprojects\hidro-calc
2. .venv\Scripts\activate.bat
3. python src/main.py

# O simplemente:
start-server.bat
```

---

## ✅ Verificación

Para verificar que todo está correcto:

```cmd
# Con el entorno virtual activado:
python -c "from src.main import app; print('✅ App importada correctamente')"
python -c "from src.core.idf_uruguay import calculate_intensity_idf; print('✅ Módulo IDF OK')"
```

Si ambos comandos muestran ✅, ¡todo está listo!
