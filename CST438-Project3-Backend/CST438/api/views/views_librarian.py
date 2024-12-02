from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, User
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404

def check_librarian(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user.is_librarian
    except User.DoesNotExist:
        return False

@api_view(['POST', 'PUT', 'DELETE'])
def manage_books(request):
    user_id = request.data.get('user_id')
    
    if not check_librarian(user_id):
        return Response({'error': 'Librarian access required'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        book = get_object_or_404(Book, pk=request.data.get('book_id'))
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book = get_object_or_404(Book, pk=request.data.get('book_id'))
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)