from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload, specific_image, save_rotated_image

app_name = 'gallery'
urlpatterns = [
    path('', upload, name='upload'),
    path('image/<int:pk>/', specific_image, name='specific_image'),
    path('saverotatedimage/', save_rotated_image, name='save_rotated_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
