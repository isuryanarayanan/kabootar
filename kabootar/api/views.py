from rest_framework import viewsets
from .serializers import EmailSesProviderSerializer, EmailSesTemplateSerializer, TransactionSerializer, SendTransactionSerializer
from email_service.models import EmailSesProvider, EmailSesTemplate
from transactions.models import Transaction, SendTransaction

class EmailSesProviderViewSet(viewsets.ModelViewSet):
    queryset = EmailSesProvider.objects.all()
    serializer_class = EmailSesProviderSerializer

class EmailSesTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailSesTemplate.objects.all()
    serializer_class = EmailSesTemplateSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class SendTransactionViewSet(viewsets.ModelViewSet):
    queryset = SendTransaction.objects.all()
    serializer_class = SendTransactionSerializer
