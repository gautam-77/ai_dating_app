from django.urls import path
from .import views

urlpatterns = [
    path('user', views.RegisterUser.as_view()),
    path('user/<int:id>', views.RegisterUser.as_view())
]
