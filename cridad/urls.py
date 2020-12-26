#cridad/settings.py

from django.contrib import admin
from django.urls import path, include
from cridad import settings
from django.conf.urls import url

from shop import views
from register import views as v

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('register/', v.register, name="register"),
    url(r'^password/$', views.change_password, name='change_password'),
    path('', include("django.contrib.auth.urls")),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

