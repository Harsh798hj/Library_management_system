from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('books/', BookListView.as_view()),
    path('books/add/', AddBookView.as_view()),
    path('books/<int:pk>/delete/', DeleteBookView.as_view()),
    path('cart/', CartItemView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('saved/', SavedForLaterView.as_view()),
    path('books/report/', BookReportView.as_view()),
    path('issued/', IssuedBooksListView.as_view()),


]
