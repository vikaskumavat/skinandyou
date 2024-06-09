from django.urls import  path
from api.account.views import ChangePasswordAPIView, LoginAPIView, PatientViewset, UserUploadByCSVAPIView, UserViewset, ProfileViewset, SSLTempView
from rest_framework_simplejwt import views as jwt_views

trailing_slash = False

urlpatterns = [    
    
    path('login', LoginAPIView.as_view(), name='login'),
    # path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('staff', UserViewset.as_view({'post': 'create', 'get': 'list'}), name='staff'),
    path('staff/<uuid:pk>', UserViewset.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='staff-list'),
    
    path('profile/', ProfileViewset.as_view(), name='profile'),
    path('change-password', ChangePasswordAPIView.as_view(), name='change-password'),
    
    
    path('user/change-password/<uuid:pk>', UserViewset.as_view({'post': 'change_password'}), name='change-password'),
    

    path('upload-user/', UserUploadByCSVAPIView.as_view(), name='upload-user'),    
    
    
    
    path('patient-list-for-table', PatientViewset.as_view({'get': 'list'}), name='patient-list'),
    
    path('patient/<uuid:pk>', PatientViewset.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='patient-list'),
]