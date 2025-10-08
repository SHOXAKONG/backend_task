from .serializers import (
    CardGetSerializer,
    CardCreateSerializer,
    CardActivateSerializer
)

serializer_action_classes = {
    "card_create": CardCreateSerializer,
    "card_get": CardGetSerializer,
    "card_activate" : CardActivateSerializer,
}
