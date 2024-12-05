from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.models import Book
from api.serializers import BookSerializer


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def allFunctionsBooks(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        search = request.GET.get('search')

        if book_id:
            book = get_object_or_404(Book, pk=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if search:
            books = Book.objects.filter(title__icontains=search)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        title = request.data.get('title')
        author = request.data.get('author')
        genre = request.data.get('genre')
        published_date = request.data.get('published_date')

        if not title or not author or not genre or not published_date:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        book = Book.objects.create(
            title=title,
            author=author,
            genre=genre,
            published_date=published_date,
            description=request.data.get('description', ''),
            cover_image=request.data.get('cover_image', None),
            available_copies=request.data.get('available_copies', 0),
        )
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response({"message": f"Book {book_id} deleted"}, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=book_id)

        book.title = request.data.get('title', book.title)
        book.author = request.data.get('author', book.author)
        book.genre = request.data.get('genre', book.genre)
        book.published_date = request.data.get('published_date', book.published_date)
        book.description = request.data.get('description', book.description)
        book.cover_image = request.data.get('cover_image', book.cover_image)
        book.available_copies = request.data.get('available_copies', book.available_copies)

        book.save()
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

