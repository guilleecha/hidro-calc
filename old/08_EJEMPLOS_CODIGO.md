# Ejemplos Prácticos - Interacción con Base de Datos HidroCalc

## 📚 Ejemplos de Código

### Ejemplo 1: Crear un proyecto completo con cuenca y tormentas

```python
from sqlalchemy.orm import Session
from core.models import Project, Watershed, DesignStorm, Hydrograph
from database import SessionLocal

def crear_proyecto_completo():
    """
    Crear un proyecto de ejemplo con:
    - 1 Proyecto
    - 1 Cuenca
    - 4 Tormentas (diferentes duraciones)
    """
    db = SessionLocal()
    
    try:
        # 1. Crear Proyecto
        proyecto = Project(
            name="Presa Tacuarembó",
            description="Análisis de tormentas para diseño de vertedor",
            location="Tacuarembó, Uruguay",
            country="Uruguay",
            region="Tacuarembó"
        )
        db.add(proyecto)
        db.flush()  # Para obtener el ID
        print(f"✅ Proyecto creado: {proyecto.name} (ID: {proyecto.id})")
        
        # 2. Crear Cuenca
        cuenca = Watershed(
            project_id=proyecto.id,
            name="Río Negro - Sección Alto",
            description="Cuenca aguas arriba de Presa Tacuarembó",
            area_hectareas=1250,
            tc_horas=3.5,
            nc_scs=65,
            latitude=-32.85,
            longitude=-56.45,
            elevation_m=120,
            c_racional=0.42
        )
        db.add(cuenca)
        db.flush()
        print(f"✅ Cuenca creada: {cuenca.name} (ID: {cuenca.id})")
        
        # 3. Crear 4 Tormentas con diferentes duraciones
        duraciones = [
            {"duracion": 2.0, "lluvia": 65.3, "nombre": "2h"},
            {"duracion": 6.0, "lluvia": 95.5, "nombre": "6h"},
            {"duracion": 12.0, "lluvia": 125.8, "nombre": "12h"},
            {"duracion": 24.0, "lluvia": 165.2, "nombre": "24h"},
        ]
        
        for dur_info in duraciones:
            tormenta = DesignStorm(
                watershed_id=cuenca.id,
                name=f"Tr=50 Años {dur_info['nombre']}",
                description=f"Tormenta de {dur_info['duracion']}h para Tr=50 años",
                return_period_years=50,
                duration_hours=dur_info['duracion'],
                total_rainfall_mm=dur_info['lluvia'],
                distribution_type="alternating_block",
                time_step_minutes=5
            )
            db.add(tormenta)
            db.flush()
            print(f"  ✅ Tormenta creada: Tr=50 {dur_info['nombre']} (ID: {tormenta.id})")
        
        db.commit()
        print(f"\n✅ Proyecto completo creado con éxito")
        return proyecto.id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


# Usar:
proyecto_id = crear_proyecto_completo()
```

---

### Ejemplo 2: Guardar un hidrograma calculado

```python
from core.models import Hydrograph, DesignStorm
from database import SessionLocal

def guardar_hidrograma(design_storm_id: int, datos_hidrograma: dict):
    """
    Guardar un hidrograma completo con su serie temporal
    
    Parámetros:
    -----------
    design_storm_id: ID de la tormenta
    datos_hidrograma: dict con:
        {
            "method": "scs_alternating_block",
            "peak_discharge_m3s": 456.78,
            "time_to_peak_minutes": 65,
            "total_runoff_m3": 1250000,
            "hydrograph_data": [
                {"time_min": 0, "discharge_m3s": 0, "cumulative_volume_m3": 0},
                {"time_min": 5, "discharge_m3s": 12.3, "cumulative_volume_m3": 1537.5},
                ...
            ],
            "rainfall_excess_mm": 98.5,
            "infiltration_total_mm": 45.2
        }
    """
    db = SessionLocal()
    
    try:
        # Verificar que la tormenta existe
        storm = db.query(DesignStorm).filter(
            DesignStorm.id == design_storm_id
        ).first()
        
        if not storm:
            raise ValueError(f"Tormenta {design_storm_id} no encontrada")
        
        # Calcular valores adicionales
        peak_m3s = datos_hidrograma['peak_discharge_m3s']
        peak_lps = peak_m3s * 1000  # Convertir a L/s
        
        area_m2 = storm.watershed.area_hectareas * 10000  # ha a m²
        vol_hm3 = datos_hidrograma['total_runoff_m3'] / 1e6  # m³ a hm³
        
        # Crear hidrograma
        hydro = Hydrograph(
            design_storm_id=design_storm_id,
            name=f"{storm.name} - {datos_hidrograma['method']}",
            method=datos_hidrograma['method'],
            peak_discharge_m3s=peak_m3s,
            peak_discharge_lps=peak_lps,
            time_to_peak_minutes=datos_hidrograma.get('time_to_peak_minutes'),
            total_runoff_mm=datos_hidrograma.get('total_runoff_mm'),
            total_runoff_m3=datos_hidrograma['total_runoff_m3'],
            volume_hm3=vol_hm3,
            hydrograph_data=datos_hidrograma['hydrograph_data'],
            rainfall_excess_mm=datos_hidrograma.get('rainfall_excess_mm'),
            infiltration_total_mm=datos_hidrograma.get('infiltration_total_mm'),
            notes=f"Calculado con {datos_hidrograma['method']}"
        )
        
        db.add(hydro)
        db.commit()
        db.refresh(hydro)
        
        print(f"✅ Hidrograma guardado:")
        print(f"   ID: {hydro.id}")
        print(f"   Método: {hydro.method}")
        print(f"   Qmax: {hydro.peak_discharge_m3s:.2f} m³/s")
        print(f"   Volumen: {hydro.volume_hm3:.4f} hm³")
        print(f"   Puntos datos: {len(hydro.hydrograph_data)}")
        
        return hydro.id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al guardar: {str(e)}")
    finally:
        db.close()


# Ejemplo de uso:
datos_ejemplo = {
    "method": "scs_alternating_block",
    "peak_discharge_m3s": 456.78,
    "time_to_peak_minutes": 65,
    "total_runoff_m3": 1250000,
    "hydrograph_data": [
        {"time_min": 0, "discharge_m3s": 0, "cumulative_volume_m3": 0},
        {"time_min": 5, "discharge_m3s": 12.3, "cumulative_volume_m3": 1537.5},
        {"time_min": 10, "discharge_m3s": 45.6, "cumulative_volume_m3": 7312.5},
        # ... más puntos ...
    ],
    "rainfall_excess_mm": 98.5,
    "infiltration_total_mm": 45.2
}

# guardar_hidrograma(design_storm_id=1, datos_hidrograma=datos_ejemplo)
```

---

### Ejemplo 3: Recuperar y comparar hidrogramas

```python
from core.models import Hydrograph, DesignStorm
from database import SessionLocal
import statistics

def comparar_hidrogramas_por_duracion(watershed_id: int, tr_anos: int):
    """
    Obtener todos los hidrogramas de una cuenca para un Tr
    y compararlos por duración de tormenta
    """
    db = SessionLocal()
    
    try:
        # Query: obtener hidrogramas ordenados por duración
        hidrogramas = (
            db.query(Hydrograph, DesignStorm)
            .join(DesignStorm)
            .filter(
                DesignStorm.watershed_id == watershed_id,
                DesignStorm.return_period_years == tr_anos
            )
            .order_by(DesignStorm.duration_hours)
            .all()
        )
        
        if not hidrogramas:
            print(f"⚠️  No se encontraron hidrogramas")
            return
        
        print(f"\n{'='*70}")
        print(f"COMPARACIÓN DE HIDROGRAMAS - Cuenca {watershed_id}, Tr={tr_anos} años")
        print(f"{'='*70}\n")
        
        # Tabla comparativa
        print(f"{'Duración':<12} {'Qmax (m³/s)':<15} {'Volumen (m³)':<15} {'T Pico (min)':<15}")
        print("-" * 70)
        
        resultados = []
        for hydro, storm in hidrogramas:
            print(f"{storm.duration_hours:>6.1f} h     "
                  f"{hydro.peak_discharge_m3s:>12.2f}    "
                  f"{hydro.total_runoff_m3:>13.0f}    "
                  f"{hydro.time_to_peak_minutes:>12.0f}")
            
            resultados.append({
                'duracion': storm.duration_hours,
                'qmax': hydro.peak_discharge_m3s,
                'volumen': hydro.total_runoff_m3,
                'tpico': hydro.time_to_peak_minutes,
                'hydro_id': hydro.id
            })
        
        print("-" * 70)
        
        # Estadísticas
        qmax_valores = [r['qmax'] for r in resultados]
        vol_valores = [r['volumen'] for r in resultados]
        
        print(f"\nESTADÍSTICAS:")
        print(f"  Caudal máximo:")
        print(f"    • Mayor: {max(qmax_valores):.2f} m³/s en {resultados[qmax_valores.index(max(qmax_valores))]['duracion']:.1f}h")
        print(f"    • Menor: {min(qmax_valores):.2f} m³/s en {resultados[qmax_valores.index(min(qmax_valores))]['duracion']:.1f}h")
        print(f"    • Promedio: {statistics.mean(qmax_valores):.2f} m³/s")
        
        print(f"\n  Volumen de escorrentía:")
        print(f"    • Mayor: {max(vol_valores):,.0f} m³ en {resultados[vol_valores.index(max(vol_valores))]['duracion']:.1f}h")
        print(f"    • Menor: {min(vol_valores):,.0f} m³ en {resultados[vol_valores.index(min(vol_valores))]['duracion']:.1f}h")
        print(f"    • Promedio: {statistics.mean(vol_valores):,.0f} m³")
        
        # Recomendación
        print(f"\n💡 RECOMENDACIONES:")
        idx_max_q = qmax_valores.index(max(qmax_valores))
        idx_max_v = vol_valores.index(max(vol_valores))
        
        print(f"  • Para dimensionamiento de canal (máximo caudal):")
        print(f"    Usar tormenta de {resultados[idx_max_q]['duracion']:.1f}h "
              f"con Qmax = {max(qmax_valores):.2f} m³/s")
        
        print(f"\n  • Para dimensionamiento de almacenamiento (máximo volumen):")
        print(f"    Usar tormenta de {resultados[idx_max_v]['duracion']:.1f}h "
              f"con V = {max(vol_valores):,.0f} m³")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


# Usar:
# comparar_hidrogramas_por_duracion(watershed_id=1, tr_anos=10)
```

---

### Ejemplo 4: Exportar hidrograma a CSV

```python
import csv
from core.models import Hydrograph
from database import SessionLocal

def exportar_hidrograma_csv(hydrograph_id: int, archivo_salida: str):
    """
    Exportar hidrograma a archivo CSV
    """
    db = SessionLocal()
    
    try:
        hydro = db.query(Hydrograph).filter(
            Hydrograph.id == hydrograph_id
        ).first()
        
        if not hydro:
            print(f"❌ Hidrograma {hydrograph_id} no encontrado")
            return
        
        # Escribir CSV
        with open(archivo_salida, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Tiempo (min)',
                'Caudal (m³/s)',
                'Caudal (L/s)',
                'Volumen Acumulado (m³)',
                'Volumen Acumulado (hm³)'
            ])
            
            # Datos
            for punto in hydro.hydrograph_data:
                vol_hm3 = punto['cumulative_volume_m3'] / 1e6
                writer.writerow([
                    punto['time_min'],
                    f"{punto['discharge_m3s']:.4f}",
                    f"{punto['discharge_m3s']*1000:.2f}",
                    f"{punto['cumulative_volume_m3']:,.0f}",
                    f"{vol_hm3:.6f}"
                ])
        
        print(f"✅ Hidrograma exportado a: {archivo_salida}")
        print(f"   Puntos datos: {len(hydro.hydrograph_data)}")
        print(f"   Método: {hydro.method}")
        print(f"   Qmax: {hydro.peak_discharge_m3s:.2f} m³/s")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


# Usar:
# exportar_hidrograma_csv(hydrograph_id=1, archivo_salida="hidrograma_export.csv")
```

---

### Ejemplo 5: Consulta avanzada con JOIN

```python
from sqlalchemy import func, desc
from core.models import Project, Watershed, DesignStorm, Hydrograph
from database import SessionLocal

def obtener_estadisticas_proyecto(project_id: int):
    """
    Obtener estadísticas completas de un proyecto
    """
    db = SessionLocal()
    
    try:
        # 1. Contar elementos
        project = db.query(Project).filter(Project.id == project_id).first()
        num_cuencas = db.query(Watershed).filter(
            Watershed.project_id == project_id
        ).count()
        
        num_tormentas = db.query(DesignStorm).join(Watershed).filter(
            Watershed.project_id == project_id
        ).count()
        
        num_hidrogramas = db.query(Hydrograph).join(DesignStorm).join(Watershed).filter(
            Watershed.project_id == project_id
        ).count()
        
        # 2. Obtener máximos
        max_flow = db.query(func.max(Hydrograph.peak_discharge_m3s)).join(
            DesignStorm
        ).join(Watershed).filter(
            Watershed.project_id == project_id
        ).scalar()
        
        max_volume = db.query(func.max(Hydrograph.total_runoff_m3)).join(
            DesignStorm
        ).join(Watershed).filter(
            Watershed.project_id == project_id
        ).scalar()
        
        # 3. Hidrograma más reciente
        ultimo_hydro = db.query(Hydrograph).join(DesignStorm).join(Watershed).filter(
            Watershed.project_id == project_id
        ).order_by(desc(Hydrograph.created_at)).first()
        
        # Mostrar resumen
        print(f"\n{'='*60}")
        print(f"ESTADÍSTICAS DEL PROYECTO: {project.name}")
        print(f"{'='*60}")
        print(f"Cuencas: {num_cuencas}")
        print(f"Tormentas: {num_tormentas}")
        print(f"Hidrogramas: {num_hidrogramas}")
        print(f"\nValores máximos encontrados:")
        print(f"  • Caudal máximo: {max_flow:.2f} m³/s")
        print(f"  • Volumen máximo: {max_volume:,.0f} m³")
        print(f"\nÚltimo hidrograma guardado:")
        if ultimo_hydro:
            print(f"  • ID: {ultimo_hydro.id}")
            print(f"  • Fecha: {ultimo_hydro.created_at}")
            print(f"  • Método: {ultimo_hydro.method}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


# Usar:
# obtener_estadisticas_proyecto(project_id=1)
```

---

### Ejemplo 6: Script de mantenimiento

```python
from datetime import datetime, timedelta
from core.models import Hydrograph, DesignStorm
from database import SessionLocal

def limpiar_hidrogramas_antiguos(dias: int = 30):
    """
    Eliminar hidrogramas más antiguos de N días
    """
    db = SessionLocal()
    
    try:
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        
        # Contar hidrogramas a eliminar
        count = db.query(Hydrograph).filter(
            Hydrograph.created_at < fecha_limite
        ).count()
        
        if count == 0:
            print(f"ℹ️  No hay hidrogramas más antiguos de {dias} días")
            return
        
        print(f"⚠️  Se van a eliminar {count} hidrogramas")
        confirmar = input("¿Continuar? (s/n): ")
        
        if confirmar.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        # Eliminar
        db.query(Hydrograph).filter(
            Hydrograph.created_at < fecha_limite
        ).delete()
        
        db.commit()
        print(f"✅ {count} hidrogramas eliminados")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()


# Usar:
# limpiar_hidrogramas_antiguos(dias=30)
```

---

## 📖 Resumen de Patrones

### Crear registro
```python
db = SessionLocal()
nuevo_objeto = Model(campo1=valor1, ...)
db.add(nuevo_objeto)
db.commit()
db.close()
```

### Leer registro
```python
db = SessionLocal()
objeto = db.query(Model).filter(Model.id == 1).first()
db.close()
```

### Actualizar registro
```python
db = SessionLocal()
objeto = db.query(Model).filter(Model.id == 1).first()
objeto.campo = nuevo_valor
db.commit()
db.close()
```

### Eliminar registro
```python
db = SessionLocal()
db.query(Model).filter(Model.id == 1).delete()
db.commit()
db.close()
```

### Consulta con JOIN
```python
resultados = db.query(Model1, Model2).join(Model2).filter(...).all()
```

---

¿Necesitas ejemplos adicionales para casos específicos?
