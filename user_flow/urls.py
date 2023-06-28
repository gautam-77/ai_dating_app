from django.urls import path
from .import views


urlpatterns = [
    path('user', views.RegisterUser.as_view()),
    path('user_add/<int:id>', views.UserAdd.as_view()),
    path('user_delete/<int:id>', views.UserDelete.as_view()),
    path('user_update/<int:id>', views.UserUpdate.as_view()),
    
]
