import pandas as pd

from datetime import timedelta

from django.db import models
from django.db.models import Avg, Q
from django.utils import timezone


def getToday():
	return timezone.now().date()


class Event(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)
	
	name = models.CharField(max_length=100, unique=True)
	
	class Meta:
		ordering = ['name']
		
	def __str__(self):
		return self.name
	
	
	@staticmethod
	def get_timeline_data():
		"""
		Usage: d3
		Create an x-axis and date array for each event.
		"""
		x_axis_mappings = {}
		y_tick_values = []
		columns = []
		
		# Get unique event names, then create object for each with array of dates.
		for i, event in enumerate(Event.objects.order_by('name')):
			x_axis_mappings[event.name] = f'{event.name}_x'
			y_tick_values.append(i)
			
			dates_arr =[f'{event.name}_x']
			values_arr =[event.name]
						
			for event_date in event.event_log_event.values_list('date', flat=True).order_by('date'):
				dates_arr.append(event_date.strftime('%Y-%m-%d'))
				values_arr.append(i)
				
			columns.extend([dates_arr, values_arr])
		
		# Return json data for timeline chart.
		return {
			'x': x_axis_mappings, 
			'columns': columns,
			'y_tick_values': y_tick_values,
		}
	
	
class EventLog(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)
	
	event = models.ForeignKey(Event, related_name='event_log_event', on_delete=models.CASCADE)
	date = models.DateField(default=getToday)
	
	class Meta:
		ordering = ['date']
		
	def __str__(self):
		return f'{self.event.name} - {self.date}'
	

	