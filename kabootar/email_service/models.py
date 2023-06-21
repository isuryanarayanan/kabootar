import os
import boto3
import json
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

EMAIL_PROVIDERS = (
    ('SES', 'SES'),
)

EVENT_STATUS = (
    ('PENDING', 'PENDING'),
    ('SENT', 'SENT'),
    ('FAILED', 'FAILED'),
)

class EmailChannel(Channel):
    """
    Email Channels are the various ways in which you can send messages to users.
    """

    provider = models.CharField(choices=EMAIL_PROVIDERS, max_length=250)

    def __str__(self):
        return self.name

class EmailSesProvider(EmailChannel):
    """
    Email SES Provider is the AWS SES provider.
    """

    access_key = models.CharField(max_length=250)
    secret_key = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    sender = models.EmailField()

    def __str__(self):
        return self.name + " - " + self.description
    
    def client(self):
        AWS_ACCESS_KEY_ID = self.access_key
        AWS_SECRET_ACCESS_KEY = self.secret_key
        AWS_REGION = self.region

        ses = boto3.client(
            'ses',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        return ses
    
    def save(self, *args, **kwargs):
        self.check_access()
        self.load_templates()
        super().save(*args, **kwargs)

    def check_access(self):
        try:
            AWS_ACCESS_KEY_ID = self.access_key
            AWS_SECRET_ACCESS_KEY = self.secret_key
            AWS_REGION = self.region

            ses = boto3.client(
                'ses',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            ses.verify_email_identity(EmailAddress=self.sender)
        except Exception as e:
            raise Exception("The AWS SES provider is not configured properly")
    
    def load_templates(self):
        ses = self.client()

        try:
            response = ses.list_templates()
        except Exception as e:
            raise Exception("The AWS SES provider is not configured properly")

        mode = os.environ.get('GENIE_CONFIGURATION_KEY', None)
        template_prefix = str(mode).upper() + "-"

        templates = response['TemplatesMetadata']

        for template in templates:
            if template['Name'].startswith(template_prefix):
                template_name = template['Name']
                try:
                    template_response = ses.get_template(TemplateName=template_name)
                    template_data = template_response['Template']

                    name = template_name.split('-')[1]
                    subject = template_data['SubjectPart']
                    text_part = template_data['TextPart']
                    html_part = template_data['HtmlPart']

                    if not EmailSesTemplate.objects.filter(name=name).exists():
                        EmailSesTemplate.objects.create(
                            provider=self,
                            name=name,
                            subject=subject,
                            text_part=text_part,
                            html_part=html_part
                        )
                except Exception as e:
                    pass

    

class EmailSesTemplate(models.Model):
    """
    Email SES Template is the AWS SES template.
    """

    provider = models.ForeignKey(EmailSesProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    subject = models.TextField()
    text_part = models.TextField()
    html_part = models.TextField()
    keys = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        mode = os.environ.get('GENIE_CONFIGURATION_KEY', None)
        template_name = str(mode).upper() + "-" + self.name
        ses = self.provider.client()

        try:
            # Check if the template already exists
            ses.get_template(TemplateName=template_name)

            # If the template exists, update it
            ses.update_template(
                Template={
                    'TemplateName': template_name,
                    'SubjectPart': self.subject,
                    'TextPart': self.text_part,
                    'HtmlPart': self.html_part
                }
            )
        except ses.exceptions.TemplateDoesNotExistException:
            # If the template doesn't exist, create it
            try:
                ses.create_template(
                    Template={
                        'TemplateName': template_name,
                        'SubjectPart': self.subject,
                        'TextPart': self.text_part,
                        'HtmlPart': self.html_part
                    }
                )
            except Exception as e:
                raise Exception(e)
        except Exception as e:
            raise Exception(e)

        super().save(*args, **kwargs)
    


class EmailSesEvent(models.Model):
    """
    Email SES Event will handle sending emails.
    """

    email = models.EmailField()
    template = models.ForeignKey(EmailSesTemplate, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    status = models.CharField(
        max_length=250,
        choices=EVENT_STATUS,
        default='PENDING'
    )

    def __str__(self):
        return f"{self.email} - {self.template} - {self.status}"

    def get_template_identifier(self):
        mode = os.environ.get('GENIE_CONFIGURATION_KEY', None)
        return str(mode).upper()+"-"+self.template.name

    def save(self, *args, **kwargs):

        template_keys = self.template.keys
        template_data = self.data

        for key in template_keys:
            if key not in template_data:
                raise Exception(
                    "The template data is not correlated with the template keys")

        super(EmailSesEvent, self).save(*args, **kwargs)

    def send(self):
        try:
            
            ses = self.template.provider.client()
            template_identifier = self.get_template_identifier()
            template_data = self.data

            response = ses.send_templated_email(
                Source=self.template.provider.sender,
                Destination={
                    'ToAddresses': [
                        self.email,
                    ]
                },
                Template=template_identifier,
                TemplateData=json.dumps(template_data)
            )

            self.status = 'SENT'
            self.save()

        except Exception as e:
            self.status = 'FAILED'
            self.save()
            raise Exception(e)
