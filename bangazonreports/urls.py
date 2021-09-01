from bangazonreports.views.orders.incompleteorders import incompleteorder_list
from django.urls import path
from .views import favoritedbycustomer_list, incompleteorder_list

urlpatterns = [
    path('reports/favoritesellers', favoritedbycustomer_list),
    path('reports/incompleteorders', incompleteorder_list),
]