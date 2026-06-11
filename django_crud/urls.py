"""
URL configuration for django_crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .todos import views as todos_views
from .users import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filter/',todos_views.filter_list),
    path("todos/create/", todos_views.todo_create),
    path("todos/update/<int:pk>/", todos_views.todo_update),
    path("todos/delete/<int:pk>/", todos_views.todo_delete),

    # urls for users

    path("users/", views.users_list),
    path("user/", views.user_detail),
    path("users/create/", views.user_create),
    path("users/update/<uuid:pk>/", views.user_update),
    path("users/delete/<uuid:pk>/", views.user_delete),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),



]


