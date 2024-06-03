from django.urls import include, path
from users.views import (UsersListView, UsersLoginView, UsersLogoutView,
                         UsersPasswordChangeView, UsersRegistrationView,
                         UsersTrackPurchasesView, UsersTrackSalesView)

app_name = 'users'

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('accounts/', include('users.accounts.urls', namespace='accounts')),
    path('login/', UsersLoginView.as_view(), name='login'),
    path('registration/', UsersRegistrationView.as_view(), name='registration'),
    path('logout/', UsersLogoutView.as_view(), name='logout'),
    path('change-password/', UsersPasswordChangeView.as_view(), name='change_password'),
    path('track-purchases/', UsersTrackPurchasesView.as_view(), name='track_purchases'),
    path('track-sales/', UsersTrackSalesView.as_view(), name='track_sales'),
]