# src/database.py
"""
Configuración de Base de Datos para HidroCalc
Soporta PostgreSQL, MySQL y SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Usar SQLite por defecto para desarrollo
    DATABASE_URL = "sqlite:///./hidrocal.db"
    print(f"[WARNING] No se encontro DATABASE_URL, usando SQLite: {DATABASE_URL}")

print(f"[DB] Conectando a: {DATABASE_URL.split('@')[0] if '@' in DATABASE_URL else DATABASE_URL[:50]}")

# ============================================================================
# CREAR MOTOR DE BASE DE DATOS
# ============================================================================

if DATABASE_URL.startswith("sqlite"):
    # SQLite (para desarrollo)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=os.getenv("SQL_ECHO", "False").lower() == "true"
    )
else:
    # PostgreSQL o MySQL (para producción)
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        echo=os.getenv("SQL_ECHO", "False").lower() == "true"
    )

# ============================================================================
# SESSION LOCAL
# ============================================================================

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependencia para obtener sesión de base de datos en FastAPI

    Uso en rutas:
    @app.get("/endpoint")
    def endpoint(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# INICIALIZAR BASE DE DATOS
# ============================================================================

def init_db():
    """
    Crear todas las tablas en la base de datos
    Llamar una sola vez al iniciar la aplicación
    """
    from core.models import Base

    print("[INIT] Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Base de datos lista")


def drop_all():
    """
    ⚠️ CUIDADO: Elimina todas las tablas
    Solo usar para desarrollo/testing
    """
    from core.models import Base

    print("[WARNING] Eliminando todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    print("[OK] Tablas eliminadas")


# ============================================================================
# SEED DATA (Datos de prueba)
# ============================================================================

def seed_db():
    """
    Crear datos de prueba en la base de datos
    Útil para desarrollo y testing
    """
    from core.models import Project, Watershed, DesignStorm

    db = SessionLocal()

    try:
        # Verificar si ya existen datos
        if db.query(Project).count() > 0:
            print("[SKIP] Base de datos ya contiene datos, saltando seed")
            return

        print("[SEED] Sembrando datos de prueba...")

        # Crear proyecto
        project = Project(
            name="Sistema de Drenaje Montevideo",
            description="Proyecto piloto para análisis de tormentas en Montevideo",
            location="Montevideo, Uruguay",
            country="Uruguay",
            region="Montevideo"
        )
        db.add(project)
        db.flush()

        # Crear cuencas
        watersheds = [
            Watershed(
                project_id=project.id,
                name="Arroyo Miguelete Alto",
                description="Cuenca alta del Arroyo Miguelete",
                area_hectareas=250,
                tc_horas=1.8,
                nc_scs=72,
                latitude=-34.85,
                longitude=-56.15,
                elevation_m=50
            ),
            Watershed(
                project_id=project.id,
                name="Arroyo Carrasco Medio",
                description="Cuenca media del Arroyo Carrasco",
                area_hectareas=180,
                tc_horas=1.5,
                nc_scs=75,
                latitude=-34.80,
                longitude=-56.12,
                elevation_m=35
            ),
            Watershed(
                project_id=project.id,
                name="Arroyo Pantanoso",
                description="Cuenca Arroyo Pantanoso",
                area_hectareas=320,
                tc_horas=2.1,
                nc_scs=68,
                latitude=-34.75,
                longitude=-56.18,
                elevation_m=25
            )
        ]

        for ws in watersheds:
            db.add(ws)

        db.flush()

        # Crear tormentas de diseño
        storms = [
            DesignStorm(
                watershed_id=watersheds[0].id,
                name="Tr=10 Años 2h",
                return_period_years=10,
                duration_hours=2.0,
                total_rainfall_mm=85.3,
                distribution_type="alternating_block",
                time_step_minutes=5
            ),
            DesignStorm(
                watershed_id=watersheds[0].id,
                name="Tr=10 Años 6h",
                return_period_years=10,
                duration_hours=6.0,
                total_rainfall_mm=102.5,
                distribution_type="alternating_block",
                time_step_minutes=5
            ),
            DesignStorm(
                watershed_id=watersheds[0].id,
                name="Tr=10 Años 12h",
                return_period_years=10,
                duration_hours=12.0,
                total_rainfall_mm=125.8,
                distribution_type="alternating_block",
                time_step_minutes=5
            ),
            DesignStorm(
                watershed_id=watersheds[0].id,
                name="Tr=10 Años 24h",
                return_period_years=10,
                duration_hours=24.0,
                total_rainfall_mm=152.2,
                distribution_type="alternating_block",
                time_step_minutes=5
            ),
        ]

        for storm in storms:
            db.add(storm)

        db.commit()
        print(f"[OK] Seed completado: 1 proyecto, {len(watersheds)} cuencas, {len(storms)} tormentas")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error en seed: {str(e)}")
    finally:
        db.close()


# ============================================================================
# FUNCIONES AUXILIARES DE CONSULTA
# ============================================================================

def get_project_by_name(db: Session, name: str) -> Optional["Project"]:
    """Obtener un proyecto por nombre"""
    from core.models import Project
    return db.query(Project).filter(Project.name == name).first()


def get_watershed_by_name(db: Session, project_id: int, name: str) -> Optional["Watershed"]:
    """Obtener una cuenca por nombre dentro de un proyecto"""
    from core.models import Watershed
    return db.query(Watershed).filter(
        Watershed.project_id == project_id,
        Watershed.name == name
    ).first()


def count_hydrographs_by_watershed(db: Session, watershed_id: int) -> int:
    """Contar hidrogramas de una cuenca"""
    from core.models import Hydrograph, DesignStorm
    return (
        db.query(Hydrograph)
        .join(DesignStorm)
        .filter(DesignStorm.watershed_id == watershed_id)
        .count()
    )


def get_hydrographs_by_return_period(
    db: Session,
    watershed_id: int,
    return_period_years: int
) -> list:
    """Obtener todos los hidrogramas de una cuenca para un período de retorno"""
    from core.models import Hydrograph, DesignStorm
    return (
        db.query(Hydrograph)
        .join(DesignStorm)
        .filter(
            DesignStorm.watershed_id == watershed_id,
            DesignStorm.return_period_years == return_period_years
        )
        .order_by(DesignStorm.duration_hours)
        .all()
    )


def get_max_flow_by_duration(
    db: Session,
    watershed_id: int,
    return_period_years: Optional[int] = None
) -> dict:
    """
    Obtener caudal máximo para cada duración de tormenta
    Útil para análisis comparativo
    """
    from core.models import Hydrograph, DesignStorm

    query = (
        db.query(
            DesignStorm.duration_hours,
            Hydrograph.peak_discharge_m3s
        )
        .join(DesignStorm)
        .filter(DesignStorm.watershed_id == watershed_id)
    )

    if return_period_years:
        query = query.filter(DesignStorm.return_period_years == return_period_years)

    results = query.order_by(DesignStorm.duration_hours).all()

    return {
        "durations_hours": [r[0] for r in results],
        "peak_flows_m3s": [r[1] for r in results]
    }


# ============================================================================
# ESTADÍSTICAS DE BASE DE DATOS
# ============================================================================

def get_db_stats(db: Session) -> dict:
    """Obtener estadísticas generales de la base de datos"""
    from core.models import Project, Watershed, DesignStorm, Hydrograph

    return {
        "num_projects": db.query(Project).count(),
        "num_watersheds": db.query(Watershed).count(),
        "num_design_storms": db.query(DesignStorm).count(),
        "num_hydrographs": db.query(Hydrograph).count(),
    }


if __name__ == "__main__":
    # Para ejecutar: python src/database.py

    print("\n" + "="*60)
    print("HidroCalc - Database Manager")
    print("="*60)

    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init":
            init_db()
        elif command == "drop":
            confirm = input("[WARNING] Estas seguro? Esto eliminara TODOS los datos. (y/n): ")
            if confirm.lower() == 'y':
                drop_all()
        elif command == "seed":
            init_db()
            seed_db()
        elif command == "reset":
            confirm = input("[WARNING] Resetear BD (eliminar + crear + seed)? (y/n): ")
            if confirm.lower() == 'y':
                drop_all()
                init_db()
                seed_db()
        else:
            print(f"[ERROR] Comando desconocido: {command}")
    else:
        print("\nUsos disponibles:")
        print("  python database.py init    → Crear tablas")
        print("  python database.py drop    → Eliminar tablas")
        print("  python database.py seed    → Crear datos de prueba")
        print("  python database.py reset   → Reset completo (drop + init + seed)")
