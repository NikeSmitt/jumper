from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('cart/', include('cartapp.urls')),
    path('order/', include('orderapp.urls', namespace='orderapp')),
    path('news/', include('newsapp.urls', namespace='newsapp'))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)