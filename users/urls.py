from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path("sign-up/", views.Users.as_view()),
    path("mypage/", views.Mypage.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("jwt-login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt-login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]