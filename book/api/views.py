from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
            books = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]
        return Response(books, status=status.HTTP_200_OK)
    

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