from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('event/<uuid:pk>/', views.event_page, name="event"),
    path('attend/<uuid:pk>/', views.attend_page, name="attend"),
    path('account/<uuid:pk>/', views.account_page, name='account'),
    path('user/<str:pk>/', views.user_page, name="profile"),
    path('create/', views.event_create, name='event_create'),
    path('registrations/', views.registrations_page, name='registrations'),
    path('edit_event/<uuid:pk>/', views.edit_event, name='edit_event'),
    path('delete_event/<uuid:pk>/', views.delete_event, name='delete_event'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.event_category, name='event_category'),
    path('events/', views.event_list, name='event_list'),
]