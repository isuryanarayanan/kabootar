from django.db import models
from transactions.models import Channel

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
        return self.name
    
class EmailSesTemplate(models.Model):
    """
    Email SES Template is the AWS SES template.
    """

    provider = models.ForeignKey(EmailSESProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    subject = models.TextField()
    text_part = models.TextField()
    html_part = models.TextField()
    keys = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class EmailSESEvent(models.Model):
    """
    Email SES Event will handle sending emails.
    """

    email = models.EmailField()
    template = models.ForeignKey(EmailSESTemplate, on_delete=models.CASCADE)
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
        return str(mode).upper()+"-"+self.template.template_identifier

    def save(self, *args, **kwargs):

        template_keys = self.template.keys
        template_data = self.data

        for key in template_keys:
            if key not in template_data:
                raise Exception(
                    "The template data is not correlated with the template keys")

        super(EmailSESEvent, self).save(*args, **kwargs)

    def send(self):
        try:
            AWS_ACCESS_KEY_ID = self.template.provider.access_key
            AWS_SECRET_ACCESS_KEY = self.template.provider.secret_key
            AWS_REGION = self.template.provider.region

            ses = boto3.client(
                'ses',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )

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
