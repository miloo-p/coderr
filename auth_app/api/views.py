from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CoderrUser
from .permissions import IsOwnerOfProfile
from .serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)


class RegistrationView(APIView):
    """
    View to register a new user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new user and returns the auth token together with the user data.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """
    View to login a user.
    """

    def post(self, request):
        """
        Logs the user in and returns the auth token together with the user data.
        """
        login_data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
        }
        serializer = self.serializer_class(data=login_data, context={"request": request})

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfProfile]

    def get(self, request, pk):
        """
        Returns a single Profile.
        """
        user = get_object_or_404(CoderrUser, pk=pk)
        self.check_object_permissions(request, user)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Updates profile owner profile values (partial allowed).
        """
        user = get_object_or_404(CoderrUser, pk=pk)
        self.check_object_permissions(request, user)
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a list of profiles.
        """
        profiles = CoderrUser.objects.filter(type=self.profile_type)
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data)


class BusinessProfilesListView(ProfilesListView):
    profile_type = "business"
    serializer_class = BusinessProfileSerializer


class CustomerProfilesListView(ProfilesListView):
    profile_type = "customer"
    serializer_class = CustomerProfileSerializer
