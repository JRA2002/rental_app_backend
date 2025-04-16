from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet,
    RoomViewSet,
    TenantViewSet,
    OccupationViewSet,
    EarningsView,
    EarningsByRegionView,
    EarningsByOwnerView
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'occupations', OccupationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('properties/stats/', PropertyViewSet.as_view({'get': 'stats'}), name='property-stats'),
    path('properties/region-stats/', PropertyViewSet.as_view({'get': 'region_stats'}), name='property-region-stats'),
    path('rooms/<int:pk>/stats/', RoomViewSet.as_view({'get': 'stats'}), name='room-stats'),
    path('tenants/<int:pk>/history/', TenantViewSet.as_view({'get': 'history'}), name='tenant-history'),
    path('earnings/', EarningsView.as_view(), name='earnings'),
    path('earnings/by-region/', EarningsByRegionView.as_view(), name='earnings-by-region'),
    path('earnings/by-owner/', EarningsByOwnerView.as_view(), name='earnings-by-owner'),
]
