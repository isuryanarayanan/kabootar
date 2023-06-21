from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmailSesProviderViewSet,
    EmailSesTemplateViewSet,
    TransactionViewSet,
    SendTransactionViewSet
)

router = DefaultRouter()
router.register(r'email-ses-providers', EmailSesProviderViewSet)
router.register(r'email-ses-templates', EmailSesTemplateViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'send-transactions', SendTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
