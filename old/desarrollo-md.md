# 📋 Plan de Desarrollo - HidroCalc

## 🎯 Visión del Proyecto

Crear una herramienta web profesional que permita a ingenieros civiles realizar cálculos hidrológicos e hidráulicos de manera eficiente, con interfaz intuitiva y resultados precisos.

## 🚀 Roadmap General

### FASE 0: Setup ✅ COMPLETADA
- [x] Estructura del proyecto
- [x] Entorno virtual configurado
- [x] Dependencias instaladas
- [x] Documentación inicial (CLAUDE.md, README.md)

### FASE 1: MVP - Método Racional 🔄 EN PROGRESO
**Objetivo**: Tener una aplicación funcional básica para cálculo de caudales.

**Duración estimada**: 1-2 días

**Tareas**:
- [ ] Servidor FastAPI básico
- [ ] Módulo de cálculo del método racional
- [ ] Endpoint API para cálculo
- [ ] Interfaz web con formulario
- [ ] Validaciones frontend y backend
- [ ] Tests unitarios básicos

**Criterios de éxito**:
- Usuario puede ingresar C, I, A y obtener Q en L/s
- Validaciones funcionando correctamente
- Interfaz profesional y responsive
- Servidor corre sin errores

### FASE 2: Tormentas de Diseño 📅 PLANIFICADA
**Objetivo**: Implementar generación de tormentas sintéticas y curvas IDF.

**Duración estimada**: 3-4 días

**Tareas**:
- [ ] Base de datos de curvas IDF (JSON inicial)
- [ ] Interpolación de intensidades
- [ ] Método de bloques alternos
- [ ] Generación de hietogramas
- [ ] Distribución temporal SCS (Tipo I, II, III)
- [ ] Visualización de hietogramas (gráficos)
- [ ] Interface para selección de región y Tr
- [ ] Exportación de resultados

**Entregables**:
- Curvas IDF de al menos 3 ciudades principales
- Hietogramas de diseño configurables
- Gráficos de tormentas
- Documentación de fórmulas IDF

### FASE 3: Hidrología Avanzada 📅 PLANIFICADA
**Objetivo**: Herramientas para análisis de cuencas y generación de hidrogramas.

**Duración estimada**: 4-5 días

**Tareas**:
- [ ] Hidrograma Unitario SCS
- [ ] Método del Número de Curva (CN)
- [ ] Abstracciones iniciales
- [ ] Tiempos de concentración:
  - Kirpich
  - California Culverts Practice
  - Témez
  - Giandotti
- [ ] Routing básico de hidrogramas
- [ ] Visualización de hidrogramas
- [ ] Cálculo de volumen de escorrentía

**Entregables**:
- Tabla de valores CN por tipo de suelo
- Calculadora de tc con múltiples métodos
- Generador de hidrogramas
- Comparador de métodos

### FASE 4: Flujo Gradualmente Variado 📅 PLANIFICADA
**Objetivo**: Cálculo de perfiles de flujo en canales.

**Duración estimada**: 4-5 días

**Tareas**:
- [ ] Método de paso estándar (Standard Step)
- [ ] Cálculo de profundidad normal (Manning)
- [ ] Cálculo de profundidad crítica
- [ ] Clasificación de perfiles (M1, M2, S1, etc)
- [ ] Visualización de perfiles longitudinales
- [ ] Detección de resalto hidráulico
- [ ] Cálculo de energía específica

**Entregables**:
- Calculadora de GVF
- Gráficos de perfil longitudinal
- Tabla de resultados por estación
- Exportación a Excel/CSV

### FASE 5: Diseño de Canales 📅 PLANIFICADA
**Objetivo**: Herramientas para diseño hidráulico de canales.

**Duración estimada**: 3-4 días

**Tareas**:
- [ ] Flujo uniforme (ecuación de Manning)
- [ ] Secciones óptimas:
  - Rectangular
  - Trapezoidal
  - Circular
  - Parabólica
- [ ] Energía específica
- [ ] Momentum específico
- [ ] Resalto hidráulico
- [ ] Curvas de remanso

**Entregables**:
- Calculadora de canales
- Comparador de secciones
- Tabla de rugosidades de Manning
- Recomendaciones de diseño

### FASE 6: Obras de Drenaje 📅 PLANIFICADA
**Objetivo**: Diseño de estructuras hidráulicas comunes.

**Duración estimada**: 4-5 días

**Tareas**:
- [ ] Alcantarillas:
  - Flujo con control de entrada
  - Flujo con control de salida
  - Sumergencia
- [ ] Vertederos:
  - Rectangular
  - Triangular
  - Trapezoidal
  - Creager
- [ ] Orificios
- [ ] Transiciones
- [ ] Disipadores de energía

**Entregables**:
- Calculadoras para cada tipo de estructura
- Tablas de coeficientes
- Diagramas y esquemas
- Recomendaciones de diseño

### FASE 7: Análisis de Redes 📅 FUTURA
**Objetivo**: Cálculo de redes de alcantarillado.

**Duración estimada**: 7-10 días

**Tareas**:
- [ ] Modelo de nodos y tramos
- [ ] Cálculo hidráulico de redes
- [ ] Routing en redes
- [ ] Balance de caudales
- [ ] Verificación de capacidad
- [ ] Optimización de diámetros
- [ ] Visualización de red

### FASE 8: Características Avanzadas 📅 FUTURA
**Objetivo**: Funcionalidades profesionales.

**Duración estimada**: 10-15 días

**Tareas**:
- [ ] Sistema de usuarios y autenticación
- [ ] Proyectos guardados
- [ ] Base de datos (SQLite/PostgreSQL)
- [ ] Generación de reportes PDF
- [ ] Exportación a CAD (DXF)
- [ ] Importación de topografía
- [ ] Procesamiento de archivos Excel
- [ ] Comparación de escenarios
- [ ] Histórico de cálculos

---

## 📊 Métricas de Progreso

### Estado Actual
- ✅ Fases completadas: 0/8
- 🔄 Fase en progreso: Fase 1 (MVP)
- 📈 Progreso general: ~5%

### Funcionalidades Implementadas
- [x] Estructura del proyecto
- [x] Documentación inicial
- [ ] Método Racional
- [ ] Tormentas de diseño
- [ ] Hidrogramas
- [ ] GVF
- [ ] Canales
- [ ] Estructuras

---

## 🎯 Prioridades

### Corto Plazo (1-2 semanas)
1. Completar FASE 1: MVP funcional
2. Comenzar FASE 2: Tormentas de diseño
3. Crear tests para método racional

### Mediano Plazo (1-2 meses)
1. Completar FASES 2-4
2. Implementar exportación de resultados
3. Mejorar visualizaciones con gráficos

### Largo Plazo (3-6 meses)
1. Completar FASES 5-6
2. Comenzar análisis de redes
3. Sistema de proyectos guardados

---

## 🔧 Decisiones Técnicas

### Stack Tecnológico
- **Framework**: FastAPI ✅
  - Razón: Simple, rápido, documentación automática
  - Alternativa considerada: Django (demasiado complejo para el proyecto)
  
- **Frontend**: HTML/CSS/JS Vanilla ✅
  - Razón: Simplicidad, sin dependencias pesadas
  - Futuro: Posible migración a React para interfaz más compleja

- **Cálculos**: NumPy + SciPy ✅
  - Razón: Estándar en computación científica Python
  
- **Base de Datos**: 
  - Corto plazo: JSON files
  - Mediano plazo: SQLite
  - Largo plazo: PostgreSQL (si es necesario)

### Patrones de Diseño
- **Separación de responsabilidades**: Core (cálculos) separado de API
- **Validación en capas**: Frontend + Backend (Pydantic)
- **API RESTful**: Endpoints descriptivos y consistentes

---

## 📚 Recursos Necesarios

### Datos de Referencia a Recopilar
- [ ] Curvas IDF de Uruguay (Montevideo, Canelones, Maldonado)
- [ ] Coeficientes de rugosidad ampliados
- [ ] Valores de CN por tipo de suelo y cobertura
- [ ] Coeficientes de escorrentía por superficie

### Bibliografía
- [x] Ven Te Chow - Applied Hydrology
- [x] Ven Te Chow - Open Channel Hydraulics
- [ ] Manual de Carreteras (Volumen de Drenaje)
- [ ] Normas UNIT (Uruguay) relacionadas

### Validación
- [ ] Casos de prueba calculados manualmente
- [ ] Comparación con software existente (HEC-HMS, HEC-RAS)
- [ ] Revisión por otros ingenieros

---

## ⚠️ Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Fórmulas incorrectas | Media | Alto | Tests extensivos, validación con casos conocidos |
| Conversión de unidades errónea | Media | Alto | Usar convención clara, tests unitarios |
| Interfaz confusa | Baja | Medio | Testing con usuarios, iteración de diseño |
| Performance lenta | Baja | Medio | Optimización si es necesario, cache |
| Datos de referencia incompletos | Alta | Medio | Comenzar con datos básicos, expandir gradualmente |

---

## 🎓 Aprendizajes y Mejoras

### Durante el Desarrollo
- Documentar decisiones importantes
- Mantener changelog actualizado
- Crear ejemplos de uso
- Escribir tests desde el principio

### Para el Futuro
- Considerar internacionalización (inglés/español)
- API pública para integraciones
- Versión móvil nativa
- Integración con GIS

---

## 📝 Notas

- Priorizar funcionalidad sobre perfección estética
- Cada módulo debe ser probado antes de pasar al siguiente
- Mantener código simple y legible
- Documentar referencias bibliográficas en el código

---

**Última actualización**: Noviembre 2025  
**Próxima revisión**: Al completar FASE 1