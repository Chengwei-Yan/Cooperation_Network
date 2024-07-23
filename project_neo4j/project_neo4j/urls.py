"""project_neo4j URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from app import views

urlpatterns = [
    path('', views.index, name='index'),  # 根URL指向index视图
    path('admin/', admin.site.urls),
    path('menus/', views.example_data),
    path('login/', views.login),
    path('search/', views.search),
    path('getfile/', views.getfile),
    path('datadetail/', views.datadetail),
    path('download/', views.download),
    path('statistics/', views.statistics),
    path('get_country/',views.get_country),
    path('get_keyword/', views.get_keyword),
    path('create/',views.create),
    path('insert_key/',views.insert_key)

]
