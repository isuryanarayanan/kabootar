import os
import boto3
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from aws.models import SESEmailTemplate


@receiver(post_save, sender=SESEmailTemplate)
def create_or_update_ses_template(sender, instance, created, **kwargs):
    ses = boto3.client('ses', region_name='ap-south-1')
    s3 = boto3.resource('s3')
    bucket_name = os.environ.get('AWS_S3_BUCKET')

    if not bucket_name:
        raise Exception("AWS S3 bucket name not found in environment variables")

    text_part_key = instance.template_text_part.name
    html_part_key = instance.template_html_part.name
    text_part_object = s3.Object(bucket_name, f"media/{text_part_key}")
    html_part_object = s3.Object(bucket_name, f"media/{html_part_key}")
    text_part = text_part_object.get()['Body'].read().decode('utf-8')
    html_part = html_part_object.get()['Body'].read().decode('utf-8')

    mode = os.environ.get('GENIE_CONFIGURATION_KEY')

    template_data = {
        'TemplateName': f"{mode.upper()}-{instance.template_identifier}",
        'SubjectPart': instance.template_subject,
        'TextPart': text_part,
        'HtmlPart': html_part
    }

    if created:
        ses.create_template(Template=template_data)
    else:
        ses.update_template(Template=template_data)


@receiver(post_delete, sender=SESEmailTemplate)
def delete_ses_template(sender, instance, **kwargs):
    ses = boto3.client('ses', region_name='ap-south-1')
    mode = os.environ.get('GENIE_CONFIGURATION_KEY')
    template_name = f"{mode.upper()}-{instance.template_identifier}"
    ses.delete_template(TemplateName=template_name)
