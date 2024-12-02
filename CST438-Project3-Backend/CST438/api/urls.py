from django.urls import path
from .views import views_user, views_book, views_list

urlpatterns = [
    # Root endpoint
    path('', views_user.api_root, name='api-root'),

    # Authentication endpoints
    path('login', views_user.logIn, name='login'),
    path('newuser', views_user.createUser, name='create-user'),
    path('logout', views_user.logout_or_delete_account, name='logout'),
    path('login/admin', views_user.adminLogIn, name='admin-login'),

    # Book endpoints
    path('books', views_book.getBooks, name='get-books'),
    path('books/manage', views_book.allFunctionsBooks, name='manage-books'),
    
    # List endpoints
    path('lists', views_list.getLists, name='get-lists'),
    path('lists/user', views_list.getUserList, name='get-user-list'),
]