"""
Django Rest Framework ViewSets para HidroCalc API
Equivalente a routers en FastAPI
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from core.models import Project, Watershed, DesignStorm, Hydrograph, RainfallData
from .serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    WatershedSerializer,
    WatershedCreateSerializer,
    WatershedDetailSerializer,
    DesignStormSerializer,
    DesignStormCreateSerializer,
    DesignStormDetailSerializer,
    HydrographSerializer,
    HydrographCreateSerializer,
    HydrographSummarySerializer,
    RainfallDataSerializer,
    RainfallDataCreateSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet para proyectos hidrológicos

    Proporciona operaciones CRUD completas:
    - GET /api/projects/ - Listar proyectos
    - POST /api/projects/ - Crear proyecto
    - GET /api/projects/{id}/ - Detalle de proyecto
    - PUT /api/projects/{id}/ - Actualizar proyecto
    - PATCH /api/projects/{id}/ - Actualización parcial
    - DELETE /api/projects/{id}/ - Eliminar proyecto
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer

    @action(detail=True, methods=['get'])
    def watersheds(self, request, pk=None):
        """
        GET /api/projects/{id}/watersheds/
        Obtener todas las cuencas de un proyecto
        """
        project = self.get_object()
        watersheds = project.watersheds.all()
        serializer = WatershedSerializer(watersheds, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        GET /api/projects/{id}/stats/
        Obtener estadísticas del proyecto
        """
        project = self.get_object()
        stats = {
            'total_watersheds': project.total_watersheds,
            'total_design_storms': sum(
                w.design_storms.count() for w in project.watersheds.all()
            ),
            'total_hydrographs': sum(
                sum(ds.hydrographs.count() for ds in w.design_storms.all())
                for w in project.watersheds.all()
            ),
            'total_area_ha': sum(
                w.area_hectareas for w in project.watersheds.all()
            ),
        }
        return Response(stats)


class WatershedViewSet(viewsets.ModelViewSet):
    """
    ViewSet para cuencas hidrográficas

    - GET /api/watersheds/ - Listar cuencas
    - POST /api/watersheds/ - Crear cuenca
    - GET /api/watersheds/{id}/ - Detalle de cuenca
    - PUT /api/watersheds/{id}/ - Actualizar cuenca
    - DELETE /api/watersheds/{id}/ - Eliminar cuenca
    """
    queryset = Watershed.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return WatershedCreateSerializer
        elif self.action == 'retrieve':
            return WatershedDetailSerializer
        return WatershedSerializer

    def get_queryset(self):
        """Filtrar por proyecto si se proporciona"""
        queryset = Watershed.objects.all()
        project_id = self.request.query_params.get('project_id', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    @action(detail=True, methods=['get'])
    def design_storms(self, request, pk=None):
        """
        GET /api/watersheds/{id}/design_storms/
        Obtener todas las tormentas de diseño de una cuenca
        """
        watershed = self.get_object()
        storms = watershed.design_storms.all()
        serializer = DesignStormSerializer(storms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def rainfall_data(self, request, pk=None):
        """
        GET /api/watersheds/{id}/rainfall_data/
        Obtener datos de lluvia medidos de una cuenca
        """
        watershed = self.get_object()
        rainfall = watershed.rainfall_data.all()
        serializer = RainfallDataSerializer(rainfall, many=True)
        return Response(serializer.data)


class DesignStormViewSet(viewsets.ModelViewSet):
    """
    ViewSet para tormentas de diseño

    - GET /api/design-storms/ - Listar tormentas
    - POST /api/design-storms/ - Crear tormenta
    - GET /api/design-storms/{id}/ - Detalle de tormenta
    - PUT /api/design-storms/{id}/ - Actualizar tormenta
    - DELETE /api/design-storms/{id}/ - Eliminar tormenta
    """
    queryset = DesignStorm.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return DesignStormCreateSerializer
        elif self.action == 'retrieve':
            return DesignStormDetailSerializer
        return DesignStormSerializer

    def get_queryset(self):
        """Filtrar por cuenca si se proporciona"""
        queryset = DesignStorm.objects.all()
        watershed_id = self.request.query_params.get('watershed_id', None)
        if watershed_id is not None:
            queryset = queryset.filter(watershed_id=watershed_id)
        return queryset

    @action(detail=True, methods=['get'])
    def hydrographs(self, request, pk=None):
        """
        GET /api/design-storms/{id}/hydrographs/
        Obtener todos los hidrogramas de una tormenta de diseño
        """
        storm = self.get_object()
        hydrographs = storm.hydrographs.all()
        serializer = HydrographSerializer(hydrographs, many=True)
        return Response(serializer.data)


class HydrographViewSet(viewsets.ModelViewSet):
    """
    ViewSet para hidrogramas calculados

    - GET /api/hydrographs/ - Listar hidrogramas
    - POST /api/hydrographs/ - Crear hidrograma
    - GET /api/hydrographs/{id}/ - Detalle de hidrograma
    - PUT /api/hydrographs/{id}/ - Actualizar hidrograma
    - DELETE /api/hydrographs/{id}/ - Eliminar hidrograma
    """
    queryset = Hydrograph.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return HydrographCreateSerializer
        elif self.action == 'list':
            return HydrographSummarySerializer
        return HydrographSerializer

    def get_queryset(self):
        """Filtrar por tormenta de diseño si se proporciona"""
        queryset = Hydrograph.objects.all()
        design_storm_id = self.request.query_params.get('design_storm_id', None)
        if design_storm_id is not None:
            queryset = queryset.filter(design_storm_id=design_storm_id)
        return queryset

    @action(detail=False, methods=['get'])
    def by_watershed(self, request):
        """
        GET /api/hydrographs/by_watershed/?watershed_id={id}
        Obtener todos los hidrogramas de una cuenca
        """
        watershed_id = request.query_params.get('watershed_id', None)
        if watershed_id is None:
            return Response(
                {'error': 'Se requiere watershed_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        hydrographs = Hydrograph.objects.filter(
            design_storm__watershed_id=watershed_id
        )
        serializer = HydrographSummarySerializer(hydrographs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def compare(self, request):
        """
        GET /api/hydrographs/compare/?ids=1,2,3
        Comparar múltiples hidrogramas
        """
        ids_str = request.query_params.get('ids', None)
        if ids_str is None:
            return Response(
                {'error': 'Se requiere parámetro ids (ej: ids=1,2,3)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ids = [int(id.strip()) for id in ids_str.split(',')]
        except ValueError:
            return Response(
                {'error': 'IDs inválidos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        hydrographs = Hydrograph.objects.filter(id__in=ids)
        serializer = HydrographSerializer(hydrographs, many=True)

        # Calcular estadísticas comparativas
        if hydrographs:
            peak_discharges = [h.peak_discharge_m3s for h in hydrographs]
            comparison_stats = {
                'max_peak_discharge': max(peak_discharges),
                'min_peak_discharge': min(peak_discharges),
                'avg_peak_discharge': sum(peak_discharges) / len(peak_discharges),
                'total_compared': len(hydrographs),
            }
        else:
            comparison_stats = {}

        return Response({
            'hydrographs': serializer.data,
            'statistics': comparison_stats
        })


class RainfallDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet para datos de lluvia medidos

    - GET /api/rainfall-data/ - Listar datos de lluvia
    - POST /api/rainfall-data/ - Crear registro de lluvia
    - GET /api/rainfall-data/{id}/ - Detalle de dato de lluvia
    - PUT /api/rainfall-data/{id}/ - Actualizar dato de lluvia
    - DELETE /api/rainfall-data/{id}/ - Eliminar dato de lluvia
    """
    queryset = RainfallData.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """Seleccionar serializer según la acción"""
        if self.action == 'create':
            return RainfallDataCreateSerializer
        return RainfallDataSerializer

    def get_queryset(self):
        """Filtrar por cuenca si se proporciona"""
        queryset = RainfallData.objects.all()
        watershed_id = self.request.query_params.get('watershed_id', None)
        if watershed_id is not None:
            queryset = queryset.filter(watershed_id=watershed_id)
        return queryset
