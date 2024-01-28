import uuid
from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):  # type: ignore
    """UserManager class."""

    # type: ignore
    def create_user(self, phone_number: str, password: Optional[str] = None) -> "User":
        """Create and return a `User` with an email, phone_number and password."""
        if phone_number is None:
            raise TypeError("Users must have a Phone Number.")

        # if email is None:
        #     raise TypeError("Users must have an email address.")

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number: str, password: str) -> "User":  # type: ignore
        """Create and return a `User` with superuser (admin) permissions."""
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


def phone_validator(value):
    if len(value) != 10 or value.isdigit() is False:
        raise ValidationError(
            ("Please Enter a valid phone number"),
            params={"value": value},
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(
        db_index=True,
        max_length=10,
        blank=False,
        null=False,
        unique=True,
        verbose_name="Phone Number",
        validators=[
            phone_validator,
        ],
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(null=True)
    full_name = models.CharField(max_length=300, null=True)
    birth_date = models.DateField(null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self) -> str:
        """Return a string representation of this `User`."""
        string = self.phone_number if self.phone_number != "" else self.get_full_name()
        return f"{self.id} {string}"

    @property
    def tokens(self) -> dict[str, str]:
        """Allow us to get a user's token by calling `user.token`."""
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def get_full_name(self) -> Optional[str]:
        """Return the full name of the user."""
        return self.full_name

    def get_short_name(self) -> str:
        """Return user phone_number."""
        return self.phone_number


class ProviderUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_vehicles = models.IntegerField("User Total Vehicles", default=0)
    total_earnings = models.IntegerField("User Total Earnings", default=0)
    total_expense = models.IntegerField("User Total Earnings", default=0)
