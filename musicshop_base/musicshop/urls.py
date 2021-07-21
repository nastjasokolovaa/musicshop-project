"""musicshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic import RedirectView
from mainapp import urls
from . import settings
from .views import main, contact

app_name = 'musicshop'


def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')

urlpatterns = [
    path('favicon.ico', okay),
    path('', main, name='index'),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('products/', include(urls, namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('', include('social_django.urls', namespace='social')),
    path('admin_staff/', include('adminapp.urls', namespace='admin_staff')),
    # path('order/', include('ordersapp.urls', namespace='order')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
