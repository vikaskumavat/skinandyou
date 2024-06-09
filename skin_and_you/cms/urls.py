from django.urls import  path

from cms.views import download_prescription

trailing_slash = False


urlpatterns = [
    path('pdf/', download_prescription, name='pdf'),    
    
    path('prescription/pdf/', download_prescription, name='prescription_pdf'),    
    
    
]
