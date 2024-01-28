from django.urls import path
from .viewsets import (
    BookingConfirmView,
    CreatePaymentView,
    OpenVehicleView,
    VehicleDetailView,
    LocationListView,
    BookingCreateView,
    StatisticsRetrieveView,
    UserVehiclesView,
    UserBookingsView,
    CancelBookingView,
    UserTerminatedBookingsView
)

urlpatterns = [
    path("open-vehicles/", OpenVehicleView.as_view(), name="open-vehicles"),
    path(
        "vehicle/<slug:vehicle_main__slug>/",
        VehicleDetailView.as_view(),
        name="vehicle-detail",
    ),
    path(
        "user-vehicles/",
        UserVehiclesView.as_view(),
        name="vehicle-detail",
    ),
    path("locations/", LocationListView.as_view(), name="active-locations"),
    path(
        "vehicle/<slug:id>/stats", StatisticsRetrieveView.as_view(), name="vehicle-stat"
    ),
    path("booking/create/", BookingCreateView.as_view(), name="booking-create"),
    path("booking/payment-create/", CreatePaymentView.as_view(), name="create-payment"),
    path("booking/cancel/", CancelBookingView.as_view(), name="create-payment"),
    path("booking/confirm/", BookingConfirmView.as_view(), name="confirm-booking"),
    path("user/bookings/", UserBookingsView.as_view(), name="user-bookings"),
    path("user/terminated-bookings/", UserTerminatedBookingsView.as_view(), name="user-bookings"),
]
