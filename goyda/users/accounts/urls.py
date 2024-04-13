from django.urls import path
from users.accounts.views import (AccountsBrowseView, AccountsEditView,
                                  AccountsPersonalView)

app_name = 'accounts'

urlpatterns = [
    path('personal/', AccountsPersonalView.as_view(), name='personal'),
    path('edit/', AccountsEditView.as_view(), name='edit'),
    path('browse/<slug:username>/', AccountsBrowseView.as_view(), name='browse')
]