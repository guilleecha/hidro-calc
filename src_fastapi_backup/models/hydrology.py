"""
Modelos Pydantic para validación de datos hidrológicos.

Define las estructuras de datos de entrada y salida para los cálculos
hidrológicos, con validaciones automáticas.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class RationalMethodInput(BaseModel):
    """
    Modelo para los datos de entrada del Método Racional.

    Attributes:
        C: Coeficiente de escorrentía (0-1)
        I_mmh: Intensidad de lluvia en mm/h
        A_ha: Área de la cuenca en hectáreas
        description: Descripción opcional del cálculo
    """

    C: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Coeficiente de escorrentía (adimensional, 0-1)",
        examples=[0.65, 0.85]
    )

    I_mmh: float = Field(
        ...,
        gt=0.0,
        le=1000.0,
        description="Intensidad de lluvia en mm/h",
        examples=[80.0, 100.0]
    )

    A_ha: float = Field(
        ...,
        gt=0.0,
        le=100000.0,
        description="Área de la cuenca en hectáreas",
        examples=[5.0, 10.0]
    )

    description: Optional[str] = Field(
        default="",
        max_length=200,
        description="Descripción opcional del cálculo"
    )

    @field_validator('C')
    @classmethod
    def validate_runoff_coefficient(cls, v: float) -> float:
        """Valida que C esté en rango razonable."""
        if v < 0 or v > 1:
            raise ValueError('El coeficiente de escorrentía debe estar entre 0 y 1')
        return v

    @field_validator('I_mmh')
    @classmethod
    def validate_intensity(cls, v: float) -> float:
        """Valida que la intensidad sea positiva y razonable."""
        if v <= 0:
            raise ValueError('La intensidad de lluvia debe ser positiva')
        if v > 1000:
            raise ValueError(
                'Intensidad de lluvia muy alta (>1000 mm/h). '
                'Verifica el valor ingresado.'
            )
        return v

    @field_validator('A_ha')
    @classmethod
    def validate_area(cls, v: float) -> float:
        """Valida que el área sea positiva."""
        if v <= 0:
            raise ValueError('El área de la cuenca debe ser positiva')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "C": 0.65,
                    "I_mmh": 80.0,
                    "A_ha": 5.0,
                    "description": "Cuenca residencial mixta"
                },
                {
                    "C": 0.85,
                    "I_mmh": 100.0,
                    "A_ha": 10.0,
                    "description": "Zona comercial pavimentada"
                }
            ]
        }
    }


class RationalMethodOutput(BaseModel):
    """
    Modelo para los resultados del Método Racional.

    Attributes:
        Q_ls: Caudal en litros por segundo
        Q_m3s: Caudal en metros cúbicos por segundo
        Q_m3h: Caudal en metros cúbicos por hora
        inputs: Datos de entrada utilizados
        description: Descripción del cálculo
        warnings: Advertencias generadas (si las hay)
    """

    Q_ls: float = Field(
        ...,
        description="Caudal de diseño en L/s"
    )

    Q_m3s: float = Field(
        ...,
        description="Caudal de diseño en m³/s"
    )

    Q_m3h: float = Field(
        ...,
        description="Caudal de diseño en m³/h"
    )

    inputs: dict = Field(
        ...,
        description="Datos de entrada utilizados en el cálculo"
    )

    description: str = Field(
        default="",
        description="Descripción del cálculo"
    )

    warnings: List[str] = Field(
        default_factory=list,
        description="Advertencias generadas durante el cálculo"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Q_ls": 722.22,
                    "Q_m3s": 0.7222,
                    "Q_m3h": 2600.0,
                    "inputs": {
                        "C": 0.65,
                        "I_mmh": 80.0,
                        "A_ha": 5.0,
                        "A_m2": 50000.0,
                        "A_km2": 0.05
                    },
                    "description": "Cuenca residencial mixta",
                    "warnings": []
                }
            ]
        }
    }


class WeightedCInput(BaseModel):
    """
    Modelo para calcular coeficiente de escorrentía ponderado.

    Attributes:
        surfaces: Lista de superficies con área y coeficiente
    """

    surfaces: List[dict] = Field(
        ...,
        min_length=1,
        description="Lista de superficies con área_ha y coeficiente C"
    )

    @field_validator('surfaces')
    @classmethod
    def validate_surfaces(cls, v: List[dict]) -> List[dict]:
        """Valida que cada superficie tenga los campos necesarios."""
        for i, surface in enumerate(v):
            if 'area_ha' not in surface or 'C' not in surface:
                raise ValueError(
                    f'Superficie {i+1} debe tener "area_ha" y "C"'
                )

            if surface['area_ha'] <= 0:
                raise ValueError(
                    f'Superficie {i+1}: área debe ser positiva'
                )

            if surface['C'] < 0 or surface['C'] > 1:
                raise ValueError(
                    f'Superficie {i+1}: C debe estar entre 0 y 1'
                )

        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "surfaces": [
                        {"area_ha": 2.0, "C": 0.90, "description": "Techos"},
                        {"area_ha": 3.0, "C": 0.85, "description": "Pavimento"},
                        {"area_ha": 5.0, "C": 0.20, "description": "Césped"}
                    ]
                }
            ]
        }
    }


class WeightedCOutput(BaseModel):
    """
    Modelo para el resultado del coeficiente ponderado.

    Attributes:
        C_weighted: Coeficiente de escorrentía ponderado
        total_area_ha: Área total de la cuenca
        surfaces: Detalle de las superficies
    """

    C_weighted: float = Field(
        ...,
        description="Coeficiente de escorrentía ponderado"
    )

    total_area_ha: float = Field(
        ...,
        description="Área total de la cuenca en hectáreas"
    )

    surfaces: List[dict] = Field(
        ...,
        description="Detalle de las superficies analizadas"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "C_weighted": 0.525,
                    "total_area_ha": 10.0,
                    "surfaces": [
                        {
                            "area_ha": 2.0,
                            "C": 0.90,
                            "description": "Techos",
                            "percentage": 20.0
                        },
                        {
                            "area_ha": 3.0,
                            "C": 0.85,
                            "description": "Pavimento",
                            "percentage": 30.0
                        },
                        {
                            "area_ha": 5.0,
                            "C": 0.20,
                            "description": "Césped",
                            "percentage": 50.0
                        }
                    ]
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error.

    Attributes:
        error: Tipo de error
        message: Mensaje descriptivo del error
        details: Detalles adicionales (opcional)
    """

    error: str = Field(
        ...,
        description="Tipo de error"
    )

    message: str = Field(
        ...,
        description="Mensaje descriptivo del error"
    )

    details: Optional[dict] = Field(
        default=None,
        description="Detalles adicionales del error"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "El coeficiente de escorrentía debe estar entre 0 y 1",
                    "details": {"field": "C", "value": 1.5}
                }
            ]
        }
    }
