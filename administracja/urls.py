from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'administracja'

urlpatterns = [
        #path('logowanie/',views.user_login, name='login'),
        #path('', views.dashboard, name='dashboard'),
        #path('login/',auth_views.LoginView.as_view(), name='login'),
        #path('logout/',auth_views.LogoutView.as_view(), name='logout'),
        #path('osoby/',views.person_list, name='persons'),
        #path('karty/',views.card_list, name='cards'),
        #path('karty/<str:id>/',views.vcard_detail,name='card_detail'),      
        ]

