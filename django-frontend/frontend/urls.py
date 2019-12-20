'''
Defines the URL paths for the web front end service.
11/15/2019  Created
'''
from django.urls import path
from . import views

urlpatterns = [
    # Library home page
    path('', views.catalog, name='frontend-catalog'),
    # Patron's borrowed book list
    path('booklist/', views.booklist, name='frontend-booklist'),
    # Patron login
    path('login/', views.login, name='frontend-login'),
    # Library about page
    path('about/', views.about, name='frontend-about'),
    # Library about page
    path('alert/', views.alert, name='frontend-alert'),
    # Library administrator page
    path('administrator/', views.administrator, name='frontend-administrator')
]
