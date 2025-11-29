from ticketmastermaster import views
"""
URL configuration for WebDevFinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.view_login, name='login'),
    path('register/', views.view_register, name='register'),
    path('logout/', views.view_logout, name='logout'),
    path('discuss/<int:discussion_id>', views.view_discuss, name='discuss'),
    path('discuss/create', views.view_discuss_create, name='create_discuss'),
    path('discuss/delete', views.view_discuss_delete, name='delete_discuss'),
    path('discuss/update', views.view_discuss_update, name='update_discuss')



]
