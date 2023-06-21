from django.contrib import admin
from .models import EmailSesProvider, EmailSesTemplate, EmailSesEvent

# Register your models here.

admin.site.register(EmailSesProvider)
admin.site.register(EmailSesTemplate)


@admin.register(EmailSesEvent)
class EmailSesEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'status', 'email')
