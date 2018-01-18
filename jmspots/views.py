from _ast import In

from django.shortcuts import render
from django.http import JsonResponse


from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from jmspots.models import *
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer
from jmspots.serializers import *

from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from django.core import serializers
from django.http import HttpResponse
import json


class CategorytList(APIView):

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


#
# def get(self, request):
#     #list_card_institutionel = CardShare.objects.filter(events=None)
#     list_card_institutionel = CardShare.objects.all()
#     #list_card_event = CardShare.objects.filter(institution=None)
#     q_json = serializers.serialize("json", list_card_institutionel)
#     return HttpResponse(q_json, content_type='application/json')

class CardList(APIView):

    def get(self, request):
        list_card_institutionel = Card.objects.exclude(event__is_public=False)
        #return HttpResponse(json.dumps(list_card_institutionel), content_type='application/json')

        # list_card_institutionel = Card.objects.exclude(event__is_public=False).values_list(
        #     'id', 'institution__id', 'institution', 'event__id', 'event__name', 'event__description', 'event__jm_tag',
        #     'event__created', 'event__is_public', 'event__spot','event__owner',
        #     'category', 'file',
        # )
        serializer = CardSerializer(list_card_institutionel, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def post(self, request):
        serializer = Card(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)




class EventList(APIView):

    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)





class InstitutionList(APIView):

    def get(self, request):
        institution = Institution.objects.all()
        serializer = InstitutionSerializer(institution, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class SpotList(APIView):

    def get(self, request):
        spot = Spot.objects.all()
        serializer = SpotSerializer(spot, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SpotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class UserCardList(APIView):

    def get(self, request):
        usercard = UserCard.objects.all()
        serializer = UserCardSerializer(usercard, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class UserCardFavouriteList(APIView):

    def get(self, request):
        usercardfavourite = UserCardFavourite.objects.all()
        serializer = UserCardFavouriteSerializer(usercardfavourite, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserCardFavouriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)





@api_view(['POST'])
def listFavourite(request):

    if request.method == "POST":

        senders = request.data['sender']
        try:
            u = UserCardFavourite.objects.get(sender=senders)
            serialiser  = UserCardFavouriteSerializer(u)
            return Response(serialiser.data)
        except:
            return Response(data={'status': -1, 'message': ' Utilisateur inextant '})