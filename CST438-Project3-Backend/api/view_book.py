# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from base.models import Book, Lists
from .serializers import BookSerializer

#Gets all the Lists
@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def allFunctionsBooks(request):
    # GET: List or show a specific book
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        search = request.GET.get('search')
        user_id = request.GET.get('user_id')
        if book_id:
            book = get_object_or_404(Book, pk=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)

        if search:
            books = Book.objects.filter(book_name__icontains=search)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        if user_id:
            user_lists = Lists.objects.filter(user_id=user_id)
            books = Book.objects.filter(list__in=user_lists)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        list_id = request.GET.get('list_id')
        if list_id:
            books = Book.objects.filter(list=list_id)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        return Response({"error": "Request was missing book_id/search, or was missing list_id/book_name"})

    # POST: Add a new book
    elif request.method == 'POST':
        book_name = request.data.get('book_name')
        list_id = request.data.get('list_id')
        
        if not book_name and not list_id:
            return Response({"error": "book_name and list_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            list_object = Lists.objects.get(pk=list_id)
        except Lists.DoesNotExist:
            return Response({"error": "List does not exist"}, status=status.HTTP_404_NOT_FOUND)

        book = Book.objects.create(
            book_name=book_name,
            list = list_object,
            book_url=request.data.get('book_url', None),
            image_url=request.data.get('image_url', None),
            price=request.data.get('price', None),
            quantity=request.data.get('quantity', None),
            description=request.data.get('description', None)
        )

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # DELETE: Remove an book by ID
    elif request.method == 'DELETE':
        # This structure means that passing parameters in the url works for easy debugging.
        book_id = request.GET.get('book_id')
        book_id = request.data.get('book_id', book_id)

        if not book_id:
            return Response({"error": "Book ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response({"message": f"Book {book_id} deleted"}, status=status.HTTP_200_OK)

    # PATCH: Update an book by ID
    elif request.method == 'PATCH':
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({"error": "Book ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, pk=book_id)

        book.book_name = request.data.get('book_name', book.book_name)
        book.book_url = request.data.get('book_url', book.book_url)
        book.image_url = request.data.get('image_url', book.image_url)
        book.price = request.data.get('price', book.price)
        book.quantity = request.data.get('quantity', book.quantity)
        book.description = request.data.get('description', book.description)

        book.save()

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)