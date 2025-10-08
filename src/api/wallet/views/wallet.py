from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from src.apps.wallet.models import Wallet, Currency
from ..serializers import WalletGetSerializer
from ..utils import serializer_action_classes
from rest_framework import serializers
from src.apps.wallet.task import send_code_activate_wallet_task

@extend_schema(tags=["Wallet"])
class WalletViewSet(GenericViewSet):
    queryset = Wallet.objects.select_related('user')
    serializer_class = serializers.Serializer

    def get_serializer_class(self):
        return serializer_action_classes.get(self.action, super().get_serializer_class())

    def get_permissions(self):
        return [IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path='wallet-get')
    def wallet_get(self, request):
        queryset = self.get_queryset()

        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='wallet-get-detail')
    def wallet_get_detail(self, request, pk=None):
        queryset = Wallet.objects.filter(pk=pk, user=request.user)
        if request.user.is_staff:
            queryset = Wallet.objects.filter(pk=pk)
        wallet = get_object_or_404(queryset)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='create-wallet')
    def create_wallet(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        wallet = serializer.save()

        recipient = request.data.get("email") or getattr(request.user, "email", None)
        if not recipient:
            return Response(
                {"detail": "Recipient email not provided and user has no email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_code_activate_wallet_task.delay(recipient, request.user.id)
        except Exception as e:
            return Response(
                {
                    "detail": f"Wallet created but failed to queue activation email: {e}",
                    "wallet": WalletGetSerializer(wallet).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": "Wallet created. Activation code sent to your email.",
                "wallet": WalletGetSerializer(wallet).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['post'], detail=False, url_path='activate-wallet')
    def activate_wallet(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        wallet = serializer.save()
        return Response(WalletGetSerializer(wallet).data, status=status.HTTP_200_OK)
