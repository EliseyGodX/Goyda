from django.urls import path, include
from users.views import UsersLoginView, UsersLogoutView, UsersRegistrationView
app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('registration/', UsersRegistrationView.as_view(), name='registration'),
    path('logout/', UsersLogoutView.as_view(), name='logout'),
    path('accounts/', include('users.accounts.urls', namespace='accounts')),
]