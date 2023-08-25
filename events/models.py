from datetime import timedelta

from django.db import models
from django.db.models import Avg, Q
from django.db.models.functions import Lower
from django.utils import timezone


def getToday():
	return timezone.now().date()


class Event(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)
	
	name = models.CharField(max_length=100, unique=True)
	average_interval_days = models.PositiveIntegerField(default=0, editable=False)
	
	class Meta:
		ordering = ['name']
		
	def __str__(self):
		return self.name
	
	
	def set_average_interval(self):
		# Last event - first event in days / # of events.
		try:
			thisEventLogs = self.event_log_event.all()
			lastEventDate = thisEventLogs.order_by('-date').first().date
			firstEventDate = thisEventLogs.order_by('date').first().date
			self.average_interval_days = (lastEventDate - firstEventDate).days / thisEventLogs.count()
			self.save()
		except Exception as ex:
			pass
		
		
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
		for i, event in enumerate(Event.objects.order_by(Lower('name'))):
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
		
		
	@staticmethod
	def get_create(event_id):
		if event_id.isdigit():
			try:
				event = Event.objects.get(id=event_id)
				return event
			except:
				raise Exception(f'Event with ID: {event_id} not found')
		else:
			try:
				event, created = Event.objects.get_or_create(name=event_id)
				return event
			except:
				raise Exception(f'Could not create event with name: {event_id}')
		
	
class EventLog(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)
	
	event = models.ForeignKey(Event, related_name='event_log_event', on_delete=models.CASCADE)
	date = models.DateField(default=getToday)
	
	class Meta:
		ordering = ['date']
		
	def __str__(self):
		return f'{self.event.name} - {self.date}'
	
	def save(self, *args, **kwargs):
		super(EventLog, self).save(*args, **kwargs)
		self.event.set_average_interval()
		

	@staticmethod
	def add_new(request):
		event_id = request.POST.get('event', None)
		event_date = request.POST.get('date', None)
		
		if not event_date:
			raise Exception('No event date specified')
			
		if event_id:
			event = Event.get_create(event_id)
		else:
			raise Exception('No event ID given')
		
		try:
			EventLog.objects.create(
				event = event,
				date = event_date,
			)
		except:
			raise Exception(f'Error creating event with ID: {event_id} and date {event_date}')
		
		
		