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
    #path('books/', views.books, name='frontend-books'),
    # Patron login
    #path('login/', views.login, name='frontend-login'),
    # Library about page
    path('about/', views.about, name='frontend-about'),
    # Library about page
    path('error/', views.error, name='frontend-error'),
]
