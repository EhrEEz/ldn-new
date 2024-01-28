import pdb
from rest_framework import viewsets, exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from django.db.models import Q

from rest_framework.response import Response
from datetime import datetime

# from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import (
    Vehicle,
    VehicleDetails,
    Location,
    Booking,
    TerminateBooking,
    VehicleStatistics,
    BookingDetails,
)
from .serializers import (
    BookingDetailsSerializer,
    VehicleDetailSerializer,
    VehicleSerializer,
    VehicleListSerializer,
    LocationSerializer,
    BookingSerializer,
    TerminateBookingSerializer,
    VehicleStatisticsSerializer,
    BookingListSerializer,
)


class StatsCreateView(CreateAPIView):
    queryset = VehicleStatistics.objects.all()
    serializer_class = VehicleStatisticsSerializer
    permission_classes = (IsAuthenticated,)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = "slug"

    def createVehicleStatistic(vehicle):
        stat_data = {}
        stat_data["booking"] = vehicle.id
        stat_serializer = StatsCreateView.serializer_class(data=stat_data)
        stat_serializer.is_valid(raise_exception=True)
        fin = stat_serializer.save()
        return fin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        if serializer.is_valid():
            vehicle = serializer.save()
        detail = self.createVehicleStatistic(vehicle)
        return Response(
            {"main": vehicle, "detail": detail}, status=status.HTTP_201_CREATED
        )


class VehicleDetailsViewSet(viewsets.ModelViewSet):
    queryset = VehicleDetails.objects.all()
    serializer_class = VehicleDetailSerializer


class OpenVehicleView(ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleListSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(is_active=True)
        params = self.request.query_params
        params = params
        if params.get("location"):
            location_id = Location.objects.get(city=params.get("location"))
            queryset = queryset.filter(vehicle_city=location_id)

        if params.get('startDate') and params.get('endDate'):
            endDate_datetime = params.get('endDate')
            startDate_datetime = params.get('startDate')
            date_format = '%Y-%m-%d'
            start_date_obj = datetime.strptime(startDate_datetime, date_format)
            end_date_obj = datetime.strptime(endDate_datetime, date_format)
            queryset = queryset.exclude(Q(bookingvehicles__booking_end_date__lte=end_date_obj) & Q( bookingvehicles__booking_start_date__gte=start_date_obj)) 
        
        if len(params.getlist('fuel_type')) > 0:
            new_queryset = Vehicle.objects.none()
            for fuel_type in params.getlist('fuel_type'):
                new_queryset = (new_queryset | queryset.filter(fuel_type=fuel_type))
            queryset = new_queryset

        if len(params.getlist('transmission')) > 0:
            new_queryset = Vehicle.objects.none()
            for transmission in params.getlist('transmission'):
                new_queryset = (new_queryset | queryset.filter(transmission=transmission))
            queryset = new_queryset

        if len(params.getlist("location_area")) > 0:
            if 'filterInside' in params.getlist("location_area") and 'filterBoth' not in params.getlist("location_area"):
                queryset = queryset.filter(location_area=False)


        if params.get("mileageStart"):
            queryset = queryset.filter(mileage__gte=params.get("mileageStart"))
        if params.get("mileageEnd"):
            queryset = queryset.filter(mileage__lte=params.get("mileageEnd"))
        if params.get("filterSeatsStart"):
            queryset = queryset.filter(seats__gte=params.get("filterSeatsStart"))
        if params.get("filterSeatsEnd"):
            queryset = queryset.filter(seats__lte=params.get("filterSeatsEnd"))
        if params.get("priceStart"):
            queryset = queryset.filter(vehicle_daily_price__gte=params.get("priceStart"))
        if params.get("priceEnd"):
            queryset = queryset.filter(vehicle_daily_price__lte=params.get("priceEnd"))
        
        # pdb.set_trace()
        return queryset


class VehicleDetailView(RetrieveAPIView):
    queryset = VehicleDetails.objects.filter(vehicle_main__is_active=True)
    serializer_class = VehicleDetailSerializer
    lookup_field = "vehicle_main__slug"


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class BookingDetailsCreateView(CreateAPIView):
    queryset = BookingDetails.objects.all()
    serializer_class = BookingDetailsSerializer
    permission_classes = (IsAuthenticated,)


class BookingConfirmView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer

    def patch(self, request, *args, **kwargs):
        booking = request.data["booking"]
        booking_obj = Booking.objects.get(id=booking)
        booking_detail = BookingDetails.objects.get(booking=booking)

        if booking_obj.is_confirmed:
            Response(
                {"error": "Booking already confirmed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vehicle_owner = booking_obj.vehicle.vehicle_owner
        if request.user != vehicle_owner:
            return Response(
                {"error": "You cannot make this request"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        initial_odometer_reading = request.data["initial_odometer_reading"]
        booking_detail.odometer_reading_after = None
        booking_detail.odometer_reading_before = initial_odometer_reading
        booking_obj.is_confirmed = True
        booking_obj.save(update_fields=["is_confirmed"])
        booking_detail.save(
            update_fields=["odometer_reading_after", "odometer_reading_before"]
        )
        return Response(
            {"success": "Booking has been confirmed"}, status=status.HTTP_202_ACCEPTED
        )


class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        renter_user_data = {}
        renter_user_data.update(request.data)
        if request.user and request.user.is_authenticated:
            renter_user_data["renter"] = request.user.id
        else:
            raise exceptions(401, "Authentication Error")
        s = self.get_serializer(data=renter_user_data)
        s.is_valid(raise_exception=True)
        booking = s.save()
        headers = self.get_success_headers(s.data)
        detail_data = {}
        detail_data["booking"] = booking.id
        detail_serializer = BookingDetailsCreateView.serializer_class(data=detail_data)
        detail_serializer.is_valid(raise_exception=True)
        detail_serializer.save()

        vehicle = Vehicle.objects.get(id=request.data.get("vehicle"))
        vehicle.on_trip = True
        vehicle.save(update_fields=["on_trip"])
        return Response(
            {"main": s.data, "detail": detail_serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class StatisticsRetrieveView(RetrieveAPIView):
    queryset = TerminateBooking.objects.all()
    serializer_class = TerminateBookingSerializer


class CreatePaymentView(CreateAPIView):
    queryset = TerminateBooking.objects.all()
    serializer_class = TerminateBookingSerializer

    def updateVehicleStats(self, booking, amount):
        booking = Booking.objects.get(id=booking)
        vehicle = booking.vehicle
        stats_obj = VehicleStatistics.objects.get(vehicle=vehicle)
        booking_detail = BookingDetails.objects.get(booking=booking)
        total_earnings = stats_obj.total_earnings + amount
        total_rentals = stats_obj.total_rentals + 1
        distance_delta = (
            booking_detail.odometer_reading_after
            - booking_detail.odometer_reading_before
        )
        total_km_tracked = stats_obj.total_km_tracked + distance_delta
        stats_obj.total_earnings = total_earnings
        stats_obj.total_km_tracked = total_km_tracked
        stats_obj.total_rentals = total_rentals
        stats_obj.save(
            update_fields=["total_earnings", "total_km_tracked", "total_rentals"]
        )

    def create(self, request, *args, **kwargs):
        create_payment_data = {}
        create_payment_data.update(request.data)
        create_payment_data["end_type"] = 332
        serializer = self.get_serializer(data=create_payment_data)

        if serializer.is_valid():
            booking = request.data["booking"]
            if not Booking.objects.get(id=booking).is_confirmed:
                return Response(
                    {"error": "Booking is not confirmed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if request.data["final_odometer_reading"] is None:
                return Response(
                    {"error": "Final Odometer Reading needs to be set first"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            final_odometer_reading = request.data["final_odometer_reading"]

            booking_detail = BookingDetails.objects.get(booking=booking)
            booking_obj = Booking.objects.get(id=booking)
            booking_detail.odometer_reading_after = final_odometer_reading

            if booking_detail.odometer_reading_before is None:
                return Response(
                    {"error": "Initial Odometer Reading needs to be set first"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if booking_detail.odometer_reading_after is None:
                return Response(
                    {"error": "Final Odometer Reading needs to be set first"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if final_odometer_reading <= booking_detail.odometer_reading_before:
                return Response(
                    {
                        "error": "Final Odometer Reading is less than or same as the Initial Odometer Reading"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            amount = request.data["amount"]
            if amount < booking_obj.total_cost:
                return Response(
                    {
                        "code": "8900X",
                        "payment_not_enough": "Payment Amount is not Enough",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            booking_obj.is_terminated = True

            res = {}

            if amount > booking_obj.total_cost:
                res.update({"return_amount": amount - booking_obj.total_cost})
            booking_detail.save(update_fields=["odometer_reading_after"])
            self.updateVehicleStats(booking, booking_obj.total_cost)
            booking_obj.save(update_fields=["is_terminated"])
            booking_obj.is_terminated = True
            booking_obj.save(update_fields=["is_terminated"])
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res.update(serializer.data)
            vehicle = Vehicle.objects.get(id=booking_obj.vehicle.id)
            vehicle.on_trip = False
            vehicle.save(update_fields=["on_trip"])
            return Response(res, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBookingView(CreateAPIView):
    queryset = TerminateBooking.objects.all()
    serializer_class = TerminateBookingSerializer

    def create(self, request, *args, **kwargs):
        create_payment_data = {}
        create_payment_data.update(request.data)
        create_payment_data["end_type"] = 232
        serializer = self.get_serializer(data=create_payment_data)

        if serializer.is_valid():
            booking = request.data["booking"]
            if Booking.objects.get(id=booking).is_confirmed:
                return Response(
                    {"error": "Booking is confirmed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            booking_obj = Booking.objects.get(id=booking)
            booking_obj.is_terminated = True
            booking_obj.save(update_fields=["is_terminated"])
            # pdb.set_trace()
            vehicle = Vehicle.objects.get(id=booking_obj.vehicle.id)
            vehicle.on_trip = False
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            vehicle.save(update_fields=["on_trip"])
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVehiclesView(ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(vehicle_owner=self.request.user)
        return queryset


class UserBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        queryset = queryset.filter(renter=user, is_terminated=False)
        return queryset


class UserTerminatedBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        queryset = queryset.filter(renter=user, is_terminated=True)
        return queryset
