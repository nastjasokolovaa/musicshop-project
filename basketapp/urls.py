from django.urls import path
from .views import basket, basket_add, basket_remove, basket_remove_all, basket_edit

app_name = 'basketapp'

urlpatterns = [
    path('', basket, name='basket'),
    path('add/<int:pk>/', basket_add, name='basket_add'),
    path('remove/<int:pk>/', basket_remove, name='basket_remove'),
    path('remove/', basket_remove_all, name='basket_remove_all'),
    path('edit/<int:pk>/<int:quantity>/', basket_edit, name='basket_edit'),
]
