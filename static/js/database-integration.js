/**
 * database-integration.js
 * Funciones para integrar el frontend con la API de base de datos
 */

// Estado global para el contexto actual
const DBContext = {
    currentProject: null,
    currentWatershed: null,
    currentDesignStorm: null
};

// ============================================================================
// FUNCIONES DE CARGA DE DATOS
// ============================================================================

/**
 * Cargar todos los proyectos desde la API
 */
async function loadProjects() {
    try {
        const projects = await fetchAPI('/api/v1/projects');
        console.log('Proyectos cargados:', projects);
        return projects;
    } catch (error) {
        console.error('Error cargando proyectos:', error);
        showNotification('Error al cargar proyectos', 'error');
        return [];
    }
}

/**
 * Cargar cuencas de un proyecto específico
 */
async function loadWatersheds(projectId) {
    try {
        const watersheds = await fetchAPI(`/api/v1/projects/${projectId}/watersheds`);
        console.log('Cuencas cargadas:', watersheds);
        return watersheds;
    } catch (error) {
        console.error('Error cargando cuencas:', error);
        showNotification('Error al cargar cuencas', 'error');
        return [];
    }
}

/**
 * Cargar tormentas de diseño de una cuenca específica
 */
async function loadDesignStorms(watershedId) {
    try {
        const storms = await fetchAPI(`/api/v1/watersheds/${watershedId}/design-storms`);
        console.log('Tormentas cargadas:', storms);
        return storms;
    } catch (error) {
        console.error('Error cargando tormentas:', error);
        showNotification('Error al cargar tormentas de diseño', 'error');
        return [];
    }
}

// ============================================================================
// FUNCIONES DE POBLACIÓN DE SELECTORES
// ============================================================================

/**
 * Poblar el selector de proyectos
 */
async function populateProjectSelect(selectId = 'projectSelect') {
    const select = document.getElementById(selectId);
    if (!select) return;

    // Limpiar opciones existentes excepto la primera
    select.innerHTML = '<option value="">-- Seleccionar Proyecto Existente --</option>';

    const projects = await loadProjects();

    projects.forEach(project => {
        const option = document.createElement('option');
        option.value = project.id;
        option.textContent = project.name;
        option.dataset.project = JSON.stringify(project);
        select.appendChild(option);
    });

    // Agregar opción para crear nuevo
    const newOption = document.createElement('option');
    newOption.value = 'new';
    newOption.textContent = '+ Crear Nuevo Proyecto';
    newOption.style.fontWeight = 'bold';
    select.appendChild(newOption);
}

/**
 * Poblar el selector de cuencas
 */
async function populateWatershedSelect(projectId, selectId = 'watershedSelect') {
    const select = document.getElementById(selectId);
    if (!select) return;

    // Limpiar opciones
    select.innerHTML = '<option value="">-- Seleccionar Cuenca --</option>';
    select.disabled = !projectId || projectId === 'new';

    if (!projectId || projectId === 'new') {
        return;
    }

    const watersheds = await loadWatersheds(projectId);

    watersheds.forEach(watershed => {
        const option = document.createElement('option');
        option.value = watershed.id;
        option.textContent = `${watershed.name} (${watershed.area_hectareas} ha)`;
        option.dataset.watershed = JSON.stringify(watershed);
        select.appendChild(option);
    });

    // Agregar opción para crear nueva
    const newOption = document.createElement('option');
    newOption.value = 'new';
    newOption.textContent = '+ Crear Nueva Cuenca';
    newOption.style.fontWeight = 'bold';
    select.appendChild(newOption);
}

// ============================================================================
// FUNCIONES DE POBLACIÓN DE FORMULARIO
// ============================================================================

/**
 * Poblar el formulario con datos de una cuenca
 */
function populateFormFromWatershed(watershed) {
    if (!watershed) return;

    console.log('Poblando formulario con cuenca:', watershed);
    DBContext.currentWatershed = watershed;

    // Poblar área de la cuenca
    const areaInput = document.getElementById('A_ha');
    if (areaInput && watershed.area_hectareas) {
        areaInput.value = watershed.area_hectareas;
    }

    // Poblar coeficiente de escorrentía si existe
    const cInput = document.getElementById('C');
    if (cInput && watershed.c_racional) {
        cInput.value = watershed.c_racional;
    }

    // Poblar tiempo de concentración si existe
    const tcInput = document.getElementById('tc_horas');
    if (tcInput && watershed.tc_horas) {
        tcInput.value = watershed.tc_horas;
    }

    // Mostrar información de la cuenca
    showWatershedInfo(watershed);
}

/**
 * Mostrar información de la cuenca seleccionada
 */
function showWatershedInfo(watershed) {
    const infoDiv = document.getElementById('watershedInfo');
    if (!infoDiv) return;

    infoDiv.style.display = 'block';
    infoDiv.innerHTML = `
        <div class="info-box">
            <h4>📊 Información de la Cuenca</h4>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Nombre:</span>
                    <span class="info-value">${watershed.name}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Área:</span>
                    <span class="info-value">${watershed.area_hectareas} ha</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Tiempo de Concentración:</span>
                    <span class="info-value">${watershed.tc_horas} horas</span>
                </div>
                ${watershed.nc_scs ? `
                <div class="info-item">
                    <span class="info-label">Número de Curva (NC):</span>
                    <span class="info-value">${watershed.nc_scs}</span>
                </div>
                ` : ''}
                ${watershed.c_racional ? `
                <div class="info-item">
                    <span class="info-label">Coef. Escorrentía (C):</span>
                    <span class="info-value">${watershed.c_racional}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `;
}

/**
 * Limpiar información de la cuenca
 */
function clearWatershedInfo() {
    const infoDiv = document.getElementById('watershedInfo');
    if (infoDiv) {
        infoDiv.style.display = 'none';
        infoDiv.innerHTML = '';
    }
}

// ============================================================================
// FUNCIONES DE CREACIÓN
// ============================================================================

/**
 * Crear un nuevo proyecto
 */
async function createProject(data) {
    try {
        const project = await fetchAPI('/api/v1/projects', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        console.log('Proyecto creado:', project);
        showNotification('Proyecto creado exitosamente', 'success');
        return project;
    } catch (error) {
        console.error('Error creando proyecto:', error);
        showNotification('Error al crear proyecto', 'error');
        throw error;
    }
}

/**
 * Crear una nueva cuenca
 */
async function createWatershed(projectId, data) {
    try {
        const watershed = await fetchAPI(`/api/v1/projects/${projectId}/watersheds`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        console.log('Cuenca creada:', watershed);
        showNotification('Cuenca creada exitosamente', 'success');
        return watershed;
    } catch (error) {
        console.error('Error creando cuenca:', error);
        showNotification('Error al crear cuenca', 'error');
        throw error;
    }
}

/**
 * Crear una tormenta de diseño
 */
async function createDesignStorm(watershedId, data) {
    try {
        const storm = await fetchAPI(`/api/v1/watersheds/${watershedId}/design-storms`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        console.log('Tormenta creada:', storm);
        return storm;
    } catch (error) {
        console.error('Error creando tormenta:', error);
        showNotification('Error al crear tormenta de diseño', 'error');
        throw error;
    }
}

// ============================================================================
// FUNCIONES DE GUARDADO DE HIDROGRAMAS
// ============================================================================

/**
 * Guardar hidrograma en la base de datos
 */
async function saveHydrographToDB(designStormId, hydrographData) {
    try {
        const hydrograph = await fetchAPI(`/api/v1/design-storms/${designStormId}/hydrographs`, {
            method: 'POST',
            body: JSON.stringify(hydrographData)
        });
        console.log('Hidrograma guardado:', hydrograph);
        showNotification('Hidrograma guardado en la base de datos', 'success');
        return hydrograph;
    } catch (error) {
        console.error('Error guardando hidrograma:', error);
        showNotification('Error al guardar hidrograma', 'error');
        throw error;
    }
}

// ============================================================================
// FUNCIONES AUXILIARES
// ============================================================================

/**
 * Mostrar notificación al usuario
 */
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Estilos inline para asegurar visibilidad
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
        color: white;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ============================================================================
// EVENTOS AL CARGAR LA PÁGINA
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Database Integration cargado');

    // Cargar proyectos al inicio
    const projectSelect = document.getElementById('projectSelect');
    if (projectSelect) {
        populateProjectSelect();

        // Event listener para cambio de proyecto
        projectSelect.addEventListener('change', function(e) {
            const projectId = e.target.value;
            DBContext.currentProject = projectId;
            clearWatershedInfo();

            if (projectId && projectId !== 'new') {
                populateWatershedSelect(projectId);
            } else if (projectId === 'new') {
                // Mostrar modal o formulario para crear nuevo proyecto
                alert('Funcionalidad de crear nuevo proyecto - Por implementar');
            }
        });
    }

    // Event listener para cambio de cuenca
    const watershedSelect = document.getElementById('watershedSelect');
    if (watershedSelect) {
        watershedSelect.addEventListener('change', function(e) {
            const option = e.target.options[e.target.selectedIndex];

            if (option.value === 'new') {
                // Mostrar modal o formulario para crear nueva cuenca
                alert('Funcionalidad de crear nueva cuenca - Por implementar');
            } else if (option.value) {
                const watershed = JSON.parse(option.dataset.watershed);
                populateFormFromWatershed(watershed);
            } else {
                clearWatershedInfo();
            }
        });
    }
});

// Exportar funciones para uso global
window.DBIntegration = {
    loadProjects,
    loadWatersheds,
    loadDesignStorms,
    populateFormFromWatershed,
    createProject,
    createWatershed,
    createDesignStorm,
    saveHydrographToDB,
    DBContext
};
