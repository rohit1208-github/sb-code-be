# api/urls.py (update)
from django.urls import path, include
from .views import UserInfoView, CustomTokenObtainPairView, CustomTokenRefreshView, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('users/', include('users.urls')),
    path('management/', include('management.urls')),
    path('microsites/', include('microsites.urls')),
    path('content/', include('content.urls')),
    path('optimization/', include('optimization.urls')),
    path('analytics/', include('analytics.urls')),
]