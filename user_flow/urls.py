from django.urls import path
from .import views


urlpatterns = [
    path('user', views.UserGet.as_view()),
    path('user_add', views.UserAdd.as_view()),
    path('user_delete/<int:id>', views.UserDelete.as_view()),
    path('user_update/<int:id>', views.UserUpdate.as_view()),
    path('user_login', views.UserLogin.as_view()),
]
