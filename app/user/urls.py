from django.urls import path

# from .views import (ActivateUserView, DeleteView, LoginView, LogoutView,
#                     RegisterView)
from .views import LoginView, RegisterView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('delete/', DeleteView.as_view(), name='delete'),
    #
    # path('activate/<str:token>/', ActivateUserView.as_view(), name='activate-user'),
]
