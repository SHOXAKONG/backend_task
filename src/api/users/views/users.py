from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..serializers import UserListSerializer
from src.apps.users.models import User
from rest_framework import status


class AdminUserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_permissions(self):
        if self.action in ['users_list']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(methods=['get'], detail=False, url_path='users-list')
    def users_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='user-detail')
    def users_detail(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
