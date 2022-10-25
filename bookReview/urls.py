"""bookReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from books.views import *
from django.contrib.auth.views import LogoutView
from rest_framework import routers
from books.apiView import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.SimpleRouter(trailing_slash=True)

router.register("books", BookViewSet, basename="books")
router.register("user", APIUserViewSet, basename="user")
router.register("comment", CommentViewSet, basename="comment")


urlpatterns = [
    path('api/', SpectacularAPIView.as_view(), name="schema"),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api-token-auth/', views.obtain_auth_token),

    path('api/user/', CurrentUserView.as_view(), name="user"),

    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
    path('home/', ListBooksView.as_view()),
    path('create/', CreateBookView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', UserSignUpView.as_view()),
] + router.urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
