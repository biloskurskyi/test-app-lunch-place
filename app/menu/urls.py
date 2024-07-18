from django.urls import path

from .views import (LunchVotingView, MenuItemView, MenuView, RemoveVotingView,
                    VotingResultsView)

app_name = 'menu'

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('menu/<int:pk>/', MenuItemView.as_view(), name='menuItem'),
    path('vote/<int:pk>/', LunchVotingView.as_view(), name='vote'),
    path('remove-vote/', RemoveVotingView.as_view(), name='vote'),
    path('result/', VotingResultsView.as_view(), name='menu')
]
