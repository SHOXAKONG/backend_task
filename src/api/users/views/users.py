from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..serializers import UserSerializer

@extend_schema(tags=["Client"])
class ClientUserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=['get'], detail=False, url_path='user-profile')
    def user_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)