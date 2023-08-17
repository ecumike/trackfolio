import random 

from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from events.models import Event, EventLog


fakeEvents = ['Clean espresso machine', 'Haircut', 'Change HVAC filter', 'Change guitar strings', 'Trim cat nails']


def randomDate():
	'''
	Return a random datetime.
	'''
	start = timezone.now() - timedelta(days=500)
	end = timezone.now()
	
	return start + timedelta(
		seconds = random.randint(0, int((end - start).total_seconds()))
	)
	
	
def createNewEvents():
	for event_name in fakeEvents:
		try:
			newEvent = Event.objects.create(name=event_name)
		except Exception as ex:
			print(f'Event already exists: {event_name}')
	

def createSampleDataSet():
	'''
	Create companies
	Create (inbound #) random applications with all random data
	Minimum is 20, so we can randomly set declines and passes
	'''
	createNewEvents()
	
	events = Event.objects.all()
	
	# Create job postings
	for i in range(50):
		event = random.choice(events)
		
		EventLog.objects.create(
			date = randomDate(),
			event = event
		)
	

class Command(BaseCommand):
	help = "Generates a random sample data set for display purposes"
	
	def handle(self, *args, **options):
		createSampleDataSet()
		self.stdout.write(
			self.style.SUCCESS('Successfully created all sample data, open the app in your browser to view.')
		)

