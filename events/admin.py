from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title','localization', 'active', 'author')
    list_filter = ('active', 'date_start', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Event, EventAdmin)