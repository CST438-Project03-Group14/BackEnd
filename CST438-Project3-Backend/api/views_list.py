from rest_framework.response import Response
from rest_framework.response.decorators import api_view

@api_view(['GET'])
def getData(request):
    # from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from base.models import Lists
from .serializers import ListsSerializer

#Gets all the Lists
@api_view(['GET'])
def getLists(request):
    user_id = request.GET.get('user_id', None)

    if user_id:
        try:
            list_instances = Lists.objects.filter(user_id=user_id)
        except Lists.DoesNotExist:
            return Response({'error':'List not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ListsSerializer(list_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    lists = Lists.objects.all()
    serializer = ListsSerializer(lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Gets all the lists of a specific user.
@api_view(['GET'])
def getUserList(request):
    user_id = request.GET.get('user_id')
    try:
        list_instance = Lists.objects.get(user_id=user_id)
    except Lists.DoesNotExist:
        return Response({'error':'List not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ListsSerializer(list_instance)
    return Response(serializer.data, status=status.HTTP_200_OK) 

#Creates a new list
@api_view(['Post'])
def addList(request):
    list_name = request.GET.get('list_name')
    user_id = request.GET.get('user_id')
    list_name = request.data.get('list_name', list_name)
    user_id = request.data.get('user_id', user_id)

    if Lists.objects.filter(list_name=list_name,user_id=user_id).exists():
        return Response({'error': 'List with this name already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    listObject = Lists.objects.create(list_name=list_name, user_id=user_id)
    serializer = ListsSerializer(listObject)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Deletes the list with the same list_id
@api_view(['DELETE'])
def deleteList(request):
    user_id = request.GET.get('user_id')
    list_id = request.GET.get('list_id')
    user_id = request.data.get('user_id', user_id)
    list_id = request.data.get('list_id', list_id)

    try:
        list_instance = Lists.objects.get(list_id=list_id, user_id=user_id)
        list_instance.delete()
        return Response({'message' : f'List {list_id} has been deleted'}, status=status.HTTP_200_OK)

    except Lists.DoesNotExist:
        return Response({'error': 'list id or user id not found'}, status=status.HTTP_404_NOT_FOUND)

