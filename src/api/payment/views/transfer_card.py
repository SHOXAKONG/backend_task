from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers

from src.apps.common.pagination import CustomPagination
from ..serializers import GetDetailTransactionSerializer
from ..transaction_actions import serializer_action_classes
from rest_framework.response import Response
from src.apps.payment.models import Transaction

@extend_schema(tags=["Transfer"])
class CardTransferViewSet(GenericViewSet):
    serializer_class = serializers.Serializer
    queryset = Transaction.objects.select_related(
        'currency', 'receiver_card', 'sender_card', 'receiver_wallet', 'sender_wallet'
    )
    pagination_class = CustomPagination

    def get_serializer_class(self):
        return serializer_action_classes.get(self.action, super().get_serializer_class())

    def get_permissions(self):
        return [IsAuthenticated()]

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='transfer-card-to-card')
    def transfer_money(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Money Transfer Finished Successfully"})

    @action(methods=['get'], detail=False, url_path='get-all-transactions')
    def get_transaction(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if not request.user.is_staff:
            user_filter = Q(
                sender_wallet__user=request.user
            ) | Q(
                receiver_wallet__user=request.user
            ) | Q(
                sender_card__user=request.user
            ) | Q(
                receiver_card__user=request.user
            )
            queryset = queryset.filter(user_filter)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get-detail-transaction')
    def get_detail_transaction(self, request, pk=None):
        queryset = Transaction.objects.get(id=pk)

        if not queryset:
            raise ValidationError("Transaction Not Found")

        if not request.user.is_staff:
            allowed = Q(sender_wallet__user=request.user) | Q(receiver_wallet__user=request.user) | \
                      Q(sender_card__user=request.user) | Q(receiver_card__user=request.user)
            if not Transaction.objects.filter(Q(id=pk) & allowed).exists():
                return Response(
                    {"detail": "You are not authorized to view this transaction."},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='transfer-wallet-to-wallet')
    def transfer_money_wallet(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_obj = serializer.save()
        return Response(GetDetailTransactionSerializer(transaction_obj).data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='transfer-wallet-to-card')
    def transfer_wallet_to_card(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_obj = serializer.save()
        return Response(GetDetailTransactionSerializer(transaction_obj).data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='transfer-card-to-wallet')
    def transfer_card_to_wallet(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_obj = serializer.save()
        return Response(GetDetailTransactionSerializer(transaction_obj).data, status=status.HTTP_200_OK)