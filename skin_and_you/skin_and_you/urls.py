"""
URL configuration for skin_and_you project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from api.account.views import SSLTempView

from skin_and_you import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('api.account.urls')),
    path('api/core/', include('api.core.urls')),    
    path('api/book/', include('api.appointment.urls')),
    path('api/inventory/', include('api.inventory.urls')),
    path('cms/', include('cms.urls')),
    path('.well-known/pki-validation/3DC5D868FC97A59CF7876FBC8A7F7957.txt', SSLTempView.as_view(), name='pki_validation'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
