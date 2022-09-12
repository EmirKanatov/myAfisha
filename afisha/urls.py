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
from movie_app.views import directors_view, directors_detail_view, movies_view, \
    movies_detail_view, reviews_view, reviews_detail_view, movies_reviews_view, DirectorListAPIView, \
    DirectorDetailUpdateDeleteAPIView, MovieListAPIView, MovieDetailUpdateDeleteAPIView, ReviewsListAPIView, \
    ReviewDetailUpdateDeleteAPIView
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', DirectorListAPIView.as_view()),
    path('api/v1/directors/<int:id>/', DirectorDetailUpdateDeleteAPIView.as_view()),
    path('api/v1/movies/', MovieListAPIView.as_view()),
    path('api/v1/movies/reviews/', movies_reviews_view),
    path('api/v1/movies/<int:id>/', MovieDetailUpdateDeleteAPIView.as_view()),
    path('api/v1/reviews/', ReviewsListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailUpdateDeleteAPIView.as_view()),
    path('api/v1/register/', users_views.RegisterAPIView.as_view()),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         users_views.activate, name='activate'),
    path('api/v1/authorization/', users_views.AuthorizationAPIView.as_view())
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)