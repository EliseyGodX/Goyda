from django.urls import path
from users.accounts.views import AccountPersonalView
app_name = 'accounts'

urlpatterns = [
    path('personal/', AccountPersonalView.as_view(), name='personal')
]