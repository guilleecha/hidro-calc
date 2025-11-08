# src/api/routes.py
"""
Rutas FastAPI para HidroCalc con CRUD completo
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Importar modelos, esquemas y base de datos
from core.models import Project, Watershed, DesignStorm, Hydrograph, RainfallData, Base
from core.schemas import (
    ProjectCreate, ProjectResponse, ProjectDetailResponse, ProjectUpdate,
    WatershedCreate, WatershedResponse, WatershedDetailResponse, WatershedUpdate,
    DesignStormCreate, DesignStormResponse, DesignStormDetailResponse, DesignStormUpdate,
    HydrographCreate, HydrographResponse, HydrographSummary, HydrographUpdate,
    RainfallDataCreate, RainfallDataResponse,
    HydrographComparison, HydrographComparisonResult
)
from database import get_db

router = APIRouter(prefix="/api/v1", tags=["HidroCalc"])


# ============================================================================
# PROJECT ROUTES
# ============================================================================

@router.get("/projects", response_model=List[ProjectResponse])
def list_projects(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de proyectos con paginación"""
    query = db.query(Project)
    
    if is_active is not None:
        query = query.filter(Project.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


@router.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo proyecto"""
    db_project = Project(**project.dict())
    db.add(db_project)
    try:
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear proyecto: {str(e)}")


@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de un proyecto con sus cuencas"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un proyecto"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un proyecto (cascada: elimina cuencas, tormentas, hidrogramas)"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db.delete(db_project)
    db.commit()
    return None


# ============================================================================
# WATERSHED ROUTES
# ============================================================================

@router.get("/projects/{project_id}/watersheds", response_model=List[WatershedResponse])
def list_watersheds(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    area_min: Optional[float] = Query(None, gt=0),
    area_max: Optional[float] = Query(None, gt=0),
    db: Session = Depends(get_db)
):
    """Obtener cuencas de un proyecto con filtros opcionales"""
    # Verificar que el proyecto existe
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    query = db.query(Watershed).filter(Watershed.project_id == project_id)
    
    # Filtrar por área si se especifica
    if area_min:
        query = query.filter(Watershed.area_hectareas >= area_min)
    if area_max:
        query = query.filter(Watershed.area_hectareas <= area_max)
    
    return query.offset(skip).limit(limit).all()


@router.post("/projects/{project_id}/watersheds", response_model=WatershedResponse, status_code=201)
def create_watershed(
    project_id: int,
    watershed: WatershedCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva cuenca en un proyecto"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    watershed_dict = watershed.dict()
    watershed_dict['project_id'] = project_id
    db_watershed = Watershed(**watershed_dict)
    
    db.add(db_watershed)
    try:
        db.commit()
        db.refresh(db_watershed)
        return db_watershed
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear cuenca: {str(e)}")


@router.get("/watersheds/{watershed_id}", response_model=WatershedDetailResponse)
def get_watershed(
    watershed_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una cuenca con sus tormentas"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    return db_watershed


@router.put("/watersheds/{watershed_id}", response_model=WatershedResponse)
def update_watershed(
    watershed_id: int,
    watershed: WatershedUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una cuenca"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    
    update_data = watershed.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_watershed, key, value)
    
    db.add(db_watershed)
    db.commit()
    db.refresh(db_watershed)
    return db_watershed


@router.delete("/watersheds/{watershed_id}", status_code=204)
def delete_watershed(
    watershed_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una cuenca (cascada)"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    
    db.delete(db_watershed)
    db.commit()


# ============================================================================
# DESIGN STORM ROUTES
# ============================================================================

@router.get("/watersheds/{watershed_id}/design-storms", response_model=List[DesignStormResponse])
def list_design_storms(
    watershed_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    return_period: Optional[int] = Query(None, gt=0),
    duration_hours: Optional[float] = Query(None, gt=0),
    db: Session = Depends(get_db)
):
    """Obtener tormentas de diseño de una cuenca con filtros"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    
    query = db.query(DesignStorm).filter(DesignStorm.watershed_id == watershed_id)
    
    if return_period:
        query = query.filter(DesignStorm.return_period_years == return_period)
    if duration_hours:
        query = query.filter(DesignStorm.duration_hours == duration_hours)
    
    return query.offset(skip).limit(limit).all()


@router.post("/watersheds/{watershed_id}/design-storms", response_model=DesignStormResponse, status_code=201)
def create_design_storm(
    watershed_id: int,
    storm: DesignStormCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva tormenta de diseño"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    
    storm_dict = storm.dict()
    storm_dict['watershed_id'] = watershed_id
    
    # Calcular Ia y S si no se proporcionan
    if storm_dict.get('storage_parameter_mm') is None and db_watershed.nc_scs:
        s_mm = (25400 / db_watershed.nc_scs) - 254
        storm_dict['storage_parameter_mm'] = max(0, s_mm)
        storm_dict['initial_abstraction_mm'] = 0.2 * max(0, s_mm)
    
    db_storm = DesignStorm(**storm_dict)
    db.add(db_storm)
    try:
        db.commit()
        db.refresh(db_storm)
        return db_storm
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear tormenta: {str(e)}")


@router.get("/design-storms/{design_storm_id}", response_model=DesignStormDetailResponse)
def get_design_storm(
    design_storm_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una tormenta con sus hidrogramas"""
    db_storm = db.query(DesignStorm).filter(DesignStorm.id == design_storm_id).first()
    if not db_storm:
        raise HTTPException(status_code=404, detail="Tormenta no encontrada")
    return db_storm


@router.put("/design-storms/{design_storm_id}", response_model=DesignStormResponse)
def update_design_storm(
    design_storm_id: int,
    storm: DesignStormUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una tormenta"""
    db_storm = db.query(DesignStorm).filter(DesignStorm.id == design_storm_id).first()
    if not db_storm:
        raise HTTPException(status_code=404, detail="Tormenta no encontrada")
    
    update_data = storm.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_storm, key, value)
    
    db.add(db_storm)
    db.commit()
    db.refresh(db_storm)
    return db_storm


@router.delete("/design-storms/{design_storm_id}", status_code=204)
def delete_design_storm(
    design_storm_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar una tormenta (cascada)"""
    db_storm = db.query(DesignStorm).filter(DesignStorm.id == design_storm_id).first()
    if not db_storm:
        raise HTTPException(status_code=404, detail="Tormenta no encontrada")
    
    db.delete(db_storm)
    db.commit()


# ============================================================================
# HYDROGRAPH ROUTES (¡LO MÁS IMPORTANTE!)
# ============================================================================

@router.get("/design-storms/{design_storm_id}/hydrographs", response_model=List[HydrographSummary])
def list_hydrographs(
    design_storm_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    method: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener hidrogramas de una tormenta"""
    db_storm = db.query(DesignStorm).filter(DesignStorm.id == design_storm_id).first()
    if not db_storm:
        raise HTTPException(status_code=404, detail="Tormenta no encontrada")
    
    query = db.query(Hydrograph).filter(Hydrograph.design_storm_id == design_storm_id)
    
    if method:
        query = query.filter(Hydrograph.method == method)
    
    return query.offset(skip).limit(limit).all()


@router.post("/design-storms/{design_storm_id}/hydrographs", response_model=HydrographResponse, status_code=201)
def create_hydrograph(
    design_storm_id: int,
    hydrograph: HydrographCreate,
    db: Session = Depends(get_db)
):
    """Crear y guardar un nuevo hidrograma"""
    db_storm = db.query(DesignStorm).filter(DesignStorm.id == design_storm_id).first()
    if not db_storm:
        raise HTTPException(status_code=404, detail="Tormenta no encontrada")
    
    hydro_dict = hydrograph.dict()
    hydro_dict['design_storm_id'] = design_storm_id
    
    # Convertir lista de HydrographPoint a JSON
    if 'hydrograph_data' in hydro_dict:
        hydro_dict['hydrograph_data'] = [
            point.dict() for point in hydro_dict['hydrograph_data']
        ]
    
    db_hydrograph = Hydrograph(**hydro_dict)
    db.add(db_hydrograph)
    try:
        db.commit()
        db.refresh(db_hydrograph)
        return db_hydrograph
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar hidrograma: {str(e)}")


@router.get("/hydrographs/{hydrograph_id}", response_model=HydrographResponse)
def get_hydrograph(
    hydrograph_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un hidrograma específico con todos sus datos"""
    db_hydrograph = db.query(Hydrograph).filter(Hydrograph.id == hydrograph_id).first()
    if not db_hydrograph:
        raise HTTPException(status_code=404, detail="Hidrograma no encontrado")
    return db_hydrograph


@router.put("/hydrographs/{hydrograph_id}", response_model=HydrographResponse)
def update_hydrograph(
    hydrograph_id: int,
    hydrograph: HydrographUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un hidrograma"""
    db_hydrograph = db.query(Hydrograph).filter(Hydrograph.id == hydrograph_id).first()
    if not db_hydrograph:
        raise HTTPException(status_code=404, detail="Hidrograma no encontrado")
    
    update_data = hydrograph.dict(exclude_unset=True)
    
    # Convertir HydrographPoint a JSON si es necesario
    if 'hydrograph_data' in update_data:
        update_data['hydrograph_data'] = [
            point.dict() if hasattr(point, 'dict') else point
            for point in update_data['hydrograph_data']
        ]
    
    for key, value in update_data.items():
        setattr(db_hydrograph, key, value)
    
    db.add(db_hydrograph)
    db.commit()
    db.refresh(db_hydrograph)
    return db_hydrograph


@router.delete("/hydrographs/{hydrograph_id}", status_code=204)
def delete_hydrograph(
    hydrograph_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un hidrograma"""
    db_hydrograph = db.query(Hydrograph).filter(Hydrograph.id == hydrograph_id).first()
    if not db_hydrograph:
        raise HTTPException(status_code=404, detail="Hidrograma no encontrado")
    
    db.delete(db_hydrograph)
    db.commit()


# ============================================================================
# ADVANCED QUERIES & ANALYSIS
# ============================================================================

@router.post("/compare-hydrographs", response_model=HydrographComparisonResult)
def compare_hydrographs(
    comparison: HydrographComparison,
    db: Session = Depends(get_db)
):
    """
    Comparar múltiples hidrogramas de una cuenca
    Útil para ver diferencias entre duraciones de tormenta
    """
    query = (
        db.query(Hydrograph)
        .join(DesignStorm)
        .filter(DesignStorm.watershed_id == comparison.watershed_id)
    )
    
    if comparison.return_period_years:
        query = query.filter(DesignStorm.return_period_years == comparison.return_period_years)
    
    if comparison.durations_hours:
        query = query.filter(DesignStorm.duration_hours.in_(comparison.durations_hours))
    
    hydrographs = query.all()
    
    if not hydrographs:
        raise HTTPException(status_code=404, detail="No se encontraron hidrogramas para comparar")
    
    # Calcular estadísticas
    peak_flows = [h.peak_discharge_m3s for h in hydrographs]
    volumes = [h.total_runoff_m3 for h in hydrographs]
    
    statistics = {
        "num_hydrographs": len(hydrographs),
        "max_peak_flow": max(peak_flows),
        "min_peak_flow": min(peak_flows),
        "avg_peak_flow": sum(peak_flows) / len(peak_flows),
        "max_volume": max(volumes),
        "min_volume": min(volumes),
        "avg_volume": sum(volumes) / len(volumes),
    }
    
    hydro_summaries = [HydrographSummary.from_orm(h) for h in hydrographs]
    
    return HydrographComparisonResult(
        hydrographs=hydro_summaries,
        statistics=statistics
    )


@router.get("/watersheds/{watershed_id}/summary")
def watershed_summary(
    watershed_id: int,
    db: Session = Depends(get_db)
):
    """Obtener resumen de una cuenca con estadísticas de hidrogramas"""
    db_watershed = db.query(Watershed).filter(Watershed.id == watershed_id).first()
    if not db_watershed:
        raise HTTPException(status_code=404, detail="Cuenca no encontrada")
    
    # Contar tormentas
    num_storms = db.query(DesignStorm).filter(DesignStorm.watershed_id == watershed_id).count()
    
    # Contar hidrogramas
    num_hydros = (
        db.query(Hydrograph)
        .join(DesignStorm)
        .filter(DesignStorm.watershed_id == watershed_id)
        .count()
    )
    
    # Obtener rangos de caudal
    hydrographs = (
        db.query(Hydrograph)
        .join(DesignStorm)
        .filter(DesignStorm.watershed_id == watershed_id)
        .all()
    )
    
    if hydrographs:
        peak_flows = [h.peak_discharge_m3s for h in hydrographs]
        stats = {
            "max_peak_flow_m3s": max(peak_flows),
            "min_peak_flow_m3s": min(peak_flows),
        }
    else:
        stats = {}
    
    return {
        "watershed": WatershedResponse.from_orm(db_watershed),
        "num_design_storms": num_storms,
        "num_hydrographs": num_hydros,
        "peak_flow_statistics": stats
    }
