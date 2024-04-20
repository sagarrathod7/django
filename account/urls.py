from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegisterationsView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password_change/', views.UserChangePasswordView.as_view(), name='password_change'),
    path('password_rest_link/', views.SendPasswordRestEmailView.as_view(), name='password_rest_link'),
    path('password_rest/<uid>/<token>', views.RestPasswordConfirmView.as_view(), name='password_rest'),
    
]
