"""
URL configuration for jobmine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

#from events.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hijack/', include('hijack.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
    
    ## Map default favicon URL to static file location.
    re_path(r'^favicon.ico$', RedirectView.as_view(
        url=staticfiles_storage.url('shared/img/favicon.ico'),
        permanent=False),
        name='favicon'
    ),
    
    path('', RedirectView.as_view(url='/events/')),
    path('events/', include(('events.urls', 'events'))),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


