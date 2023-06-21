from django.db import models

CHANNEL_TYPES = (
    ('EMAIL', 'EMAIL'),
)

class Channel(models.Model):
    """
    Channels are the various ways in which you can send messages to users.
    """

    name = models.CharField(choices=CHANNEL_TYPES, max_length=250)
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

    template = models.ForeignKey(EmailSESTemplate, on_delete=models.CASCADE)

    priority = models.IntegerField(default=0)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return self.template.name + " - " + str(self.priority)

class Transaction(models.Model):
    """
    Holds templates and when user adds data for the template,
    events are created and sent accordingly.
    """

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    context = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        template_stack = TemplateStackItem.objects.filter(
            transaction=self
        ).order_by("-priority")

        for template in template_stack:
            if template.template.template_identifier in self.context:
                template_context = self.context[template.template.template_identifier]
                email = TemplatedEmail(
                    template=template.template,
                    email=self.email,
                    template_data=template_context
                )
                email.send()

   