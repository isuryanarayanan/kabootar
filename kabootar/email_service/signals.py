import os
import boto3
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import EmailSesTemplate

@receiver(post_delete, sender=EmailSesTemplate)
def delete_ses_template(sender, instance, **kwargs):

    ses = instance.provider.client()

    mode = os.environ.get('GENIE_CONFIGURATION_KEY')

    template_name = f"{mode.upper()}-{instance.name}"

    ses.delete_template(TemplateName=template_name)
