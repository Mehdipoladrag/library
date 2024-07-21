from django.urls import path
from .views import BookListApiView, BookSearchByGenreApiView




urlpatterns = [
    path('list/', BookListApiView.as_view(), name='BookList'),
    path('books', BookSearchByGenreApiView.as_view(), name='BooksByGenre'),
]
