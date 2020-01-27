"""skdmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views import generic
from django.views.decorators.cache import never_cache
from administracja import views

admin.site.site_header = "Panel administatora IT"

urlpatterns = [
    # witryna administracyjna Django
    path('admin/', admin.site.urls, name='admin'),
    # Strona główna
    path('', views.dashboard, name='dashboard'),
    # logowanie
    #path('logowanie/',views.user_login, name='login'),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    # zmiana hasła
    path('password_change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    # Widoki biznesowe
    path('osoby/',
        never_cache(views.PersonListView.as_view()),
        name='persons'),
    path('osoby/<int:pk>/',
        never_cache(views.PersonDetailView.as_view()),
        name='person_detail'),
    path('karty/',
        never_cache(views.CardListView.as_view()),name='cards2'),
    path('karty/<str:pk>/',
        never_cache(views.CardDetailView.as_view()),
        name='card_detail'),
]
