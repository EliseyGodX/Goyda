from categories.views import LotsByCategoryView, CategoriesSearchView
from django.urls import path

app_name = 'categories'

urlpatterns = [
    path('<slug:category_slug>', LotsByCategoryView.as_view(), name='category'),
    path('search/<slug:category_slug>', CategoriesSearchView.as_view(), name='search')
]

