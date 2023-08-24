from django.http import JsonResponse
from django.shortcuts import render


from events.models import Event, EventLog


# Create your views here.
def home(request):
	context = {
		'chart_data': Event.get_timeline_data(),
		'events': Event.objects.only('name'),
	}
	return render(request, 'home.html', context)
	
	
def add_event_log(request):
	try:
		EventLog.add_new(request)
	except Exception as ex:
		return JsonResponse({
			'result': f'{ex}'
		})
	
	return JsonResponse({
		'chart_data': Event.get_timeline_data()
	})
	