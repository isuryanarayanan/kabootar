from rest_framework import serializers
from email_service.models import EmailSesProvider, EmailSesTemplate
from transactions.models import Transaction, SendTransaction, TransactionTemplate

class EmailSesProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSesProvider
        fields = '__all__'
    
    def validate(self, data):
        if data['access_key'] is None:
            raise serializers.ValidationError("Access key is required")
        
        if data['secret_key'] is None:
            raise serializers.ValidationError("Secret key is required")
        
        if data['region'] is None:
            raise serializers.ValidationError("Region is required")
        
        return data
    
    def create(self, validated_data):
        return super().create(validated_data)

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
    
    def validate_template(self, value):
        try:
            template = EmailSesTemplate.objects.get(name=value)
        except EmailSesTemplate.DoesNotExist:
            raise serializers.ValidationError("Template does not exist")
        
        return template.name

class TransactionSerializer(serializers.ModelSerializer):
    stack = TransactionTemplateSerializer(many=True, write_only=True)

    class Meta:
        model = Transaction
        fields = ['name', 'description', 'stack']

    def create(self, validated_data):
        stack_data = validated_data.pop('stack')

        if len(stack_data) == 0:
            raise serializers.ValidationError("Stack is required")
        
        if TransactionTemplateSerializer(data=stack_data, many=True).is_valid() is False:
            raise serializers.ValidationError("Invalid stack")

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