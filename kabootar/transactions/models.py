from django.db import models
from email_service.models import EmailSesTemplate, EmailSesEvent

class Transaction(models.Model):
    """
    Holds templates and when user adds data for the template,
    events are created and sent accordingly.
    """

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class TransactionTemplate(models.Model):
    """
    Holds single template and its priority in the stack.
    """

    # Since only email is supported for now, we can use the same model.
    # Else, we can create a new model for each channel type. And use
    # a generic foreign key to point to the template.

    template = models.ForeignKey(EmailSesTemplate, on_delete=models.CASCADE)

    priority = models.IntegerField(default=0)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)

    def __str__(self):
        return self.template.name + " - " + str(self.priority)

    
class SendTransaction(models.Model):
    """
    Holds the data for the transaction. When user adds data for the
    transaction, events are created and sent accordingly.
    """

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    email = models.EmailField()
    context = models.JSONField()

    def __str__(self):
        return self.transaction.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        template_stack = TransactionTemplate.objects.filter(
            transaction=self.transaction
        ).order_by("-priority")

        for template in template_stack:
            if template.template.name in self.context:
                template_context = self.context[template.template.name]
                email = EmailSesEvent(
                    template=template.template,
                    email=self.email,
                    data=template_context
                )
                
                email.send()
            else:
                raise Exception("Template data is not provided, or is not in the correct format.")
  