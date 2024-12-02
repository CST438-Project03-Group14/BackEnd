import logging
logger = logging.getLogger('api')

# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import Book
from ..serializers import BookSerializer

import logging
logger = logging.getLogger('api')

@api_view(['GET'])
def getBooks(request):
    logger.info('Fetching all books')
    try:
        books = Book.objects.all()
        logger.debug(f'Found {books.count()} books')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error fetching books: {str(e)}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def allFunctionsBooks(request):
    logger.info(f'Book operation: {request.method}')
    
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        search = request.GET.get('search')
        user_id = request.GET.get('user_id')
        
        logger.debug(f'GET parameters - book_id: {book_id}, search: {search}, user_id: {user_id}')
        
        if not book_name and not list_id:
            logger.warning("Missing required fields book_name and list_id")
            return Response({"error": "book_name and list_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            list_object = Lists.objects.get(pk=list_id)
            logger.debug(f"Found list with id: {list_id}")
        except Lists.DoesNotExist:
            logger.error(f"List with id {list_id} not found")
            return Response({"error": "List does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            book = Book.objects.create(
                book_name=book_name,
                list=list_object,
                book_url=request.data.get('book_url', None),
                image_url=request.data.get('image_url', None),
                price=request.data.get('price', None),
                quantity=request.data.get('quantity', None),
                description=request.data.get('description', None)
            )
            logger.info(f"Successfully created book: {book_name}")
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating book: {str(e)}")
            return Response({"error": str(e)}, status=500)