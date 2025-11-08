// App principal - Manejo del formulario y comunicación con API

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('rational-form');
    const resultsCard = document.getElementById('results');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Event listener del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Obtener valores del formulario
        const C = parseFloat(document.getElementById('C').value);
        const I = parseFloat(document.getElementById('I').value);
        const A = parseFloat(document.getElementById('A').value);

        // Validación básica frontend
        if (!validateInputs(C, I, A)) {
            return;
        }

        // Deshabilitar botón durante cálculo
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculando...';

        try {
            // Llamada a la API
            const response = await fetch('/api/calculate-rational', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ C, I_mmh: I, A_ha: A })
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
            // Rehabilitar botón
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calcular Caudal';
        }
    });

    // Función de validación
    function validateInputs(C, I, A) {
        if (isNaN(C) || C < 0 || C > 1) {
            alert('El coeficiente C debe estar entre 0 y 1');
            return false;
        }

        if (isNaN(I) || I <= 0) {
            alert('La intensidad debe ser mayor a 0');
            return false;
        }

        if (I > 500) {
            if (!confirm('La intensidad parece muy alta (>500 mm/h). ¿Continuar?')) {
                return false;
            }
        }

        if (isNaN(A) || A <= 0) {
            alert('El área debe ser mayor a 0');
            return false;
        }

        return true;
    }

    // Función para mostrar resultados
    function displayResults(result) {
        // Actualizar valores
        document.getElementById('Q-ls').textContent = result.Q_ls.toFixed(2);
        document.getElementById('Q-m3s').textContent = result.Q_m3s.toFixed(4);
        document.getElementById('result-C').textContent = result.inputs.C;
        document.getElementById('result-I').textContent = result.inputs.I_mmh;
        document.getElementById('result-A').textContent = result.inputs.A_ha;

        // Mostrar card de resultados con animación
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
