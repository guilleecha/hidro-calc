# 📋 Sistema de Contexto de Proyecto

Este directorio contiene el **estado actualizado del proyecto** para facilitar el inicio de nuevas sesiones de trabajo.

---

## 🎯 Propósito

Cuando comiences una nueva sesión de trabajo con Claude Code:
1. Lee primero `CLAUDE.md` en la raíz del proyecto
2. CLAUDE.md te dirigirá a leer `current_session.md`
3. Esto te dará contexto completo de:
   - ✅ Lo que ya está hecho
   - 🔄 Lo que está en progreso
   - ⏳ Lo que falta por hacer
   - 🏗️ Arquitectura actual del proyecto

---

## 📁 Estructura de Archivos

### **`current_session.md`** ⭐ (LEER PRIMERO)
Estado actual del proyecto al finalizar la última sesión:
- Última tarea completada
- Estado de la base de datos
- Servidor corriendo o no
- Problemas conocidos
- Contexto inmediato para continuar

### **`completed_tasks.md`**
Lista completa de tareas completadas organizadas por sesión:
- Sesión 1: Implementación de BD con FastAPI
- Sesión 2: Migración a Django
- Sesión 3: MCP Servers
- etc.

### **`next_steps.md`**
Próximos pasos priorizados:
- Alta prioridad (hacer ahora)
- Media prioridad (hacer pronto)
- Baja prioridad (backlog)

### **`architecture_overview.md`**
Overview de la arquitectura actual:
- Stack tecnológico
- Estructura de carpetas
- Modelos de base de datos
- APIs disponibles
- Flujos principales

---

## 🔄 Workflow de Sesiones

### **Al COMENZAR una sesión:**
```
1. Leer CLAUDE.md (raíz del proyecto)
2. Leer context/current_session.md
3. Revisar context/next_steps.md
4. Continuar trabajo
```

### **Al FINALIZAR una sesión:**
```
1. Actualizar context/current_session.md con:
   - Última tarea completada
   - Estado actual del sistema
   - Problemas encontrados
   - Siguiente tarea sugerida

2. Actualizar context/completed_tasks.md con:
   - Tareas completadas en esta sesión
   - Número de sesión
   - Fecha

3. Actualizar context/next_steps.md:
   - Remover tareas completadas
   - Agregar nuevas tareas descubiertas
   - Repriorizar si es necesario

4. Si hubo cambios arquitectónicos:
   - Actualizar context/architecture_overview.md
```

---

## ⚡ Inicio Rápido

**Para Claude Code al comenzar sesión:**

1. **Leer contexto:**
   ```bash
   cat context/current_session.md
   ```

2. **Ver próximos pasos:**
   ```bash
   cat context/next_steps.md
   ```

3. **Verificar estado del proyecto:**
   ```bash
   python manage.py showmigrations
   python manage.py runserver  # si es necesario
   ```

---

## 📊 Beneficios

- ✅ **No perder contexto** entre sesiones
- ✅ **Inicio rápido** sin necesidad de recordar todo
- ✅ **Tracking claro** de progreso
- ✅ **Evitar duplicación** de trabajo
- ✅ **Decisiones documentadas** para referencia futura

---

**Última actualización:** 2025-11-08
