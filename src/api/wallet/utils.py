from .serializers import (
    WalletGetSerializer,
    WalletCreateSerializer,
    ConfirmCodeSerializer
)

serializer_action_classes = {
    "wallet_get": WalletGetSerializer,
    "wallet_get_detail": WalletGetSerializer,
    "create_wallet": WalletCreateSerializer,
    "activate_wallet": ConfirmCodeSerializer
}
