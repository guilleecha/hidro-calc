/**
 * Dashboard Charts Initialization
 * Renders charts when DOM is loaded using data from Django context
 */

document.addEventListener('DOMContentLoaded', function() {
    // Render Hyetograph if data is available
    if (typeof window.hyetographData !== 'undefined' && window.hyetographData) {
        if (window.hyetographData.time_steps && window.hyetographData.intensity) {
            renderHyetograph(
                window.hyetographData.time_steps,
                window.hyetographData.intensity,
                'hyetograph-chart',
                window.hyetographData.title || 'Hietograma - Distribución Temporal de Lluvia'
            );
        }
    }

    // Render Hydrographs Comparison if data is available
    if (typeof window.hydrographsData !== 'undefined' && window.hydrographsData) {
        if (Array.isArray(window.hydrographsData) && window.hydrographsData.length > 0) {
            renderHydrographComparison(
                window.hydrographsData,
                'hydrographs-chart',
                window.hydrographsTitle || 'Comparación de Hidrogramas'
            );
        }
    }
});
