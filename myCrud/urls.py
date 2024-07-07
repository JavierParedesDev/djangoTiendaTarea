from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from tienda import views

from django.conf.urls.static import static
from tienda.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', include('tienda.urls')),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('dashboard/', dashboard, name='dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)