"""
Vistas para las calculadoras hidrológicas rápidas.
Sin login requerido, sin persistencia en BD.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .services.rational import (
    calculate_rational_flow_detailed,
    calculate_weighted_C,
    get_runoff_coefficients
)
from .services.idf import (
    calculate_intensity_idf,
    get_P3_10_reference_values,
    validate_inputs_and_warn
)


# ===== VISTAS DE TEMPLATES =====

def rational_calculator_view(request):
    """Vista para la calculadora de Método Racional."""
    context = {
        'title': 'Método Racional',
        'runoff_coefficients': get_runoff_coefficients()
    }
    return render(request, 'calculators/rational.html', context)


def idf_calculator_view(request):
    """Vista para la calculadora de Curvas IDF."""
    context = {
        'title': 'Curvas IDF Uruguay',
        'p3_10_values': get_P3_10_reference_values()
    }
    return render(request, 'calculators/idf.html', context)


# ===== API ENDPOINTS (JSON) =====

@csrf_exempt
@require_http_methods(["POST"])
def api_rational_calculate(request):
    """
    API para calcular caudal con Método Racional.

    POST /calculators/api/rational/calculate
    Body: {
        "C": 0.65,
        "I_mmh": 80,
        "A_ha": 5,
        "description": "Cuenca residencial" (opcional)
    }

    Returns: {
        "Q_ls": 722.22,
        "Q_m3s": 0.7222,
        "Q_m3h": 2600.0,
        "inputs": {...},
        "warnings": []
    }
    """
    try:
        data = json.loads(request.body)

        C = float(data.get('C'))
        I_mmh = float(data.get('I_mmh'))
        A_ha = float(data.get('A_ha'))
        description = data.get('description', '')

        result = calculate_rational_flow_detailed(
            C=C,
            I_mmh=I_mmh,
            A_ha=A_ha,
            description=description
        )

        return JsonResponse(result)

    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error en el cálculo: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_rational_weighted_c(request):
    """
    API para calcular coeficiente de escorrentía ponderado.

    POST /calculators/api/rational/weighted-c
    Body: {
        "surfaces": [
            {"area_ha": 2, "C": 0.90, "description": "Techos"},
            {"area_ha": 3, "C": 0.85, "description": "Pavimento"},
            {"area_ha": 5, "C": 0.20, "description": "Césped"}
        ]
    }

    Returns: {
        "C_weighted": 0.525,
        "total_area_ha": 10.0,
        "surfaces": [...]
    }
    """
    try:
        data = json.loads(request.body)
        surfaces = data.get('surfaces', [])

        if not surfaces:
            return JsonResponse({
                'error': 'Debe proporcionar al menos una superficie'
            }, status=400)

        # Extraer tuplas (area, C) para el cálculo
        areas_coefficients = [
            (float(s['area_ha']), float(s['C']))
            for s in surfaces
        ]

        C_weighted = calculate_weighted_C(areas_coefficients)
        total_area = sum(a[0] for a in areas_coefficients)

        # Calcular porcentajes
        surfaces_with_pct = []
        for s in surfaces:
            area = float(s['area_ha'])
            surfaces_with_pct.append({
                'area_ha': area,
                'C': float(s['C']),
                'description': s.get('description', ''),
                'percentage': round((area / total_area) * 100, 2)
            })

        result = {
            'C_weighted': round(C_weighted, 4),
            'total_area_ha': round(total_area, 4),
            'surfaces': surfaces_with_pct
        }

        return JsonResponse(result)

    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error en el cálculo: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_idf_calculate(request):
    """
    API para calcular intensidad con Curvas IDF.

    POST /calculators/api/idf/calculate
    Body: {
        "P3_10": 75,
        "Tr": 5,
        "d": 1,
        "Ac": 30 (opcional)
    }

    Returns: {
        "I_mmh": 36.34,
        "P_mm": 36.34,
        "CT": 0.8456,
        "CD": 0.5184,
        "CA": 0.9451,
        "warnings": []
    }
    """
    try:
        data = json.loads(request.body)

        P3_10 = float(data.get('P3_10'))
        Tr = float(data.get('Tr'))
        d = float(data.get('d'))
        Ac = data.get('Ac')
        if Ac is not None:
            Ac = float(Ac)

        # Validar y obtener warnings
        warnings = validate_inputs_and_warn(P3_10, Tr, d, Ac)

        # Calcular
        result = calculate_intensity_idf(
            P3_10=P3_10,
            Tr=Tr,
            d=d,
            Ac=Ac
        )

        # Agregar warnings al resultado
        result['warnings'] = warnings

        return JsonResponse(result)

    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error en el cálculo: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def api_runoff_coefficients(request):
    """
    API para obtener coeficientes de escorrentía de referencia.

    GET /calculators/api/runoff-coefficients

    Returns: {
        "techos": {
            "min": 0.75,
            "max": 0.95,
            "tipico": 0.85,
            "descripcion": "Techos de cualquier material"
        },
        ...
    }
    """
    coefficients = get_runoff_coefficients()
    return JsonResponse(coefficients)


@require_http_methods(["GET"])
def api_p3_10_values(request):
    """
    API para obtener valores de P3_10 de referencia.

    GET /calculators/api/p3-10-values

    Returns: {
        "Montevideo": 75.0,
        "La Paloma": 74.0,
        ...
    }
    """
    values = get_P3_10_reference_values()
    return JsonResponse(values)
