from rest_framework import serializers
from email_service.models import EmailSesProvider, EmailSesTemplate
from transactions.models import Transaction, SendTransaction, TransactionTemplate

class EmailSesProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSesProvider
        fields = '__all__'

class EmailSesTemplateSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(write_only=True)

    class Meta:
        model = EmailSesTemplate
        fields = [
            'name',
            'subject',
            'text_part',
            'html_part',
            'keys',
            'provider_name'
        ]
    
    def create(self, validated_data):
        provider_name = validated_data.pop('provider_name', None)

        if provider_name is None:
            raise serializers.ValidationError("Provider name is required")

        try:
            provider = EmailSesProvider.objects.get(name=provider_name)
        except EmailSesProvider.DoesNotExist:
            raise serializers.ValidationError("Provider does not exist")

        validated_data['provider'] = provider

        return super().create(validated_data)


class TransactionTemplateSerializer(serializers.ModelSerializer):

    template = serializers.CharField(write_only=True)

    class Meta:
        model = TransactionTemplate
        fields = ['template', 'priority']

class TransactionSerializer(serializers.ModelSerializer):
    stack = TransactionTemplateSerializer(many=True, write_only=True)

    class Meta:
        model = Transaction
        fields = ['name', 'description', 'stack']

    def create(self, validated_data):
        stack_data = validated_data.pop('stack')
        transaction = Transaction.objects.create(**validated_data)

        for item in stack_data:
            template = EmailSesTemplate.objects.get(name=item['template'])
            TransactionTemplate.objects.create(
                transaction=transaction,
                template=template,
                priority=item['priority']
            )

        return transaction


class SendTransactionSerializer(serializers.ModelSerializer):

    transaction = serializers.CharField(write_only=True)

    class Meta:
        model = SendTransaction
        fields = ['transaction', 'email', 'context']

    def create(self, validated_data):
        transaction_name = validated_data.pop('transaction', None)

        if transaction_name is None:
            raise serializers.ValidationError("Transaction name is required")

        try:
            transaction = Transaction.objects.get(name=transaction_name)
        except Transaction.DoesNotExist:
            raise serializers.ValidationError("Transaction does not exist")

        validated_data['transaction'] = transaction

        return super().create(validated_data)