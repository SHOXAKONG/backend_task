from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from src.api.users.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    AuthForgotPasswordSerializer,
    ConfirmCodeSerializer,
    RestorePasswordSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from src.apps.users.models import User
from src.apps.users.task import send_html_email_task


class AuthUserViewSet(viewsets.GenericViewSet):
    queryset = None
    lookup_field = "id"
    lookup_value_regex = "[0-9a-f-]{36}"

    def get_serializer_class(self):
        if self.action in ['register']:
            return UserRegisterSerializer
        elif self.action in ['forgot_password']:
            return AuthForgotPasswordSerializer
        elif self.action in ['confirm_code']:
            return ConfirmCodeSerializer
        elif self.action in ['restore_password']:
            return RestorePasswordSerializer
        return super().get_serializer_class()

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



