from django.contrib import admin
from .models import Event, TemplateStackItem, SendEvent

class TemplateStackItemInline(admin.TabularInline):
    model = TemplateStackItem

class EventAdmin(admin.ModelAdmin):
    inlines = [TemplateStackItemInline]

admin.site.register(Event, EventAdmin)
admin.site.register(SendEvent)
