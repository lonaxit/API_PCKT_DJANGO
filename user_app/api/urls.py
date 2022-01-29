from django.urls import path,include
from user_app.api.views import *

# 1
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import *

# import for jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 2 create url pattern

urlpatterns = [

    # urls for token authentication
    path('login/',obtain_auth_token, name='login'),
    path('register/',registration_view, name='register'),
    path('logout/',logout_view, name='logout'),
    
    
    # urls for jwt authentication comment out
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
]