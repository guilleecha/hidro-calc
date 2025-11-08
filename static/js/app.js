/**
 * app.js - JavaScript principal de HidroCalc
 */

console.log('HidroCalc v1.0.0 - Cargado correctamente');

/**
 * Utility function para hacer peticiones HTTP
 */
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || data.detail || 'Error en la petición');
        }

        return data;
    } catch (error) {
        console.error('Error en fetchAPI:', error);
        throw error;
    }
}

/**
 * Muestra un mensaje de error en el formulario
 */
function showError(fieldId, message) {
    const errorDiv = document.getElementById(`error-${fieldId}`);
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.add('active');
    }

    const input = document.getElementById(fieldId);
    if (input) {
        input.classList.add('error');
    }
}

/**
 * Limpia todos los errores del formulario
 */
function clearErrors() {
    const errorDivs = document.querySelectorAll('.form-error');
    errorDivs.forEach(div => {
        div.textContent = '';
        div.classList.remove('active');
    });

    const inputs = document.querySelectorAll('.form-input.error');
    inputs.forEach(input => {
        input.classList.remove('error');
    });
}

/**
 * Valida un número en un rango
 */
function validateNumber(value, min, max, fieldName) {
    const num = parseFloat(value);

    if (isNaN(num)) {
        return `${fieldName} debe ser un número válido`;
    }

    if (min !== undefined && num < min) {
        return `${fieldName} debe ser mayor o igual a ${min}`;
    }

    if (max !== undefined && num > max) {
        return `${fieldName} debe ser menor o igual a ${max}`;
    }

    return null;
}

/**
 * Formatea un número con separadores de miles
 */
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return '-';
    return num.toLocaleString('es-UY', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

/**
 * Muestra un loader en un botón
 */
function showButtonLoader(button, show = true) {
    if (show) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="loading"></span> Calculando...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || 'Calcular';
    }
}
