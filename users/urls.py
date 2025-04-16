from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    LogoutView,
    UserDetailView,
    ProfileUserView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', ProfileUserView.as_view(), name='profile_detail'),
]
