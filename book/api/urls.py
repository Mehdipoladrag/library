from django.urls import path
from .views import (
    BookListApiView, 
    BookSearchByGenreApiView, 
    AddReviewApiView,
    DeleteReviewApiView,
)




urlpatterns = [
    path('list/', BookListApiView.as_view(), name='BookList'),
    path('books', BookSearchByGenreApiView.as_view(), name='BooksByGenre'),
    path('review/add/', AddReviewApiView.as_view(), name='AddReview'),
    path('review/delete/', DeleteReviewApiView.as_view(), name='DeleteReview'),

]
