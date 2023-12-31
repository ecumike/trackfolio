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
	average_interval_days = models.PositiveIntegerField(default=0)
	next_event_date = models.DateField(null=True, blank=True)
	
	class Meta:
		ordering = ['name']
		
	def __str__(self):
		return self.name
	
	
	def set_next_event_date(self):
		if self.average_interval_days > 0:
			last_event_date = EventLog.objects.filter(event=self).only('date').order_by('-date').first().date
			self.next_event_date = last_event_date + timedelta(days=self.average_interval_days)
			self.save()
	
	
	def set_average_interval(self):
		# Last event - first event in days / # of events.
		try:
			this_event_logs = self.event_log_event.all()
			if this_event_logs.count() > 1:
				lastEventDate = this_event_logs.order_by('-date').first().date
				firstEventDate = this_event_logs.order_by('date').first().date
				self.average_interval_days = (lastEventDate - firstEventDate).days / (this_event_logs.count()-1)
				self.save()
		except Exception as ex:
			pass
		
		
	@staticmethod
	def get_timeline_data():
		"""
		Usage: d3
		Create an x-axis and date array for each event.
		The "y-tick-values" is simply used as a y-axis value for the date to separate
		the different data series into their own lines, else they would all be on one flat line.
		"""
		x_axis_mappings = {}
		y_tick_values = []
		columns = []
		comments = {}
		
		# Get unique event names, then create object for each with array of dates.
		for i, event in enumerate(Event.objects.order_by(Lower('name'))):
			x_axis_mappings[event.name] = f'{event.name}_x'
			y_tick_values.append(i)
			
			dates_arr =[f'{event.name}_x']
			values_arr =[event.name]
			comments[event.name] = []
			
			for event_log in event.event_log_event.only('date', 'comments').order_by('date'):
				dates_arr.append(event_log.date.strftime('%Y-%m-%d'))
				values_arr.append(i)
				comments[event.name].append(event_log.comments if event_log.comments else 'null')
				
			columns.extend([dates_arr, values_arr])
		
		# Return json data for timeline chart.
		return {
			'x': x_axis_mappings, 
			'columns': columns,
			'y_tick_values': y_tick_values,
			'comments': comments,
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
	comments = models.CharField(max_length=100, null=True, blank=True)
	
	class Meta:
		ordering = ['date']
		
	def __str__(self):
		return f'{self.event.name} - {self.date}'
	
	def save(self, *args, **kwargs):
		super(EventLog, self).save(*args, **kwargs)
		self.event.set_average_interval()
		self.event.set_next_event_date()
		

	@staticmethod
	def add_new(request):
		id = request.POST.get('event', None)
		date = request.POST.get('date', None)
		comments = request.POST.get('comments', None)
		
		if not date:
			raise Exception('No event date specified')
			
		if id:
			event = Event.get_create(id)
		else:
			raise Exception('No event ID given')
		
		try:
			EventLog.objects.create(
				date = date,
				event = event,
				comments = comments,
			)
		except:
			raise Exception(f'Error creating event with ID: {id} and date {date}')
		
		
		