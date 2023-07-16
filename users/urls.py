from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("", views.UserAPIView.as_view(), name="signup"),
    path("<int:pk>/", views.UserDetailAPIView.as_view(), name="user_detail"),
]
