from django.urls import path
from users.views import Login, UserRegistrationView
app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]