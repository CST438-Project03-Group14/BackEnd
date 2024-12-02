from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from ..models import List, User
from ..serializers import ListSerializer

@api_view(['GET'])
def getLists(request):
    user_id = request.GET.get('user_id', None)

    if user_id:
        try:
            list_instances = List.objects.filter(user_id=user_id)
        except List.DoesNotExist:
            return Response({'error':'List not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ListSerializer(list_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    lists = List.objects.all()
    serializer = ListSerializer(lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getUserList(request):
    user_id = request.GET.get('user_id')
    try:
        list_instance = List.objects.get(user_id=user_id)
    except List.DoesNotExist:
        return Response({'error':'List not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ListSerializer(list_instance)
    return Response(serializer.data, status=status.HTTP_200_OK) 

@api_view(['POST'])
def addList(request):
    list_name = request.GET.get('list_name')
    user_id = request.GET.get('user_id')
    list_name = request.data.get('list_name', list_name)
    user_id = request.data.get('user_id', user_id)

    if List.objects.filter(shelf_type=list_name, user_id=user_id).exists():
        return Response({'error': 'List with this name already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_id=user_id)
        listObject = List.objects.create(shelf_type=list_name, user=user)
        serializer = ListSerializer(listObject)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def deleteList(request):
    user_id = request.GET.get('user_id')
    list_id = request.GET.get('list_id')
    user_id = request.data.get('user_id', user_id)
    list_id = request.data.get('list_id', list_id)

    try:
        list_instance = List.objects.get(list_id=list_id, user_id=user_id)
        list_instance.delete()
        return Response({'message' : f'List {list_id} has been deleted'}, status=status.HTTP_200_OK)
    except List.DoesNotExist:
        return Response({'error': 'list id or user id not found'}, status=status.HTTP_404_NOT_FOUND)