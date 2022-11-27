from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorite, name='favorite'),
    path('add_favorite/<int:product_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite_item/<int:product_id>/', views.remove_favorite_item, name='remove_favorite_item'),
    path('communicate/', views.communicate, name='communicate'),


]
