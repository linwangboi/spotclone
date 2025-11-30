from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('music/<str:pk>/', views.music, name='music'),
    path('profile/<str:pk>/', views.profile, name='profile'), 
    path('search/', views.search, name='search'),
]
