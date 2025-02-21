from django.urls import path
from .views import transaction_test_view

urlpatterns = [
    path('', transaction_test_view, name='transaction_test'),
]
