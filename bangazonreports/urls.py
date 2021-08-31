from django.urls import path
from .views import favoritedbycustomer_list

urlpatterns = [
    path('reports/favoritesellers', favoritedbycustomer_list),
]
