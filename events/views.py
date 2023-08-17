from django.shortcuts import render

from events.models import Event


# Create your views here.
def home(request):
	context = {
		'chart_data': Event.get_timeline_data(),
	}
	return render(request, 'home.html', context)