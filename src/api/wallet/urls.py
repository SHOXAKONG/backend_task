from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('wallet', views.WalletViewSet, 'wallet')

urlpatterns = [
    path('', include(router.urls))
]
