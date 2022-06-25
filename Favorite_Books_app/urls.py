from django.urls import path  
from .views import books,register,login,book,add_book,favoriteBook,logout
from . import views
urlpatterns = [	
    path('',views.index),
    path('books',views.books),  
    path('registre',views.register),
    path('login',views.login), 
    path('addBook',views.add_book),
    path("books/<int:id>",views.book),
    path('books/<int:id>/favorite',views.favoriteBook),
    path('books/<int:id>/unfavorite',views.unfavoriteBook),
    path('books/<int:id>/delete',views.delete_book),
    path('books/<int:id>/updated',views.edit_book),
    path('logout',views.logout),
]