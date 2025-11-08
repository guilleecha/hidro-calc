# src/core/models.py
"""
Modelos de Base de Datos para HidroCalc
Usando SQLAlchemy ORM
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List, Optional

Base = declarative_base()


class Project(Base):
    """Modelo para proyectos de hidrología"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    timezone = Column(String(50), default="UTC")
    
    owner_id = Column(Integer, nullable=True, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con cuencas
    watersheds: List["Watershed"] = relationship(
        "Watershed",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    
    class Config:
        arbitrary_types_allowed = True


class Watershed(Base):
    """Modelo para cuencas hidrográficas"""
    __tablename__ = "watersheds"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Características hidráulicas
    area_hectareas = Column(Float, nullable=False, index=True)
    tc_horas = Column(Float, nullable=False)  # Tiempo de concentración
    nc_scs = Column(Integer, nullable=True)   # Número de curva SCS
    
    # Ubicación
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    elevation_m = Column(Float, nullable=True)
    
    # Coeficiente de escorrentía
    c_racional = Column(Float, nullable=True)  # Para Método Racional
    
    # Metadata adicional
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    project: "Project" = relationship("Project", back_populates="watersheds")
    design_storms: List["DesignStorm"] = relationship(
        "DesignStorm",
        back_populates="watershed",
        cascade="all, delete-orphan"
    )
    rainfall_data: List["RainfallData"] = relationship(
        "RainfallData",
        back_populates="watershed",
        cascade="all, delete-orphan"
    )
    
    class Config:
        arbitrary_types_allowed = True


class DesignStorm(Base):
    """Modelo para tormentas de diseño parametrizadas"""
    __tablename__ = "design_storms"
    
    id = Column(Integer, primary_key=True, index=True)
    watershed_id = Column(Integer, ForeignKey("watersheds.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Parámetros básicos
    return_period_years = Column(Integer, nullable=False, index=True)  # Tr
    duration_hours = Column(Float, nullable=False, index=True)
    
    # Lluvia total
    total_rainfall_mm = Column(Float, nullable=False)
    
    # Método de distribución
    distribution_type = Column(String(50), default="alternating_block")
    # Opciones: 'alternating_block', 'chicago', 'sidle', 'custom'
    
    # Parámetros SCS
    initial_abstraction_mm = Column(Float, nullable=True)  # Ia = 0.2*S
    storage_parameter_mm = Column(Float, nullable=True)    # S = (25400/NC - 254)
    
    # Intervalo de tiempo
    time_step_minutes = Column(Integer, default=5)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    watershed: "Watershed" = relationship("Watershed", back_populates="design_storms")
    hydrographs: List["Hydrograph"] = relationship(
        "Hydrograph",
        back_populates="design_storm",
        cascade="all, delete-orphan"
    )
    
    class Config:
        arbitrary_types_allowed = True


class Hydrograph(Base):
    """Modelo para hidrogramas calculados"""
    __tablename__ = "hydrographs"
    
    id = Column(Integer, primary_key=True, index=True)
    design_storm_id = Column(Integer, ForeignKey("design_storms.id", ondelete="CASCADE"), 
                            nullable=False, index=True)
    
    # Identificación
    name = Column(String(255), nullable=True)
    
    # Método de cálculo
    method = Column(String(50), nullable=False, index=True)
    # Opciones: 'rational', 'scs_unit_hydrograph', 'synth_unit_hydro'
    
    # Resultados resumen
    peak_discharge_m3s = Column(Float, nullable=False, index=True)
    peak_discharge_lps = Column(Float, nullable=True)
    time_to_peak_minutes = Column(Float, nullable=True)
    
    # Escorrentía
    total_runoff_mm = Column(Float, nullable=True)
    total_runoff_m3 = Column(Float, nullable=True)
    volume_hm3 = Column(Float, nullable=True)
    
    # Serie temporal del hidrograma (JSON)
    # Array de: {time_min, discharge_m3s, cumulative_volume_m3}
    hydrograph_data = Column(JSON, nullable=False)
    
    # Metadata del cálculo
    rainfall_excess_mm = Column(Float, nullable=True)
    infiltration_total_mm = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    design_storm: "DesignStorm" = relationship("DesignStorm", back_populates="hydrographs")
    
    class Config:
        arbitrary_types_allowed = True


class RainfallData(Base):
    """Modelo para datos de lluvia medidos (opcional)"""
    __tablename__ = "rainfall_data"
    
    id = Column(Integer, primary_key=True, index=True)
    watershed_id = Column(Integer, ForeignKey("watersheds.id", ondelete="CASCADE"), 
                         nullable=False, index=True)
    
    event_date = Column(Date, nullable=False, index=True)
    return_period_years = Column(Integer, nullable=True)
    duration_hours = Column(Float, nullable=True)
    total_rainfall_mm = Column(Float, nullable=False)
    
    # Serie de intensidades
    # Array de: {time_min, intensity_mm_h, cumulative_mm}
    rainfall_series = Column(JSON, nullable=False)
    
    source = Column(String(100), nullable=True)  # DNM, IMFIA, sensor local, etc
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    watershed: "Watershed" = relationship("Watershed", back_populates="rainfall_data")
    
    class Config:
        arbitrary_types_allowed = True
