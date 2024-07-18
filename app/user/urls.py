from django.urls import path

from .views import DeleteView, LoginView, LogoutView, RegisterView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteView.as_view(), name='delete'),
]
