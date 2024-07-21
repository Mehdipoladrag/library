from django.urls import path
from .views import (
    BookListApiView,
    BookSearchByGenreApiView,
    AddReviewApiView,
    DeleteReviewApiView,
    UpdateReviewApiView,
    RecommendBooksApiView,
)


urlpatterns = [
    path("list/", BookListApiView.as_view(), name="BookList"),
    path("books", BookSearchByGenreApiView.as_view(), name="BooksByGenre"),
    path("review/add/", AddReviewApiView.as_view(), name="AddReview"),
    path("review/delete/", DeleteReviewApiView.as_view(), name="DeleteReview"),
    path("review/update/", UpdateReviewApiView.as_view(), name="edit-review"),
    path("suggest/", RecommendBooksApiView.as_view(), name="recommend-books"),
]
