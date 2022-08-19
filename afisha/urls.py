"""afisha URL Configuration

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
from movie_app.views import directors_view, directors_detail_view, movies_view,\
    movies_detail_view, reviews_view, reviews_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', directors_view),
    path('api/v1/directors/<int:id>/', directors_detail_view),
    path('api/v1/movies/', movies_view),
    path('api/v1/movies/<int:id>/', movies_detail_view),
    path('api/v1/reviews/', reviews_view),
    path('api/v1/reviews/<int:id>/', reviews_detail_view),
]
