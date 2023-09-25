from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns=[
    #path('',Image.as_view(),name='upload-image'),
    path('', views.image, name='image-upload'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
