from django.urls import path, include
from users.views import UsersLoginView, UsersLogoutView, UsersRegistrationView, UsersListView, UsersPasswordChangeView, UsersTrackPurchasesView
app_name = 'users'

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('accounts/', include('users.accounts.urls', namespace='accounts')),
    path('login/', UsersLoginView.as_view(), name='login'),
    path('registration/', UsersRegistrationView.as_view(), name='registration'),
    path('logout/', UsersLogoutView.as_view(), name='logout'),
    path('change-password/', UsersPasswordChangeView.as_view(), name='change_password'),
    path('track-purchases/', UsersTrackPurchasesView.as_view(), name='track_purchases'),
    path('track-sales/', UsersPasswordChangeView.as_view(), name='track_sales'),
    path('sell/', UsersPasswordChangeView.as_view(), name='sell'),
]