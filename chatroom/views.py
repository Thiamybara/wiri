from django.shortcuts import render

from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer
from chatroom.serializers import *

from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view



class ChatGroupList(APIView):

    def get(self, request):
        chatgroup = ChatGroup.objects.all()
        serializer = ChatGroupSerializer(chatgroup, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ChatGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


    def put(self, request, pk, format=None):
        chatgroup = self.get_object(pk)
        serializer = ChatGroupSerializer(chatgroup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MessageList(APIView):

    def get(self, request):
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)




class MediaList(APIView):

    def get(self, request):
        media = Media.objects.all()
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



@api_view(['POST'])
def getGroupList(request):

    id_user = request.data['id']
    chatgroup = ChatGroup.objects.filter(users=id_user)
    serializer = ChatGroupSerializer(chatgroup, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['PUT'])
def addUserGroup(request):

    id_group = request.data['id_group']
    list_users = request.data['users']
    print (list_users)

    chatgroup = ChatGroup.objects.get(id=id_group)


    i = 0
    print(' debut boucle ')
    while i < (len(list_users)):
        print (list_users[i])
        chatgroup.users.add(list_users[i])
        i += 1
    print (' fin boucle ')
    chatgroup.save()

    return Response(data={
        'status':0,
        'message': 'Enregisent fait avec succès'
    })