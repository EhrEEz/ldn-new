from .models import (
    BookingDetails,
    Location,
    Vehicle,
    VehicleDetails,
    Booking,
    VehicleStatistics,
    TerminateBooking,
)
from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "id"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["city"]


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_city = serializers.StringRelatedField(many=False)
    transmission = ChoiceField(choices=Vehicle.TRANSMISSION_TYPES)
    vehicle_owner = ShortUserSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleListSerializer(serializers.ModelSerializer):
    vehicle_city = serializers.StringRelatedField(many=False)
    transmission = ChoiceField(choices=Vehicle.TRANSMISSION_TYPES)

    class Meta:
        model = Vehicle
        fields = [
            "reg_no",
            "seats",
            "color_name",
            "color_code",
            "model_name",
            "model_manufacturer",
            "vehicle_image",
            "vehicle_daily_price",
            "vehicle_location",
            "location_area",
            "vehicle_city",
            "mileage",
            "fuel_type",
            "transmission",
            "slug",
        ]


class VehicleDetailSerializer(serializers.ModelSerializer):
    vehicle_main = VehicleSerializer(read_only=True)

    class Meta:
        model = VehicleDetails
        fields = [
            "vehicle_main",
            "vehicle_verified",
        ]
        lookup_field = "vehicle_main__slug"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class VehicleStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatistics
        fields = "__all__"


class TerminateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminateBooking
        fields = "__all__"


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDetails
        fields = "__all__"


class BookingListSerializer(serializers.ModelSerializer):
    renter = ShortUserSerializer(read_only=True)
    vehicle = VehicleListSerializer(read_only=True)
    terminate_bookings_set = TerminateBookingSerializer(read_only=True)
    booking_details_set = BookingDetailsSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "vehicle",
            "renter",
            "creation_date",
            "modification_date",
            "is_confirmed",
            "is_terminated",
            "booking_start_date",
            "booking_end_date",
            "terminate_bookings_set",
            "booking_details_set",
            "total_cost",
        )
