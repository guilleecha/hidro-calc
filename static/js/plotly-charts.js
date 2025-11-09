/**
 * Plotly Charts for HidroStudio Professional
 * Functions to render interactive hydrological charts
 */

// Color palette for charts
const CHART_COLORS = {
    primary: '#2563eb',
    secondary: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    purple: '#8b5cf6',
    teal: '#14b8a6',
    methods: ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#14b8a6']
};

// Default layout configuration
const DEFAULT_LAYOUT = {
    plot_bgcolor: '#f9fafb',
    paper_bgcolor: 'white',
    font: {
        family: 'system-ui, -apple-system, sans-serif',
        size: 12,
        color: '#374151'
    },
    margin: { l: 60, r: 40, t: 60, b: 60 },
    hovermode: 'closest',
    showlegend: true,
    legend: {
        x: 1,
        y: 1,
        bgcolor: 'rgba(255,255,255,0.8)',
        bordercolor: '#e5e7eb',
        borderwidth: 1
    }
};

/**
 * Render Hyetograph (Rainfall Distribution)
 * @param {Array} timeSteps - Time in minutes [0, 5, 10, 15, ...]
 * @param {Array} intensity - Rainfall intensity in mm/h
 * @param {string} containerId - ID of the div container
 * @param {string} title - Chart title (optional)
 */
function renderHyetograph(timeSteps, intensity, containerId, title = 'Hietograma - Distribución Temporal de Lluvia') {
    const data = [{
        x: timeSteps,
        y: intensity,
        type: 'bar',
        name: 'Intensidad',
        marker: {
            color: CHART_COLORS.primary,
            line: {
                color: '#1e40af',
                width: 1
            }
        },
        hovertemplate: '<b>Tiempo:</b> %{x} min<br>' +
                       '<b>Intensidad:</b> %{y:.2f} mm/h<br>' +
                       '<extra></extra>'
    }];

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: title,
            font: { size: 16, weight: 600 }
        },
        xaxis: {
            title: 'Tiempo (minutos)',
            gridcolor: '#e5e7eb',
            zeroline: false
        },
        yaxis: {
            title: 'Intensidad (mm/h)',
            gridcolor: '#e5e7eb',
            zeroline: false
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    Plotly.newPlot(containerId, data, layout, config);
}

/**
 * Render Single Hydrograph
 * @param {Array} timeSteps - Time in minutes
 * @param {Array} discharge - Discharge in m³/s
 * @param {string} containerId - ID of the div container
 * @param {string} method - Method name (e.g., "Racional", "SCS")
 * @param {string} title - Chart title (optional)
 */
function renderHydrograph(timeSteps, discharge, containerId, method = 'Hidrograma', title = 'Hidrograma de Caudal') {
    const data = [{
        x: timeSteps,
        y: discharge,
        type: 'scatter',
        mode: 'lines',
        name: method,
        line: {
            color: CHART_COLORS.primary,
            width: 3
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(37, 99, 235, 0.1)',
        hovertemplate: '<b>Tiempo:</b> %{x} min<br>' +
                       '<b>Caudal:</b> %{y:.2f} m³/s<br>' +
                       '<extra></extra>'
    }];

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: title,
            font: { size: 16, weight: 600 }
        },
        xaxis: {
            title: 'Tiempo (minutos)',
            gridcolor: '#e5e7eb',
            zeroline: false
        },
        yaxis: {
            title: 'Caudal (m³/s)',
            gridcolor: '#e5e7eb',
            zeroline: false
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    Plotly.newPlot(containerId, data, layout, config);
}

/**
 * Render Hydrograph Comparison (Multiple Methods)
 * @param {Array} hydrographs - Array of hydrograph objects
 *   Example: [{
 *     name: "Método Racional",
 *     time_steps: [0, 5, 10, ...],
 *     discharge: [0, 2.5, 5.8, ...]
 *   }, ...]
 * @param {string} containerId - ID of the div container
 * @param {string} title - Chart title (optional)
 */
function renderHydrographComparison(hydrographs, containerId, title = 'Comparación de Hidrogramas') {
    const data = hydrographs.map((hydro, index) => ({
        x: hydro.time_steps,
        y: hydro.discharge,
        type: 'scatter',
        mode: 'lines',
        name: hydro.name,
        line: {
            width: 2.5,
            color: CHART_COLORS.methods[index % CHART_COLORS.methods.length]
        },
        hovertemplate: '<b>' + hydro.name + '</b><br>' +
                       'Tiempo: %{x} min<br>' +
                       'Caudal: %{y:.2f} m³/s<br>' +
                       '<extra></extra>'
    }));

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: title,
            font: { size: 16, weight: 600 }
        },
        xaxis: {
            title: 'Tiempo (minutos)',
            gridcolor: '#e5e7eb',
            zeroline: false
        },
        yaxis: {
            title: 'Caudal (m³/s)',
            gridcolor: '#e5e7eb',
            zeroline: false
        },
        hovermode: 'x unified',
        legend: {
            ...DEFAULT_LAYOUT.legend,
            orientation: 'h',
            y: -0.2,
            x: 0.5,
            xanchor: 'center'
        }
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    Plotly.newPlot(containerId, data, layout, config);
}

/**
 * Generate sample hyetograph data (Alternating Block Method)
 * This is a helper function for testing
 * @param {number} duration - Storm duration in hours
 * @param {number} totalRainfall - Total rainfall in mm
 * @param {number} interval - Time interval in minutes (default 5)
 * @returns {Object} - {timeSteps: Array, intensity: Array}
 */
function generateSampleHyetograph(duration = 2, totalRainfall = 85, interval = 5) {
    const numIntervals = Math.floor((duration * 60) / interval);
    const timeSteps = [];
    const intensity = [];

    // Simple alternating block pattern (peak in the middle)
    const peakIndex = Math.floor(numIntervals / 2);

    for (let i = 0; i < numIntervals; i++) {
        timeSteps.push(i * interval);

        // Distance from peak
        const distFromPeak = Math.abs(i - peakIndex);
        // Intensity decreases with distance from peak
        const relativeIntensity = 1 - (distFromPeak / numIntervals);
        const intensityValue = (totalRainfall / duration) * (1 + relativeIntensity);

        intensity.push(intensityValue);
    }

    return { timeSteps, intensity };
}

/**
 * Generate sample hydrograph data (Triangular shape)
 * This is a helper function for testing
 * @param {number} peakDischarge - Peak discharge in m³/s
 * @param {number} timeToPeak - Time to peak in minutes
 * @param {number} baseTime - Total base time in minutes
 * @param {number} interval - Time interval in minutes (default 5)
 * @returns {Object} - {timeSteps: Array, discharge: Array}
 */
function generateSampleHydrograph(peakDischarge = 15, timeToPeak = 45, baseTime = 180, interval = 5) {
    const timeSteps = [];
    const discharge = [];

    for (let t = 0; t <= baseTime; t += interval) {
        timeSteps.push(t);

        let q = 0;
        if (t <= timeToPeak) {
            // Rising limb
            q = (peakDischarge / timeToPeak) * t;
        } else {
            // Falling limb
            const timeFromPeak = t - timeToPeak;
            const fallingTime = baseTime - timeToPeak;
            q = peakDischarge * (1 - (timeFromPeak / fallingTime));
        }

        discharge.push(Math.max(0, q));
    }

    return { timeSteps, discharge };
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        renderHyetograph,
        renderHydrograph,
        renderHydrographComparison,
        generateSampleHyetograph,
        generateSampleHydrograph
    };
}
