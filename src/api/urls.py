from django.urls import path, include

urlpatterns = [
    path('', include('src.api.users.urls')),
    path('', include('src.api.wallet.urls')),
    path('', include('src.api.card.urls')),
    path('', include('src.api.payment.urls')),
]
