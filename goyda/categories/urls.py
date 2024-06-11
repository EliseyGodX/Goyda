from categories.views import LotsByCategoryView
from django.urls import path

app_name = 'categories'

urlpatterns = [
    path('<slug:category_slug>', LotsByCategoryView.as_view(), name='category'),
]

