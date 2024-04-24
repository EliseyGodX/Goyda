from categories.views import LotsByCategory
from django.urls import path

app_name = 'category'

urlpatterns = [
    path('<slug:category_slug>', LotsByCategory.as_view(), name='category'),
]