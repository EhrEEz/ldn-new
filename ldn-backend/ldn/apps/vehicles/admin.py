from django.contrib import admin
from .models import (
    Vehicle, VehicleDetails, Location, Booking,
    VehicleStatistics, BookingDetails, TerminateBooking
)

admin.site.site_header = "LDN Admin"
admin.site.site_title = "LDN"
admin.site.index_title = "Site Administration"


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    model = Vehicle
    list_display = ("id", "reg_no", "model_manufacturer", "model_name", "vehicle_owner", "creation_date")
    ordering = ('-creation_date', )


@admin.register(VehicleDetails)
class VehicleDetailsAdmin(admin.ModelAdmin):
    model = VehicleDetails
    list_display = ("vehicle_main", "vehicle_verified", "registration_document")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ("id", "creation_date", "is_confirmed", "is_terminated", "booking_start_date", "booking_end_date", "total_cost")
    ordering = ["-creation_date",]


@admin.register(BookingDetails)
class BookingDetailsAdmin(admin.ModelAdmin):
    model = BookingDetails
    list_display = ("booking", "creation_date", "odometer_reading_before", "odometer_reading_after")
    ordering = ["-creation_date"]


@admin.register(VehicleStatistics)
class VehicleStatisticsAdmin(admin.ModelAdmin):
    model = VehicleStatistics
    list_display = ("vehicle", "total_earnings", "total_expense", "total_km_tracked", "total_rentals", "total_turnover", "creation_date")
    ordering = ["-creation_date"]


@admin.register(TerminateBooking)
class TerminateBookingAdmin(admin.ModelAdmin):
    model = TerminateBooking
    list_display = ("end_type", "booking", "amount", "handshake", "creation_date", "modification_date")
    ordering = ["-creation_date"]


# admin.site.register(VehicleDetails)
admin.site.register(Location)
# admin.site.register(Booking)
# admin.site.register(VehicleStatistics)
# admin.site.register(BookingDetails)
# admin.site.register(TerminateBooking)
