from rest_framework import routers
from apps.vehicles import viewsets as vehicle_rental_views

router = routers.DefaultRouter()

router.register(
    r"vehicle",
    vehicle_rental_views.VehicleViewSet,
    basename="vehicle",
)
router.register(
    r"vehicle-details",
    vehicle_rental_views.VehicleDetailsViewSet,
    basename="vehicle_detail",
)
