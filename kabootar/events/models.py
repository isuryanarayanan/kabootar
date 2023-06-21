from django.db import models
from aws.models import SESEmailTemplate, TemplatedEmail
from django.conf import settings

class TemplateStackItem(models.Model):
    template = models.ForeignKey(
        SESEmailTemplate, on_delete=models.CASCADE, null=True, blank=True
    )

    priority = models.IntegerField(default=0)

    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SendEvent(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )

    email = models.EmailField()
    context = models.JSONField()

    def __str__(self):
        return self.event.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        template_stack = TemplateStackItem.objects.filter(
            event=self.event
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

          