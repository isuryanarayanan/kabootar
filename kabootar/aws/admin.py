from django.contrib import admin
from aws.models import SESEmailTemplate, TemplatedEmail
# Register your models here.

admin.site.register(SESEmailTemplate)
# admin.site.register(TemplatedEmail)

@admin.register(TemplatedEmail)
class TemplatedEmailAdmin(admin.ModelAdmin):
    list_display = ('template', 'email', 'status')
    list_filter = ('template', 'status')

