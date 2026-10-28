from rest_framework import serializers

from auth_app.models import CoderrUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Validates registration data and creates a user with its profile.
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CoderrUser

        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True, "allow_blank": False},
        }

    def validate_email(self, value):
        """
        Rejects an email that is already used by another user.
        """
        if CoderrUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def save(self):
        """
        Checks that both passwords match, creates the user with the email as username
        and creates the matching UserProfile.
        """
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "Passwords dont match. Please try again!"})

        account = CoderrUser(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            type=self.validated_data["type"],
        )
        account.set_password(pw)
        account.save()

        return account
