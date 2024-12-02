from django.urls import path
from .views import views_book, views_list, views_user

urlpatterns = [
    # Book Management
    path('books', views_book.getBooks, name='get-books'),
    path('books/manage', views_book.allFunctionsBooks, name='manage-books'),
    
    # List Management
    path('lists', views_list.getLists, name='get-lists'),
    path('lists/user', views_list.getUserList, name='get-user-list'),
    path('lists/add', views_list.addList, name='add-list'),
    path('lists/delete', views_list.deleteList, name='delete-list'),
    
    # User Management
    path('', views_user.homePage, name='home'),
    path('users', views_user.getAllUsers, name='get-all-users'),
]