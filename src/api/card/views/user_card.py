from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..card_action import serializer_action_classes
from rest_framework import serializers
from src.apps.card.models import Card
from ..serializers import CardGetSerializer
from src.apps.card.task import send_code_activate_card_task

@extend_schema(tags=["Card"])
class ClientCardViewSet(GenericViewSet):
    serializer_class = serializers.Serializer
    queryset = Card.objects.select_related('user').all()

    def get_serializer_class(self):
        return serializer_action_classes.get(self.action, super().get_serializer_class())

    def get_permissions(self):
        return [IsAuthenticated()]

    @action(methods=['post'], detail=False, url_path='card-create')
    def card_create(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        card = serializer.save()

        recipient = request.data.get("email") or getattr(request.user, "email", None)
        if not recipient:
            return Response(
                {"detail": "Recipient email not provided and user has no email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_code_activate_card_task.delay(recipient, request.user.id)
        except Exception as e:
            return Response(
                {
                    "detail": f"Card created but failed to queue activation email: {e}",
                    "wallet": CardGetSerializer(card).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": "Card created. Activation code sent to your email.",
                "wallet": CardGetSerializer(card).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['put'], detail=False, url_path='card-activate')
    def card_activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = serializer.save()
        return Response(CardGetSerializer(card).data)

    @action(methods=['get'], detail=False, url_path='card-get')
    def card_get(self, request):
        queryset = Card.objects.filter(user=request.user, is_active=True)
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, url_path='delete-card')
    def delete_card(self, request, pk=None):
        card = Card.objects.filter(id=pk).first()
        if not card:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

        card.is_active = False
        card.save(update_fields=["is_active"])

        return Response({
            "message": "Card deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)