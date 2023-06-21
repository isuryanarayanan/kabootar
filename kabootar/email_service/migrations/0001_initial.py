# Generated by Django 4.1.4 on 2023-06-21 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('EMAIL', 'EMAIL')], max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EmailSesTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('subject', models.TextField()),
                ('text_part', models.TextField()),
                ('html_part', models.TextField()),
                ('keys', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='EmailChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='email_service.channel')),
                ('provider', models.CharField(choices=[('SES', 'SES')], max_length=250)),
            ],
            bases=('email_service.channel',),
        ),
        migrations.CreateModel(
            name='EmailSesEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('data', models.JSONField(default=dict)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SENT', 'SENT'), ('FAILED', 'FAILED')], default='PENDING', max_length=250)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_service.emailsestemplate')),
            ],
        ),
        migrations.CreateModel(
            name='EmailSesProvider',
            fields=[
                ('emailchannel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='email_service.emailchannel')),
                ('access_key', models.CharField(max_length=250)),
                ('secret_key', models.CharField(max_length=250)),
                ('region', models.CharField(max_length=250)),
                ('sender', models.EmailField(max_length=254)),
            ],
            bases=('email_service.emailchannel',),
        ),
        migrations.AddField(
            model_name='emailsestemplate',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_service.emailsesprovider'),
        ),
    ]
