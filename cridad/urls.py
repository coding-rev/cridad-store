#PAYSTACK CONFIGURATIONS
import django

version = django.get_version().split(".")
if int(version[0]) >= 2:
    from django.urls import re_path as url, include
else:
    from django.conf.urls import url
    from django.conf.urls import url, include

from django.contrib import admin
from django.views.generic import TemplateView
from paystack.api import signals
from dispatch import receiver

@receiver(signals.successful_payment_signal)
def on_successful_payment(sender, **kwargs):
    import pdb

    pdb.set_trace()
    pass


if int(version[0]) > 1:
    paystack_route = url(
        "^paystack/",
        include(("paystack.frameworks.django.urls", "paystack"), namespace="paystack"),
    )
else:
    paystack_route = (
        url(
            r"^paystack/",
            include("paystack.frameworks.django.urls", namespace="paystack"),
        ),
    )


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
    paystack_route,
    path('', include('shop.urls')),
    path('register/', v.register, name="register"),
    url(r'^password/$', views.change_password, name='change_password'),
    path('', include("django.contrib.auth.urls")),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

