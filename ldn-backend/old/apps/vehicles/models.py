from django.db import models
from django.contrib import admin
import uuid
from django.utils.text import slugify
from apps.authentication.models import User
from datetime import datetime, timezone
import pdb

# Create your models here.


class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-creation_date", "-modification_date"]


class Location(models.Model):
    city = models.CharField("City Name", max_length=200)

    def __str__(self):
        return self.city


class Vehicle(BaseModel):
    AUTO = "AT"
    MANUAL = "MN"
    AUTO_MANUAL = "AM"
    TRANSMISSION_TYPES = [
        (AUTO, "Automatic"),
        (MANUAL, "Manual"),
        (AUTO_MANUAL, "Automatic Manual"),
    ]

    ELECTRIC = "EV"
    HYBRID = "HV"
    FUEL_PETROL = "PF"
    FUEL_DIESEL = "DF"
    HYDROGEN = "HY"

    FUEL_TYPE = [
        (ELECTRIC, "Electric Vehicle"),
        (FUEL_PETROL, "Petrol Fuel"),
        (FUEL_DIESEL, "Diesel Fuel"),
        (HYBRID, "Hybrid Electric and Fuel"),
        (HYDROGEN, "Hydrogen Power"),
    ]
    name = models.CharField("Vehicle Name", max_length=100)
    reg_no = models.CharField("Vehicle Registration Number", max_length=20, unique=True)
    on_trip = models.BooleanField(
        "Vehicle is on trip", default=False, null=False, blank=False
    )
    seats = models.IntegerField("Vehicle Seat Limit")
    color_name = models.CharField("Vehicle Color Name", max_length=50)
    color_code = models.CharField("Vehicle Color Code", max_length=6)
    model_name = models.CharField("Vehicle Model Name", max_length=100)
    model_manufacturer = models.CharField("Vehicle Model Manufacturer", max_length=100)
    is_active = models.BooleanField(
        "Vehicle is active", default=True, null=False, blank=False
    )
    slug = models.TextField("Vehicle Slug", unique=True, null=False, blank=True)
    vehicle_image = models.ImageField("Vehicle Image", upload_to="vehicle_image")
    vehicle_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Vehicle Owner"
    )
    vehicle_daily_price = models.DecimalField(
        "Vehicle Price",
        max_digits=6,
        decimal_places=2,
        help_text="Cost of renting the Vehicle for a day",
    )
    location_area = models.BooleanField("Inside Area", default=False)
    vehicle_city = models.ForeignKey(
        Location, verbose_name="Vehicle City", on_delete=models.CASCADE
    )
    vehicle_location = models.CharField("Location", max_length=200)
    transmission = models.CharField(
        "Transmission Type", max_length=200, choices=TRANSMISSION_TYPES, default=MANUAL
    )
    fuel_type = models.CharField(
        "Fuel Type", max_length=200, choices=FUEL_TYPE, default=FUEL_PETROL
    )
    mileage = models.IntegerField("Mileage")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        *args,
        **kwargs,
    ):
        self.is_active = True
        if self.color_name is None or self.color_name == "":
            self.color_name = self.color_code
        if self.slug is None or self.slug == "":
            self.slug = slugify(f"{self.name}-{self.reg_no}")
        if update_fields is not None and (
            "reg_no" in update_fields or "name" in update_fields
        ):
            update_fields = {"slug"}.union(update_fields)

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            *args,
            **kwargs,
        )

    def __str__(self):
        return f"{self.name} {self.reg_no}"

    class Meta:
        ordering = ["-modification_date", "-creation_date", "name"]
        verbose_name_plural = "Vehicles"


class VehicleDetails(BaseModel):
    vehicle_main = models.OneToOneField(
        Vehicle, on_delete=models.CASCADE, related_name="vehicle", primary_key=True
    )
    registration_document = models.ImageField(
        "Vehicle Bluebook Information", upload_to="vehicle_details"
    )
    vehicle_verified = models.BooleanField("Vehicle Verification", default=False)
    security_deposit = models.IntegerField(
        "Security Deposit",
    )
    driving_limit = models.IntegerField("Driving Limit")

    def __str__(self):
        vehicle = self.vehicle_main.__str__()
        return f"{vehicle} Details"
    
    @admin.display(boolean=True)
    def vehicle_name(self):
        v_name = self.vehicle_main.name
        return f"{v_name}"


class Booking(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_staff": False}
    )
    is_confirmed = models.BooleanField("Booking Confirmed", default=False, null=True)
    booking_start_date = models.DateField("Booking Start Date")
    booking_end_date = models.DateField("Booking End Date")
    booking_total_days = models.IntegerField("Booking Duration", null=True, blank=True)
    is_terminated = models.BooleanField(
        "Booking is Terminated", null=True, default=False
    )
    total_cost = models.IntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'"{self.vehicle.name}" booking by "{self.renter.phone_number}" from "{self.booking_start_date}" to "{self.booking_end_date}"'

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        *args,
        **kwargs,
    ):
        delta = self.booking_end_date - self.booking_start_date
        self.booking_total_days = delta.days
        total = self.vehicle.vehicle_daily_price * delta.days
        self.total_cost = total

        if update_fields is not None and (
            "booking_end_date" in update_fields
            or "booking_start_date" in update_fields
            or "total_cost"
        ):
            update_fields = {"total_cost", "booking_total_days"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            *args,
            **kwargs,
        )


class BookingDetails(BaseModel):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, verbose_name="Booking", primary_key=True, related_name="booking_details_set"
    )
    odometer_reading_before = models.IntegerField(
        "Odometer Reading at Start of Trip", null=True, blank=True
    )
    odometer_reading_after = models.IntegerField(
        "Odometer Reading at End of Trip", null=True, blank=True
    )
    notes = models.TextField("Notes on delivery", null=True, blank=True)


class TerminateBooking(BaseModel):
    class TerminationType(models.IntegerChoices):
        PAYMENT = 332
        CANCEL = 232

    end_type = models.IntegerField(
        choices=TerminationType.choices, verbose_name="Termination Type"
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        verbose_name="Payment for booking",
        related_name="terminate_bookings_set",
        primary_key=True,
    )
    amount = models.IntegerField("Payment Amount", default=0)
    handshake = models.BooleanField("Renter Rentee Handshake", default=False)


class VehicleStatistics(BaseModel):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, primary_key=True)

    total_earnings = models.DecimalField(
        "Total Earnings till Date", decimal_places=0, max_digits=16, default=0
    )
    total_expense = models.DecimalField(
        "Total Expense till Date", decimal_places=0, max_digits=16, default=0
    )
    total_km_tracked = models.IntegerField("Total KMs travelled so far", default=0)
    total_rentals = models.IntegerField("Total Rentals Till Date", default=0)
    total_turnover = models.IntegerField("Vehicle Turnover", default=0)

    # Automatic fields
    # Average Expense
    average_expense_per_day = models.DecimalField(
        "Average Daily Expense", decimal_places=0, max_digits=16, default=0
    )
    average_expense_per_rental = models.DecimalField(
        "Average Expense per Rental", decimal_places=0, max_digits=16, default=0
    )
    average_expense_per_distance = models.DecimalField(
        "Average Expense per Distance", decimal_places=0, max_digits=16, default=0
    )
    # Average Income
    average_income_per_day = models.DecimalField(
        "Average Daily Income", decimal_places=0, max_digits=16, default=0
    )
    average_income_per_rental = models.DecimalField(
        "Average Income per Rental", decimal_places=0, max_digits=16, default=0
    )
    average_income_per_distance = models.DecimalField(
        "Average Income per Distance", decimal_places=0, max_digits=16, default=0
    )

    # Turnover
    average_turnover_per_day = models.DecimalField(
        "Average Daily Turnover", decimal_places=0, max_digits=16, default=0
    )
    average_turnover_per_rental = models.DecimalField(
        "Average Turnover per Rental", decimal_places=0, max_digits=16, default=0
    )
    average_turnover_per_distance = models.DecimalField(
        "Average Turnover per Distance", decimal_places=0, max_digits=16, default=0
    )

    # Utils
    def getLifeTime(self):
        creation_date = self.vehicle.creation_date
        today = datetime.now(timezone.utc)
        delta = today - creation_date
        lifetime = delta.days
        return lifetime

    def getAverageEarningPerDay(self):
        life_time = self.getLifeTime()
        if life_time <= 0:
            return 0
        return self.total_earnings / life_time

    def getAverageEarningPerDistance(self):
        total_km = self.total_km_tracked
        if total_km <= 0:
            return 0
        return self.total_earnings / total_km

    def getAverageEarningPerRental(self):
        total_rentals = self.total_rentals
        if total_rentals <= 0:
            return 0
        return self.total_earnings / total_rentals

    def getAverageExpensePerDay(self):
        life_time = self.getLifeTime()
        if life_time <= 0:
            return 0
        return self.total_expense / life_time

    def getAverageExpensePerDistance(self):
        total_km = self.total_km_tracked
        if total_km <= 0:
            return 0
        return self.total_expense / total_km

    def getAverageExpensePerRental(self):
        total_rentals = self.total_rentals
        if total_rentals <= 0:
            return 0
        return self.total_expense / total_rentals

    def getAverageTurnoverPerDay(self):
        life_time = self.getLifeTime()
        if life_time <= 0:
            return 0
        return self.total_turnover / life_time

    def getAverageTurnoverPerDistance(self):
        total_km = self.total_km_tracked
        if total_km <= 0:
            return 0
        return self.total_turnover / total_km

    def getAverageTurnoverPerRental(self):
        total_rentals = self.total_rentals
        if total_rentals <= 0:
            return 0
        return self.total_turnover / total_rentals

    def updateExpenses(self):
        self.average_expense_per_day = self.getAverageExpensePerDay()
        self.average_expense_per_rental = self.getAverageExpensePerRental()
        self.average_expense_per_distance = self.getAverageExpensePerDistance()

    def updateEarnings(self):
        self.average_income_per_day = self.getAverageEarningPerDay()
        self.average_income_per_rental = self.getAverageEarningPerRental()
        self.average_income_per_distance = self.getAverageEarningPerDistance()

    def updateTurnover(self):
        self.average_turnover_per_day = self.getAverageTurnoverPerDay()
        self.average_turnover_per_rental = self.getAverageTurnoverPerRental()
        self.average_turnover_per_distance = self.getAverageTurnoverPerDistance()

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        *args,
        **kwargs,
    ):
        if update_fields is not None and (
            "total_km_tracked" in update_fields or "total_rentals" in update_fields
        ):
            self.updateEarnings()
            self.updateExpenses()
            self.updateTurnover()
            update_fields = {
                "average_expense_per_day",
                "average_expense_per_rental",
                "average_expense_per_distance",
                "average_income_per_day",
                "average_income_per_rental",
                "average_income_per_distance",
                "average_turnover_per_day",
                "average_turnover_per_rental",
                "average_turnover_per_distance",
            }.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
            *args,
            **kwargs,
        )

        if update_fields is not None and ("total_earnings" in update_fields):
            self.updateEarnings()
            self.updateTurnover()

            update_fields = {
                "average_income_per_day",
                "average_income_per_rental",
                "average_income_per_distance",
                "average_turnover_per_day",
                "average_turnover_per_rental",
                "average_turnover_per_distance",
            }.union(update_fields)
            super().save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
                *args,
                **kwargs,
            )

        if update_fields is not None and ("total_expense" in update_fields):
            self.updateExpenses()
            self.updateTurnover()
            update_fields = {
                "average_expense_per_day",
                "average_expense_per_rental",
                "average_expense_per_distance",
                "average_turnover_per_day",
                "average_turnover_per_rental",
                "average_turnover_per_distance",
            }.union(update_fields)
            super().save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
                *args,
                **kwargs,
            )
