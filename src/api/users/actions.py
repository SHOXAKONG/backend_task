from .serializers import (
    UserRegisterSerializer,
    AuthForgotPasswordSerializer,
    ConfirmCodeSerializer,
    RestorePasswordSerializer,
    GoogleAuthSerializer,
    SetPasswordSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    UserListSerializer

)

serializer_action_classes = {
    "register": UserRegisterSerializer,
    "forgot_password": AuthForgotPasswordSerializer,
    "confirm_code": ConfirmCodeSerializer,
    "restore_password": RestorePasswordSerializer,
    "google": GoogleAuthSerializer,
    "set_password": SetPasswordSerializer,
    "login": LoginSerializer,
    "token_refresh": RefreshTokenSerializer,
    "users_list": UserListSerializer
}
