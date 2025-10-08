from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
router.register('auth-methods', views.AuthUserViewSet, 'auth')
router.register('users-control', views.AdminUserViewSet, 'users-control')
router.register('client', views.ClientUserViewSet, 'client')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
