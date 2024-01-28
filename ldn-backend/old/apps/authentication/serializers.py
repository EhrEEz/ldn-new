from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .utils import validate_email as email_is_valid


class RegistrationSerializer(serializers.ModelSerializer[User]):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "password",
            "bio",
            "full_name",
        ]

    def validate_email(self, value: str) -> str:
        """Normalize and validate email address."""
        valid, error_text = email_is_valid(value)
        if not valid:
            raise serializers.ValidationError(error_text)
        try:
            email_name, domain_part = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain_part.lower()])

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )
        user.bio = validated_data.get("bio", "")
        user.email = validated_data.get("email", "")
        user.full_name = validated_data.get("full_name", "")
        user.save(update_fields=["bio", "full_name"])
        return user


class LoginSerializer(serializers.ModelSerializer[User]):
    # email = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=128, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        user = User.objects.get(phone_number=obj.phone_number)

        return {"refresh": user.tokens["refresh"], "access": user.tokens["access"]}

    class Meta:
        model = User
        fields = ["phone_number", "password", "tokens", "full_name"]

    def validate(self, data):  # type: ignore
        """Validate and return user login."""
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        if phone_number is None:
            raise serializers.ValidationError("A Phone number is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this phone_number and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user is not currently activated.")

        return user


class UserSerializer(serializers.ModelSerializer[User]):
    """Handle serialization and deserialization of User objects."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "password",
            "tokens",
            "bio",
            "full_name",
            "birth_date",
            "is_staff",
        )
        read_only_fields = ("tokens", "is_staff")

    def update(self, instance, validated_data):  # type: ignore
        """Perform an update on a User."""

        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer[User]):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type: ignore
        """Validate token."""
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type: ignore
        """Validate save backlisted token."""

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)
