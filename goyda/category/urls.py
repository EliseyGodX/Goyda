from django.urls import path
from category.views import LotsByCategory

app_name = 'category'

urlpatterns = [
    path('<slug:category_slug>', LotsByCategory.as_view(), name='category'),
]