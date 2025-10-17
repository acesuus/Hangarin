from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Core
    path('admin/', admin.site.urls),
    path('', include('task.urls')),        # main app (homepage + models)
    path('', include('pwa.urls')),         # PWA assets (manifest, service worker)
    
    # Demo / Static pages
    path('charts/', TemplateView.as_view(template_name='charts.html'), name='charts'),
    path('tables/', TemplateView.as_view(template_name='tables.html'), name='tables'),

    # Authentication
    path('accounts/', include('allauth.urls')),
]
