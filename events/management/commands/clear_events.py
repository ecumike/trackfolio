from django.core.management.base import BaseCommand, CommandError
from events.models import Event


def clearSampleData():
	Event.objects.all().delete()
	

class Command(BaseCommand):
	help = "Deletes all Events."
	
	def handle(self, *args, **options):
		clearSampleData()
		self.stdout.write(
			self.style.SUCCESS('Successfully removed all events.')
		)
