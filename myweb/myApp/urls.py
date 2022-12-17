from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_products, name='display_products'),
    path('create_table/', views.create_table, name='create_table'),
    path('insert_data/', views.insert_data, name='insert_data'),
    path('first_query/', views.first_query, name='first_query'),
    path('second_query/', views.second_query, name='second_query'),
    path('third_query/', views.third_query, name='third_query'),
    path('fourth_query/', views.fourth_query, name='fourth_query'),
]