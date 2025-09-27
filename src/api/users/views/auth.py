from django.contrib.auth import logout
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from src.api.users.serializers import UserSerializer
from ..actions import serializer_action_classes
from rest_framework_simplejwt.tokens import RefreshToken
from src.apps.users.models import User
from src.apps.users.task import send_html_email_task


@extend_schema(tags=["Auth"])
class AuthUserViewSet(viewsets.GenericViewSet):
    queryset = None
    lookup_field = "id"
    lookup_value_regex = "[0-9a-f-]{36}"
    serializer_class = serializers.Serializer

    def get_serializer_class(self):
        return serializer_action_classes.get(self.action, super().get_serializer_class())

    def get_permissions(self):
        if self.action in ['logout_view']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False, url_path='logout')
    def logout_view(self, request):
        logout(request)
        return Response({"message": "User Logout"}, status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='forgot-password')
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        send_html_email_task(user.email, user.id)
        return Response({
            "message": "We send code to your email",
            "id": user.id})

    @action(methods=['post'], detail=False, url_path='confirm-code')
    def confirm_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Code confirmed successfully"})

    @action(methods=['put'], detail=True, url_path='restore-password')
    def restore_password(self, request, id=None):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user=user)

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="google")
    def google(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        claims = serializer.validated_data["claims"]

        user, _ = User.objects.get_or_create(
            email=claims["email"],
            defaults={
                "first_name": claims.get("given_name", ""),
                "last_name": claims.get("family_name", ""),
            },
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True, url_path='set-password')
    def set_password(self, request, id=None):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"detail": "User not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user=user)
        return Response({
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='login/token-refresh')
    def token_refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
