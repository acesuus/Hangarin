from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Core
    path('', include('task.urls')),        # main app (homepage + models)
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),         # PWA assets (manifest, service worker)
    
    # Demo / Static pages
    path('charts/', TemplateView.as_view(template_name='charts.html'), name='charts'),
    path('tables/', TemplateView.as_view(template_name='tables.html'), name='tables'),

    # Authentication
    path('accounts/', include('allauth.urls')),
]
