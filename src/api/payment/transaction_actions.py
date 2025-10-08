from .serializers import (
    TransferByCardPToP,
    GetTransaction,
    TransactionWalletToWalletSerializer,
    GetDetailTransactionSerializer,
    TransactionWalletToCardSerializer,
    TransactionCardToWalletSerializer
)

serializer_action_classes = {
    "transfer_money": TransferByCardPToP,
    "get_transaction": GetTransaction,
    "get_detail_transaction": GetDetailTransactionSerializer,
    "transfer_money_wallet": TransactionWalletToWalletSerializer,
    "transfer_wallet_to_card": TransactionWalletToCardSerializer,
    "transfer_card_to_wallet": TransactionCardToWalletSerializer,
}
