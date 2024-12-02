from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def manage_reviews(request):
    if request.method == 'POST':
        try:
            review = Review.objects.create(
                user_id=request.data.get('user_id'),
                book_id=request.data.get('book_id'),
                rating=request.data.get('rating'),
                review_text=request.data.get('review_text')
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        book_id = request.GET.get('book_id')
        if book_id:
            reviews = Review.objects.filter(book_id=book_id)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        review_id = request.data.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        
        if review.user_id != request.data.get('user_id'):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        review.rating = request.data.get('rating', review.rating)
        review.review_text = request.data.get('review_text', review.review_text)
        review.save()
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        review_id = request.data.get('review_id')
        user_id = request.data.get('user_id')
        
        review = get_object_or_404(Review, pk=review_id)
        
        if review.user_id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_book_stats(request, book_id):
    stats = Review.objects.filter(book_id=book_id).aggregate(
        average_rating=Avg('rating'),
        total_reviews=models.Count('id')
    )
    return Response(stats)