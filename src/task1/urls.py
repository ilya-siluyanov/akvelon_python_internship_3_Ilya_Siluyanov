from django.urls import path

from . import views

urlpatterns = [
    path('users', views.users.UserView.as_view()),
    path('users/<int:user_id>', views.users.UserView.as_view()),
    path('users/<int:user_id>/transactions', views.transactions.TransactionSetView.as_view()),
    path('users/<int:user_id>/transactions/statistics', views.transactions.TransactionStatsView.as_view()),
    path('users/<int:user_id>/transactions/<int:transaction_id>', views.transactions.TransactionView.as_view())
]
