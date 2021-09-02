from bangazonreports.views.products.inexpensiveproducts import inexpensiveproduct_list
from bangazonreports.views.orders.incompleteorders import incompleteorder_list
from bangazonreports.views.orders.completedorders import completeorder_list
from django.urls import path
from .views import favoritedbycustomer_list, incompleteorder_list, inexpensiveproduct_list, completeorder_list

urlpatterns = [
    path('reports/favoritesellers', favoritedbycustomer_list),
    path('reports/incompleteorders', incompleteorder_list),
    path('reports/inexpensiveproducts', inexpensiveproduct_list),
    path('reports/completeorders', completeorder_list),
]
