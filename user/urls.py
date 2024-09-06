
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("user/create/", views.UserCreateViewSet.as_view({"post": "create"} ), name='user_creation_viewset'),
    path("user/", views.UserViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name='user_viewset'),
    path("user/reset-password/", views.UserPasswordResetViewSet.as_view({"post": "update"}), name='user_reset_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

