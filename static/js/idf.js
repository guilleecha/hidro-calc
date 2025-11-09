/**
 * idf.js - Lógica para Curvas IDF Uruguay
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Módulo Curvas IDF cargado');

    // Referencias a elementos del DOM
    const form = document.getElementById('idfForm');
    const calculateBtn = document.getElementById('calculateBtn');
    const citySelect = document.getElementById('city');
    const P3_10Input = document.getElementById('P3_10');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsContent = document.getElementById('resultsContent');

    // ===== SELECTOR DE CIUDAD =====
    if (citySelect) {
        citySelect.addEventListener('change', function() {
            const selectedValue = this.value;
            if (selectedValue) {
                P3_10Input.value = selectedValue;
            }
        });
    }

    // ===== VALIDACIÓN DEL FORMULARIO =====
    function validateForm() {
        clearErrors();

        let isValid = true;

        // Validar P3_10
        const P3_10 = document.getElementById('P3_10').value;
        const errorP3_10 = validateNumber(P3_10, 50, 100, 'P₃,₁₀');
        if (errorP3_10) {
            showError('P3_10', errorP3_10);
            isValid = false;
        }

        // Validar Tr
        const Tr = document.getElementById('Tr').value;
        const errorTr = validateNumber(Tr, 2, 500, 'Período de retorno');
        if (errorTr) {
            showError('Tr', errorTr);
            isValid = false;
        }

        // Validar d
        const d = document.getElementById('d').value;
        const errorD = validateNumber(d, 0.1, 48, 'Duración');
        if (errorD) {
            showError('d', errorD);
            isValid = false;
        }

        // Validar Ac (opcional)
        const Ac = document.getElementById('Ac').value;
        if (Ac && Ac.trim() !== '') {
            const errorAc = validateNumber(Ac, 0, 1000, 'Área cuenca');
            if (errorAc) {
                showError('Ac', errorAc);
                isValid = false;
            }
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
            const P3_10 = parseFloat(document.getElementById('P3_10').value);
            const Tr = parseFloat(document.getElementById('Tr').value);
            const d = parseFloat(document.getElementById('d').value);
            const AcValue = document.getElementById('Ac').value;
            const Ac = AcValue && AcValue.trim() !== '' ? parseFloat(AcValue) : null;

            const formData = {
                P3_10: P3_10,
                Tr: Tr,
                d: d
            };

            if (Ac !== null) {
                formData.Ac = Ac;
            }

            console.log('Enviando datos:', formData);

            // Mostrar loader
            showButtonLoader(calculateBtn, true);

            try {
                // Llamar a la API
                const result = await fetchAPI('/calculators/api/idf/calculate', {
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

        // Intensidad y Precipitación
        document.getElementById('result-I-mmh').textContent = formatNumber(data.I_mmh, 4);
        document.getElementById('result-P-mm').textContent = formatNumber(data.P_mm, 4);

        // Factores de corrección
        document.getElementById('result-CT').textContent = formatNumber(data.CT, 4);
        document.getElementById('result-CD').textContent = formatNumber(data.CD, 4);
        document.getElementById('result-CA').textContent = formatNumber(data.CA, 4);

        // Parámetros de entrada
        document.getElementById('result-input-P3_10').textContent = data.P3_10;
        document.getElementById('result-input-Tr').textContent = data.Tr;
        document.getElementById('result-input-d').textContent = data.d_hours;

        const acElement = document.getElementById('result-input-Ac');
        if (data.Ac_km2 !== null) {
            acElement.textContent = `${data.Ac_km2} km²`;
        } else {
            acElement.textContent = 'Sin corrección (intensidad puntual)';
        }

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

        // Scroll suave a resultados
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // ===== LIMPIAR FORMULARIO =====
    form.addEventListener('reset', function() {
        clearErrors();
        resultsContainer.style.display = 'block';
        resultsContent.style.display = 'none';

        // Resetear selector de ciudad
        if (citySelect) {
            citySelect.selectedIndex = 0;
        }
    });

    // ===== VALIDACIÓN EN TIEMPO REAL =====
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            // Validar solo el campo que perdió el foco
            const fieldId = this.id;
            const value = this.value;

            // No validar si está vacío y es opcional (solo Ac)
            if (fieldId === 'Ac' && (!value || value.trim() === '')) {
                return;
            }

            let error = null;
            let min, max, fieldName;

            switch(fieldId) {
                case 'P3_10':
                    error = validateNumber(value, 50, 100, 'P₃,₁₀');
                    break;
                case 'Tr':
                    error = validateNumber(value, 2, 500, 'Período de retorno');
                    break;
                case 'd':
                    error = validateNumber(value, 0.1, 48, 'Duración');
                    break;
                case 'Ac':
                    error = validateNumber(value, 0, 1000, 'Área cuenca');
                    break;
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
