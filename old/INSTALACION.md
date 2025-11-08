# 🚀 Guía de Instalación - HidroCalc

## Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Paso 1: Descargar el Proyecto

Si tienes Git instalado:
```bash
git clone [URL_DEL_REPO]
cd hidro-calc
```

O simplemente navega al directorio del proyecto:
```bash
cd C:\myprojects\hidro-calc
```

## Paso 2: Crear Entorno Virtual

Es recomendable usar un entorno virtual para aislar las dependencias:

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

## Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si tienes problemas instalando NumPy, SciPy o Matplotlib en Windows, puedes instalar solo las dependencias básicas primero:

```bash
pip install fastapi uvicorn[standard] pydantic pydantic-settings jinja2 python-multipart
```

Las librerías científicas (NumPy, SciPy, Matplotlib) no son necesarias para el MVP del Método Racional.

## Paso 4: Ejecutar el Servidor

```bash
python src/main.py
```

O alternativamente:
```bash
uvicorn src.main:app --reload --port 8000
```

El servidor estará disponible en:
- **Aplicación Web:** http://localhost:8000
- **Documentación API (Swagger):** http://localhost:8000/docs
- **Documentación API (ReDoc):** http://localhost:8000/redoc

## Paso 5: Verificar la Instalación

Abre tu navegador y visita:
- http://localhost:8000 - Deberías ver la página principal de HidroCalc
- http://localhost:8000/rational - Calculadora del Método Racional

También puedes verificar la API:
```bash
curl http://localhost:8000/api/health
```

Deberías recibir:
```json
{
  "status": "healthy",
  "project": "HidroCalc",
  "version": "1.0.0"
}
```

## Paso 6: Ejecutar Tests (Opcional)

Para verificar que todo funciona correctamente:

```bash
pytest tests/ -v
```

Deberías ver todos los tests pasando (43 passed).

## Uso de la Aplicación

### Interfaz Web

1. Visita http://localhost:8000/rational
2. Ingresa los valores:
   - **C:** Coeficiente de escorrentía (0-1)
   - **I:** Intensidad de lluvia (mm/h)
   - **A:** Área de la cuenca (ha)
3. Haz clic en "Calcular Caudal"
4. Los resultados se mostrarán en el panel derecho

### API REST

Puedes usar la API directamente con cualquier cliente HTTP:

```bash
curl -X POST http://localhost:8000/api/rational \
  -H "Content-Type: application/json" \
  -d '{
    "C": 0.65,
    "I_mmh": 80,
    "A_ha": 5,
    "description": "Cuenca residencial"
  }'
```

Respuesta:
```json
{
  "Q_ls": 722.28,
  "Q_m3s": 0.7223,
  "Q_m3h": 2600.21,
  "inputs": {
    "C": 0.65,
    "I_mmh": 80.0,
    "A_ha": 5.0,
    "A_m2": 50000.0,
    "A_km2": 0.05
  },
  "description": "Cuenca residencial",
  "warnings": []
}
```

## Solución de Problemas

### Error: "No module named 'src'"

Asegúrate de ejecutar el servidor desde el directorio raíz del proyecto:
```bash
cd C:\myprojects\hidro-calc
python src/main.py
```

### Error: "Address already in use"

El puerto 8000 ya está siendo usado. Puedes:
1. Detener el proceso que usa el puerto 8000
2. Usar otro puerto:
   ```bash
   uvicorn src.main:app --port 8001
   ```

### Problemas con NumPy/SciPy en Windows

Si tienes problemas instalando librerías científicas:
1. Instala solo las dependencias básicas (ver Paso 3)
2. O descarga wheels pre-compilados desde: https://www.lfd.uci.edu/~gohlke/pythonlibs/

## Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está corriendo el servidor.

## Actualizar el Proyecto

Si hay nuevas versiones:

```bash
git pull  # Si usas Git
pip install -r requirements.txt --upgrade
```

## Próximos Pasos

Una vez que tengas el servidor corriendo, puedes:

1. Explorar la documentación interactiva en http://localhost:8000/docs
2. Probar diferentes valores en la calculadora
3. Revisar el código fuente en `src/`
4. Consultar la documentación técnica en los archivos .md

## Contacto y Soporte

Si tienes problemas o preguntas:
- Revisa la documentación en `docs/`
- Consulta los issues en GitHub
- Lee el archivo CLAUDE.md para entender la estructura del proyecto

---

**Versión:** 1.0.0
**Última actualización:** Noviembre 2025
