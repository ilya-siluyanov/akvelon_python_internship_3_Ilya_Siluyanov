from django.urls import path

from . import views

urlpatterns = [
    path('users', views.users.UserView.as_view()),
    path('users/<int:user_id>', views.users.UserView.as_view()),
]
