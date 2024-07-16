from django.urls import path

from .views import MenuView

app_name = 'menu'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='create')
]
