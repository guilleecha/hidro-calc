/**
 * rational.js - Lógica para el Método Racional
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo Método Racional cargado');

    // Referencias a elementos del DOM
    const form = document.getElementById('rationalForm');
    const calculateBtn = document.getElementById('calculateBtn');
    const showCoefficientsBtn = document.getElementById('showCoefficients');
    const coefficientsTable = document.getElementById('coefficientsTable');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsContent = document.getElementById('resultsContent');

    // ===== CARGAR COEFICIENTES DE REFERENCIA =====
    async function loadRunoffCoefficients() {
        try {
            const data = await fetchAPI('/api/runoff-coefficients');
            renderCoefficientsTable(data.coefficients);
        } catch (error) {
            console.error('Error cargando coeficientes:', error);
        }
    }

    // ===== RENDERIZAR TABLA DE COEFICIENTES =====
    function renderCoefficientsTable(coefficients) {
        const tbody = document.getElementById('coefficientsBody');
        tbody.innerHTML = '';

        Object.entries(coefficients).forEach(([key, data]) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${data.descripcion}</td>
                <td>${data.min}</td>
                <td><strong>${data.tipico}</strong></td>
                <td>${data.max}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // ===== MOSTRAR/OCULTAR TABLA DE COEFICIENTES =====
    if (showCoefficientsBtn) {
        showCoefficientsBtn.addEventListener('click', function() {
            if (coefficientsTable.style.display === 'none') {
                coefficientsTable.style.display = 'block';
                showCoefficientsBtn.textContent = '❌ Ocultar tabla de coeficientes';
                loadRunoffCoefficients();
            } else {
                coefficientsTable.style.display = 'none';
                showCoefficientsBtn.textContent = '📋 Ver tabla de coeficientes típicos';
            }
        });
    }

    // ===== VALIDACIÓN DEL FORMULARIO =====
    function validateForm() {
        clearErrors();

        let isValid = true;

        // Validar C
        const C = document.getElementById('C').value;
        const errorC = validateNumber(C, 0, 1, 'Coeficiente C');
        if (errorC) {
            showError('C', errorC);
            isValid = false;
        }

        // Validar I
        const I_mmh = document.getElementById('I_mmh').value;
        const errorI = validateNumber(I_mmh, 0, 1000, 'Intensidad I');
        if (errorI) {
            showError('I_mmh', errorI);
            isValid = false;
        }

        // Validar A
        const A_ha = document.getElementById('A_ha').value;
        const errorA = validateNumber(A_ha, 0, 100000, 'Área A');
        if (errorA) {
            showError('A_ha', errorA);
            isValid = false;
        }

        return isValid;
    }

    // ===== ENVIAR FORMULARIO =====
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            if (!validateForm()) {
                return;
            }

            // Obtener datos del formulario
            const formData = {
                C: parseFloat(document.getElementById('C').value),
                I_mmh: parseFloat(document.getElementById('I_mmh').value),
                A_ha: parseFloat(document.getElementById('A_ha').value),
                description: document.getElementById('description').value || ''
            };

            console.log('Enviando datos:', formData);

            // Mostrar loader
            showButtonLoader(calculateBtn, true);

            try {
                // Llamar a la API
                const result = await fetchAPI('/api/rational', {
                    method: 'POST',
                    body: JSON.stringify(formData)
                });

                console.log('Resultado:', result);

                // Mostrar resultados
                displayResults(result);

            } catch (error) {
                console.error('Error:', error);
                alert(`Error al calcular: ${error.message}`);
            } finally {
                showButtonLoader(calculateBtn, false);
            }
        });
    }

    // ===== MOSTRAR RESULTADOS =====
    function displayResults(data) {
        // Ocultar mensaje vacío y mostrar contenido
        resultsContainer.style.display = 'none';
        resultsContent.style.display = 'block';

        // Caudales
        document.getElementById('result-Q-ls').textContent = formatNumber(data.Q_ls, 2);
        document.getElementById('result-Q-m3s').textContent = formatNumber(data.Q_m3s, 4);
        document.getElementById('result-Q-m3h').textContent = formatNumber(data.Q_m3h, 2);

        // Datos de entrada
        document.getElementById('result-input-C').textContent = data.inputs.C;
        document.getElementById('result-input-I').textContent = `${data.inputs.I_mmh} mm/h`;
        document.getElementById('result-input-A-ha').textContent = `${data.inputs.A_ha} ha`;
        document.getElementById('result-input-A-m2').textContent = formatNumber(data.inputs.A_m2, 0);

        // Advertencias
        const warningsContainer = document.getElementById('warningsContainer');
        const warningsList = document.getElementById('warningsList');

        if (data.warnings && data.warnings.length > 0) {
            warningsList.innerHTML = '';
            data.warnings.forEach(warning => {
                const li = document.createElement('li');
                li.textContent = warning;
                warningsList.appendChild(li);
            });
            warningsContainer.style.display = 'block';
        } else {
            warningsContainer.style.display = 'none';
        }

        // Descripción
        const descriptionContainer = document.getElementById('descriptionContainer');
        const descriptionText = document.getElementById('result-description');

        if (data.description && data.description.trim() !== '') {
            descriptionText.textContent = data.description;
            descriptionContainer.style.display = 'block';
        } else {
            descriptionContainer.style.display = 'none';
        }

        // Scroll suave a resultados
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // ===== LIMPIAR FORMULARIO =====
    form.addEventListener('reset', function() {
        clearErrors();
        resultsContainer.style.display = 'block';
        resultsContent.style.display = 'none';
    });

    // ===== VALIDACIÓN EN TIEMPO REAL =====
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            // Validar solo el campo que perdió el foco
            const fieldId = this.id;
            const value = this.value;

            let error = null;

            if (fieldId === 'C') {
                error = validateNumber(value, 0, 1, 'Coeficiente C');
            } else if (fieldId === 'I_mmh') {
                error = validateNumber(value, 0, 1000, 'Intensidad I');
            } else if (fieldId === 'A_ha') {
                error = validateNumber(value, 0, 100000, 'Área A');
            }

            // Limpiar error previo del campo
            const errorDiv = document.getElementById(`error-${fieldId}`);
            if (errorDiv) {
                errorDiv.textContent = '';
                errorDiv.classList.remove('active');
            }
            this.classList.remove('error');

            // Mostrar nuevo error si existe
            if (error) {
                showError(fieldId, error);
            }
        });
    });
});
