from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

class BookListApiView(APIView):
    """
        BookListApiView provides an API 
        endpoint to retrieve a list of books.
        This view requires authentication using
        JWT and ensures that the user is authenticated.

    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, author, genre FROM books")
            rows = cursor.fetchall()
            paginator = PageNumberPagination()
            paginator.page_size = 10  
            result_page = paginator.paginate_queryset(rows, request)
            books = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in result_page]

        return paginator.get_paginated_response(books)
    

class BookSearchByGenreApiView(APIView):
    """
        Provides an API endpoint to search books by genre.
        This view requires authentication using
        JWT and ensures that the user is authenticated.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        genre = request.query_params.get('genre')
        if not genre:
            return Response({'error': 'Genre is required'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, author, genre FROM books WHERE genre = %s", [genre])
            rows = cursor.fetchall()
            if not rows:
                return Response({'message': 'No books found for the specified genre'}, status=status.HTTP_404_NOT_FOUND)

            books = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]

        return Response(books, status=status.HTTP_200_OK)
    

class AddReviewApiView(APIView):
    """
        Provides an API endpoint to add a New Review.
        This view requires authentication using
        JWT and ensures that the user is authenticated.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')
        rating = request.data.get('rating')
        
        if not book_id or not user_id or not rating:
            return Response({'error': 'book_id, user_id, and rating are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_id = int(book_id)
            user_id = int(user_id)

        except ValueError:
            return Response({'error': 'book_id and user_id must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rating = int(rating)
        except ValueError:
            return Response({'error': 'Rating must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if rating < 1 or rating > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:

            cursor.execute("SELECT COUNT(*) FROM books WHERE id = %s", [book_id])
            if cursor.fetchone()[0] == 0:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", [user_id])
            if cursor.fetchone()[0] == 0:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                cursor.execute("""
                    INSERT INTO reviews (book_id, user_id, rating)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (book_id, user_id) 
                    DO UPDATE SET rating = EXCLUDED.rating
                """, [book_id, user_id, rating])
                return Response({'message': 'Review added or updated successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteReviewApiView(APIView):
    """
        API endpoint for deleting a review of a book by a specific user.
        Requires `book_id` and `user_id` to identify the review to be deleted.
        This view requires authentication using
        JWT and ensures that the user is authenticated.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')

        if not book_id or not user_id:
            return Response({'error': 'book_id and user_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_id = int(book_id)
            user_id = int(user_id)

        except ValueError:
            return Response({'error': 'book_id and user_id must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            
            cursor.execute("SELECT COUNT(*) FROM reviews WHERE book_id = %s AND user_id = %s", [book_id, user_id])
            if cursor.fetchone()[0] == 0:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

            try:
                
                cursor.execute("DELETE FROM reviews WHERE book_id = %s AND user_id = %s", [book_id, user_id])
                return Response({'message': 'Review deleted successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
