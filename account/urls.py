from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/<uuid:token>/', views.VerifyRegistrationView.as_view(), name='verify-registration'),

    path('login/', views.EmailLoginView.as_view(), name='email-login'),
    path('send-magic-link/', views.SendMagicLinkView.as_view(), name='send-magic-link'),
    path('magic-login/<uuid:token>/', views.MagicLinkLoginView.as_view(), name='magic-login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token-refresh')
]
