# src/core/schemas.py
"""
Esquemas Pydantic para validación y serialización en HidroCalc
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# PROJECT SCHEMAS
# ============================================================================

class ProjectBase(BaseModel):
    """Base schema para proyectos"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre del proyecto")
    description: Optional[str] = Field(None, description="Descripción del proyecto")
    location: Optional[str] = Field(None, description="Ubicación del proyecto")
    country: Optional[str] = Field(None, description="País")
    region: Optional[str] = Field(None, description="Región/Departamento")
    timezone: str = Field("UTC", description="Zona horaria")


class ProjectCreate(ProjectBase):
    """Schema para crear un nuevo proyecto"""
    pass


class ProjectUpdate(BaseModel):
    """Schema para actualizar un proyecto"""
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    timezone: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema de respuesta para un proyecto con todas sus relaciones"""
    id: int
    owner_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    """Schema detallado de proyecto con cuencas incluidas"""
    watersheds: List["WatershedResponse"] = []
    
    class Config:
        from_attributes = True


# ============================================================================
# WATERSHED SCHEMAS
# ============================================================================

class WatershedBase(BaseModel):
    """Base schema para cuencas"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la cuenca")
    description: Optional[str] = None
    
    area_hectareas: float = Field(..., gt=0, description="Área en hectáreas")
    tc_horas: float = Field(..., gt=0, description="Tiempo de concentración en horas")
    nc_scs: Optional[int] = Field(None, ge=30, le=100, description="Número de curva SCS (30-100)")
    
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    elevation_m: Optional[float] = None
    
    c_racional: Optional[float] = Field(None, ge=0, le=1, description="Coef. escorrentía (0-1)")

    extra_metadata: Optional[Dict[str, Any]] = None


class WatershedCreate(WatershedBase):
    """Schema para crear una nueva cuenca"""
    project_id: int


class WatershedUpdate(BaseModel):
    """Schema para actualizar una cuenca"""
    name: Optional[str] = None
    description: Optional[str] = None
    area_hectareas: Optional[float] = None
    tc_horas: Optional[float] = None
    nc_scs: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_m: Optional[float] = None
    c_racional: Optional[float] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class WatershedResponse(WatershedBase):
    """Schema de respuesta para una cuenca"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        protected_namespaces = ()


class WatershedDetailResponse(WatershedResponse):
    """Schema detallado de cuenca con tormentas incluidas"""
    design_storms: List["DesignStormResponse"] = []
    
    class Config:
        from_attributes = True


# ============================================================================
# DESIGN STORM SCHEMAS
# ============================================================================

class DesignStormBase(BaseModel):
    """Base schema para tormentas de diseño"""
    name: str = Field(..., min_length=1, description="Nombre de la tormenta")
    description: Optional[str] = None
    
    return_period_years: int = Field(..., gt=0, description="Período de retorno (años)")
    duration_hours: float = Field(..., gt=0, description="Duración de la tormenta (horas)")
    
    total_rainfall_mm: float = Field(..., gt=0, description="Lluvia total (mm)")
    
    distribution_type: str = Field("alternating_block", 
                                  description="Tipo de distribución: alternating_block, chicago, sidle, custom")
    
    initial_abstraction_mm: Optional[float] = Field(None, ge=0, description="Abstracción inicial (mm)")
    storage_parameter_mm: Optional[float] = Field(None, ge=0, description="Parámetro de almacenamiento (mm)")
    
    time_step_minutes: int = Field(5, gt=0, description="Intervalo de tiempo (minutos)")

    extra_metadata: Optional[Dict[str, Any]] = None


class DesignStormCreate(DesignStormBase):
    """Schema para crear una tormenta de diseño"""
    watershed_id: int


class DesignStormUpdate(BaseModel):
    """Schema para actualizar una tormenta"""
    name: Optional[str] = None
    description: Optional[str] = None
    return_period_years: Optional[int] = None
    duration_hours: Optional[float] = None
    total_rainfall_mm: Optional[float] = None
    distribution_type: Optional[str] = None
    initial_abstraction_mm: Optional[float] = None
    storage_parameter_mm: Optional[float] = None
    time_step_minutes: Optional[int] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class DesignStormResponse(DesignStormBase):
    """Schema de respuesta para una tormenta de diseño"""
    id: int
    watershed_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DesignStormDetailResponse(DesignStormResponse):
    """Schema detallado con hidrogramas incluidos"""
    hydrographs: List["HydrographResponse"] = []
    
    class Config:
        from_attributes = True


# ============================================================================
# HYDROGRAPH SCHEMAS (La parte más importante)
# ============================================================================

class HydrographPoint(BaseModel):
    """Un punto en la serie temporal del hidrograma"""
    time_min: float = Field(..., ge=0, description="Tiempo en minutos")
    discharge_m3s: float = Field(..., ge=0, description="Caudal en m³/s")
    cumulative_volume_m3: float = Field(..., ge=0, description="Volumen acumulado en m³")


class HydrographBase(BaseModel):
    """Base schema para hidrogramas"""
    name: Optional[str] = Field(None, description="Nombre descriptivo del hidrograma")
    
    method: str = Field(..., description="Método de cálculo: rational, scs_unit_hydrograph, synth_unit_hydro")
    
    peak_discharge_m3s: float = Field(..., gt=0, description="Caudal máximo (m³/s)")
    peak_discharge_lps: Optional[float] = Field(None, description="Caudal máximo (L/s)")
    time_to_peak_minutes: Optional[float] = Field(None, ge=0, description="Tiempo al pico (min)")
    
    total_runoff_mm: Optional[float] = Field(None, ge=0, description="Escorrentía total (mm)")
    total_runoff_m3: Optional[float] = Field(None, ge=0, description="Escorrentía total (m³)")
    volume_hm3: Optional[float] = Field(None, ge=0, description="Volumen (hm³)")
    
    hydrograph_data: List[HydrographPoint] = Field(..., description="Serie temporal del hidrograma")
    
    rainfall_excess_mm: Optional[float] = Field(None, ge=0, description="Lluvia neta (mm)")
    infiltration_total_mm: Optional[float] = Field(None, ge=0, description="Infiltración total (mm)")
    
    notes: Optional[str] = None


class HydrographCreate(HydrographBase):
    """Schema para crear un hidrograma"""
    design_storm_id: int


class HydrographUpdate(BaseModel):
    """Schema para actualizar un hidrograma"""
    name: Optional[str] = None
    method: Optional[str] = None
    peak_discharge_m3s: Optional[float] = None
    peak_discharge_lps: Optional[float] = None
    time_to_peak_minutes: Optional[float] = None
    total_runoff_mm: Optional[float] = None
    total_runoff_m3: Optional[float] = None
    volume_hm3: Optional[float] = None
    hydrograph_data: Optional[List[HydrographPoint]] = None
    rainfall_excess_mm: Optional[float] = None
    infiltration_total_mm: Optional[float] = None
    notes: Optional[str] = None


class HydrographResponse(HydrographBase):
    """Schema de respuesta para un hidrograma"""
    id: int
    design_storm_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HydrographSummary(BaseModel):
    """Resumen simplificado de un hidrograma para listas"""
    id: int
    name: Optional[str]
    method: str
    peak_discharge_m3s: float
    peak_discharge_lps: Optional[float]
    total_runoff_m3: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# RAINFALL DATA SCHEMAS (Opcional)
# ============================================================================

class RainfallPoint(BaseModel):
    """Un punto en la serie de lluvia"""
    time_min: float = Field(..., ge=0)
    intensity_mm_h: float = Field(..., ge=0)
    cumulative_mm: float = Field(..., ge=0)


class RainfallDataBase(BaseModel):
    """Base schema para datos de lluvia"""
    event_date: str = Field(..., description="Fecha del evento (YYYY-MM-DD)")
    return_period_years: Optional[int] = None
    duration_hours: Optional[float] = None
    total_rainfall_mm: float = Field(..., gt=0)
    
    rainfall_series: List[RainfallPoint]
    
    source: Optional[str] = None  # DNM, IMFIA, sensor local, etc
    notes: Optional[str] = None


class RainfallDataCreate(RainfallDataBase):
    """Schema para crear datos de lluvia"""
    watershed_id: int


class RainfallDataResponse(RainfallDataBase):
    """Schema de respuesta para datos de lluvia"""
    id: int
    watershed_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# QUERY & COMPARISON SCHEMAS (Para funcionalidades avanzadas)
# ============================================================================

class HydrographComparison(BaseModel):
    """Schema para comparar múltiples hidrogramas"""
    watershed_id: int
    return_period_years: Optional[int] = None
    durations_hours: Optional[List[float]] = None  # Si está vacío, todas


class HydrographComparisonResult(BaseModel):
    """Resultado de comparación de hidrogramas"""
    hydrographs: List[HydrographSummary]
    statistics: Dict[str, Any]  # Estadísticas comparativas


class StormAnalysis(BaseModel):
    """Schema para análisis completo de una tormenta"""
    design_storm_id: int
    include_hydrographs: bool = True
    include_rainfall_data: bool = False


# ============================================================================
# Update de relaciones circulares
# ============================================================================

ProjectDetailResponse.model_rebuild()
WatershedDetailResponse.model_rebuild()
DesignStormDetailResponse.model_rebuild()
