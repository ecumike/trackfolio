from django.contrib import admin

from .models import Event, EventLog


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'updated_at', 'name')
	list_filter = ('created_at', 'updated_at')
	search_fields = ('name',)
	date_hierarchy = 'created_at'


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'updated_at', 'event', 'date')
	list_filter = ('created_at', 'updated_at', 'date')
	date_hierarchy = 'created_at'
	