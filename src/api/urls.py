from django.urls import path, include

urlpatterns = [
    path('', include('src.api.users.urls'))
]