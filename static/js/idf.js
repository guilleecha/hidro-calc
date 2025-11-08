/**
 * idf.js - Lógica del frontend para el módulo de Curvas IDF de Uruguay
 *
 * Maneja la interacción del usuario con el formulario de cálculo de intensidades
 * de lluvia y la comunicación con la API backend.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('idf-form');
    const resultsCard = document.getElementById('results');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Manejo de Tr personalizado
    const trRadios = document.querySelectorAll('input[name="Tr"]');
    const trCustomInput = document.getElementById('Tr-custom');

    trRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'custom') {
                trCustomInput.style.display = 'block';
                trCustomInput.required = true;
                trCustomInput.focus();
            } else {
                trCustomInput.style.display = 'none';
                trCustomInput.required = false;
                trCustomInput.value = '';
            }
        });
    });

    // Submit del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Obtener valores
        const P3_10 = parseFloat(document.getElementById('P3_10').value);

        // Determinar Tr
        let Tr;
        const selectedTr = document.querySelector('input[name="Tr"]:checked');
        if (selectedTr.value === 'custom') {
            Tr = parseFloat(trCustomInput.value);
            if (!Tr || isNaN(Tr)) {
                alert('Por favor, ingrese un período de retorno personalizado válido');
                trCustomInput.focus();
                return;
            }
        } else {
            Tr = parseFloat(selectedTr.value);
        }

        const d = parseFloat(document.getElementById('d').value);
        const AcInput = document.getElementById('Ac').value;
        const Ac = AcInput ? parseFloat(AcInput) : null;

        // Validaciones básicas
        if (!validateInputs(P3_10, Tr, d, Ac)) {
            return;
        }

        // Deshabilitar botón
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculando...';

        try {
            // Preparar datos
            const requestData = {
                P3_10: P3_10,
                Tr: Tr,
                d: d
            };

            if (Ac !== null) {
                requestData.Ac = Ac;
            }

            // Llamada a la API
            const response = await fetch('/api/calculate-idf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error en el cálculo');
            }

            const result = await response.json();

            // Mostrar resultados
            displayResults(result);

        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error('Error:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calcular Intensidad';
        }
    });

    /**
     * Valida los datos de entrada antes de enviar al servidor
     */
    function validateInputs(P3_10, Tr, d, Ac) {
        // Validar P3_10
        if (isNaN(P3_10) || P3_10 < 50 || P3_10 > 100) {
            alert('P₃,₁₀ debe estar entre 50 y 100 mm');
            document.getElementById('P3_10').focus();
            return false;
        }

        // Validar Tr
        if (isNaN(Tr) || Tr < 2) {
            alert('El período de retorno debe ser mayor o igual a 2 años');
            return false;
        }

        if (Tr > 100) {
            if (!confirm('Período de retorno muy alto (>100 años). Las ecuaciones fueron calibradas hasta Tr=100. ¿Continuar de todas formas?')) {
                return false;
            }
        }

        // Validar duración
        if (isNaN(d) || d <= 0) {
            alert('La duración debe ser mayor a 0');
            document.getElementById('d').focus();
            return false;
        }

        if (d > 24) {
            if (!confirm('Duración mayor a 24 horas. ¿Continuar?')) {
                return false;
            }
        }

        // Validar área (si se proporciona)
        if (Ac !== null) {
            if (isNaN(Ac) || Ac < 0) {
                alert('El área de cuenca debe ser mayor o igual a 0');
                document.getElementById('Ac').focus();
                return false;
            }

            if (Ac > 300) {
                if (!confirm('Área de cuenca muy grande (>300 km²). ¿Continuar?')) {
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * Muestra los resultados en la interfaz
     */
    function displayResults(result) {
        // Valores principales
        document.getElementById('I-mmh').textContent = result.I_mmh.toFixed(2);
        document.getElementById('P-mm').textContent = result.P_mm.toFixed(2);

        // Factores
        document.getElementById('CT').textContent = result.CT.toFixed(4);
        document.getElementById('CD').textContent = result.CD.toFixed(4);
        document.getElementById('CA').textContent = result.CA.toFixed(4);

        // Datos de entrada
        document.getElementById('result-P3_10').textContent = result.P3_10;
        document.getElementById('result-Tr').textContent = result.Tr;
        document.getElementById('result-d').textContent = result.d_hours;
        document.getElementById('result-Ac').textContent =
            result.Ac_km2 !== null ? `${result.Ac_km2} km²` : 'Sin corrección (puntual)';

        // Mostrar card de resultados
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Manejo de tooltips (opcional)
     */
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('click', (e) => {
            e.preventDefault();
            const title = tooltip.getAttribute('title');
            if (title) {
                alert(title);
            }
        });
    });
});
