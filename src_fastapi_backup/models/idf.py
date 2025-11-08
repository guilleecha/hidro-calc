"""
Modelos Pydantic para validación de datos de Curvas IDF.

Define las estructuras de datos de entrada y salida para los cálculos
de intensidad de lluvia según las Curvas IDF de Uruguay.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class IDFInput(BaseModel):
    """
    Modelo para los datos de entrada del cálculo de Curvas IDF.

    Attributes:
        P3_10: Precipitación de 3 horas y 10 años en mm (rango típico: 50-100)
        Tr: Período de retorno en años (>= 2)
        d: Duración de la tormenta en horas (> 0)
        Ac: Área de cuenca en km² (opcional, para corrección por área)
    """

    P3_10: float = Field(
        ...,
        ge=50,
        le=100,
        description="Precipitación de 3h y 10 años en mm (P₃,₁₀)",
        examples=[74.0, 75.0, 79.0]
    )

    Tr: float = Field(
        ...,
        ge=2,
        le=500,
        description="Período de retorno en años",
        examples=[5, 10, 25, 50, 100]
    )

    d: float = Field(
        ...,
        gt=0,
        le=48,
        description="Duración de la tormenta en horas",
        examples=[0.25, 0.5, 1, 2, 3, 6, 12, 24]
    )

    Ac: Optional[float] = Field(
        default=None,
        ge=0,
        description="Área de cuenca en km² (opcional, None para intensidad puntual)"
    )

    @field_validator('Tr')
    @classmethod
    def validate_Tr(cls, v: float) -> float:
        """
        Valida el período de retorno.

        Args:
            v: Valor del período de retorno

        Returns:
            Valor validado

        Raises:
            ValueError: Si Tr < 2 años
        """
        if v < 2:
            raise ValueError('El período de retorno debe ser >= 2 años')
        return v

    @field_validator('d')
    @classmethod
    def validate_duration(cls, v: float) -> float:
        """
        Valida la duración.

        Args:
            v: Valor de la duración

        Returns:
            Valor validado

        Raises:
            ValueError: Si d <= 0
        """
        if v <= 0:
            raise ValueError('La duración debe ser mayor a 0')
        return v

    @field_validator('P3_10')
    @classmethod
    def validate_P3_10(cls, v: float) -> float:
        """
        Valida P₃,₁₀.

        Args:
            v: Valor de P₃,₁₀

        Returns:
            Valor validado
        """
        if v < 50 or v > 100:
            raise ValueError(
                'P₃,₁₀ debe estar entre 50 y 100 mm (rango típico de Uruguay)'
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "P3_10": 74,
                    "Tr": 5,
                    "d": 1,
                    "Ac": 30,
                    "description": "Ejemplo: La Paloma, Tr=5 años, d=1h, A=30km²"
                },
                {
                    "P3_10": 75,
                    "Tr": 10,
                    "d": 0.5,
                    "Ac": None,
                    "description": "Intensidad puntual, Tr=10 años, d=30min"
                },
                {
                    "P3_10": 79,
                    "Tr": 25,
                    "d": 24,
                    "Ac": 100,
                    "description": "Minas, Tr=25 años, d=24h, A=100km²"
                }
            ]
        }
    }


class IDFOutput(BaseModel):
    """
    Modelo para los resultados del cálculo de Curvas IDF.

    Attributes:
        I_mmh: Intensidad de lluvia en mm/h
        P_mm: Precipitación total en mm
        CT: Factor de corrección por período de retorno
        CD: Factor de corrección por duración
        CA: Factor de corrección por área de cuenca
        P3_10: Valor de P₃,₁₀ utilizado
        Tr: Período de retorno utilizado
        d_hours: Duración utilizada
        Ac_km2: Área de cuenca utilizada (None si no aplica)
        formula: Fórmula utilizada
    """

    I_mmh: float = Field(
        ...,
        description="Intensidad de lluvia en mm/h"
    )

    P_mm: float = Field(
        ...,
        description="Precipitación total en mm"
    )

    CT: float = Field(
        ...,
        description="Factor de corrección por período de retorno"
    )

    CD: float = Field(
        ...,
        description="Factor de corrección por duración"
    )

    CA: float = Field(
        ...,
        description="Factor de corrección por área de cuenca"
    )

    P3_10: float = Field(
        ...,
        description="Precipitación de 3h y 10 años (mm)"
    )

    Tr: float = Field(
        ...,
        description="Período de retorno (años)"
    )

    d_hours: float = Field(
        ...,
        description="Duración de la tormenta (horas)"
    )

    Ac_km2: Optional[float] = Field(
        default=None,
        description="Área de cuenca (km²)"
    )

    formula: str = Field(
        default="I = P₃,₁₀ × CT × CD × CA / d",
        description="Fórmula utilizada para el cálculo"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "I_mmh": 36.34,
                    "P_mm": 36.34,
                    "CT": 0.8456,
                    "CD": 0.5184,
                    "CA": 0.9451,
                    "P3_10": 74,
                    "Tr": 5,
                    "d_hours": 1,
                    "Ac_km2": 30,
                    "formula": "I = P₃,₁₀ × CT × CD × CA / d"
                },
                {
                    "I_mmh": 77.24,
                    "P_mm": 38.62,
                    "CT": 0.9432,
                    "CD": 0.4103,
                    "CA": 1.0,
                    "P3_10": 75,
                    "Tr": 10,
                    "d_hours": 0.5,
                    "Ac_km2": None,
                    "formula": "I = P₃,₁₀ × CT × CD × CA / d"
                }
            ]
        }
    }
