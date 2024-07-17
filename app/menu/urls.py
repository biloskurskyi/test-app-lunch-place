from django.urls import path

from .views import MenuItemView, MenuView

app_name = 'menu'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('menu/<int:pk>/', MenuItemView.as_view(), name='menuItem'),
]
