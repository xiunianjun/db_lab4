"""canteen_order URL Configuration

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
from django.urls import re_path, include
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index 

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('canteen/', include('canteen.urls')),
    path('dish/', include('dish.urls')),
    path('customer/', include('customer.urls')),
    re_path(r'^', include('cms.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
