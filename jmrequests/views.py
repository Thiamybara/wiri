from django.shortcuts import render

from django.shortcuts import render

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
from jmrequests.models import *
from jmrequests.serializers import *
from jmspots.serializers import *

from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from datetime import datetime
from django.db import transaction



class RequestList(APIView):

    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        # serializer = RequestSerializer(requests)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request):
    #     serializer = RequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors)




class Request_ReceiversList(APIView):

    def get(self, request):
        requestsReceivers = Request_Receivers.objects.all()
        serializer = Request_ReceiversSerializer(requestsReceivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = Request_ReceiversSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



@api_view(['POST'])
@transaction.atomic
def jmrequest_join_me(request):

    if request.method == 'POST':

        #telephone = request.data['telephone']
        latitude=request.data['latitude']
        longitude=request.data['longitude']
        sender=request.data['sender']
        list_receivers= request.data['receivers']

        try:
            spot = Spot()
            requests = Request()
            request_receivers = Request_Receivers()

            spot.latitude=latitude
            spot.longitude=longitude
            spot.save()

            requests.spot=spot
            requests.date_sender = datetime.now()

            requests.save()

            last_requete = Request.objects.latest('id')
            print (' LAST REQUETTE ')
            last_reque = last_requete.pk
            print (last_reque)

            print(' ok 1')

            print (' sender ')
            sender1 = User.objects.get(id=sender)
            request_receivers.sender= sender1
            print (request_receivers.sender)
            print(' ok 2')

            print (list_receivers)
            i = 0
            print(' debut boucle ')
            # with transaction.commit_on_success():


            with transaction.atomic():

                while i < (len(list_receivers)):
                    print (' ccccccccccccccccccc ')
                    print (list_receivers[i])
                    request_receivers.sender = sender1
                    print (' cc 1 ')
                    request_receivers.is_active = True
                    print (' cc 2 ')
                    # request_receivers.list_receivers.add(list_receivers[i])

                    u = User.objects.get(id=list_receivers[i])
                    request_receivers.list_receivers = u
                    print (request_receivers.list_receivers)
                    print (' cc 3 ')
                    # request_receivers.state= 'NULL'
                    # print (' cc 4 ')

                    req = Request.objects.get(id=last_reque)
                    Request.objects.latest('id')
                    print (' Requette ')
                    print (req)
                    request_receivers.receivers = req
                    print (' cc 4 ')
                    a = Request_Receivers(
                        sender=sender1,
                        list_receivers = u,
                        receivers = req,
                        is_active= True,
                    )
                    print(' cc 5 ')
                    a.save()
                    print(' cc 6 ')

                    # request_receivers.save()
                    print(' cc 7 ')

                    i += 1
                print (' fin boucle ')

            return Response(data={
                'status':0,
                'message':'L\'enregistrement est bien effectué',
                # 'requests': {
                #     'id': requests.id,
                #     'sender': requests.sender,
                #     'receivers': requests.receivers
                #     # 'spot':requests.spot
                #           },
                                }
                    )
        except :
            return Response(
                data={
                    'status':1,
                    'message':'Echec de l\'enregistrement des Requests '})






@api_view(['POST'])
@transaction.atomic
def jmrequest_join_me_card(request):

    if request.method == 'POST':

        # id = request.data['id']

        sender = request.data['sender']
        id_card = request.data['card']
        list_receiver = request.data['list_receiver']
        message = request.data['message']
        # date_receivers = request.data['date_receivers']
        # date_receivers = datetime.now()

        try:
            requests = Request()
            # requests = Request.objects.get(id=id)
            requests.with_card=True
            # requests.date_sender=datetime.now()
            # requests.date_receivers=date_receivers
            requests.message=message

            print(' cc1 ')
            print (requests.message)

            cards = Card.objects.values('institution__spot__id', 'event__spot__id').get(id=id_card)
            print (cards)

            print (cards.institution__spot__id)
            print(' cc ')
            print (cards.event.id)

            # requests.card=cards

            print(requests.card)
            print (' cc 2 ')

            if cards.institution == None:
                events = Card.objects.values('event__spot').get(id=1)
                print (events.id)
                print(' Event ')
                requests.spot=events.id
                print (' Fin Event ')
            else:
                institutions = Card.objects.values('institution__spot').get(id=1)
                print (institutions.id)
                print (' Institutions ')
                requests.spot=institutions.id
                print (' Fin institution ')



            # test = Card.objects.get(id=1)
            # print (test)
            #
            # if test.institution==None:
            #
            #     events = Card.objects.values('event__spot').get(id=1)
            #     print (events.id)
            #     print(' Event ')
            #     requests.spot=events.id
            #     print (' Fin Event ')
            #
            # else:
            #     institutions = Card.objects.values('institution__spot').get(id=1)
            #     print (institutions.id)
            #     print (' Institutions ')
            #     requests.spot=institutions.id
            #     print (' Fin institution ')
            #


            # if test.institution

            # requests.spot = eee
            print (' spot ')

            requests.save()
            print (' cc 3 ')



            last_requete = Request.objects.latest('id')
            print (' LAST REQUETTE ')
            last_reque = last_requete.pk
            print (last_reque)

            request_receivers = Request_Receivers()
            i = 0

            with transaction.atomic():

                while i < (len(list_receiver)):
                    print (' ccccccccccccccccccc ')
                    print (list_receiver[i])

                    sender1 = User.objects.get(id=sender)
                    request_receivers.sender = sender1
                    print (' cc 1 ')

                    request_receivers.is_active = True
                    print (' cc 2 ')
                    # request_receivers.list_receivers.add(list_receivers[i])


                    u = User.objects.get(id=list_receiver[i])
                    request_receivers.receivers = u

                    print (request_receivers.receivers)
                    print (' cc 3 ')
                    # request_receivers.state= 'NULL'
                    # print (' cc 4 ')

                    req = Request.objects.get(id=last_reque)
                    Request.objects.latest('id')
                    print (' Requette ')
                    print (req)
                    request_receivers.receivers = req
                    print (' cc 4 ')
                    a = Request_Receivers(
                        sender=sender1,
                        list_receivers = u,
                        receivers = req,
                        is_active= True,
                    )
                    print(' cc 5 ')
                    a.save()
                    print(' cc 6 ')

                    # request_receivers.save()
                    print(' cc 7 ')

                    i += 1
                print (' fin boucle ')

            return Response(data={
                'status': 0,
                'message': 'L\'enregistrement est bien effectué',
                # 'requests':{
                #     'id': requests.id,
                #     'is_active': requests.is_active,
                #     'date_sender': requests.date_sender,
                #     'date_receivers': requests.date_receivers,
                #     'with_card': requests.with_card,
                #     'message':requests.message,
                #     'sender': requests.sender,
                #     'card': requests.card
                # }
            }
            )

        except:
            return Response(
                data={
                    'status': 1,
                    'message': 'Echec de l\'enregistrement des Requests '})





# @api_view(['POST'])
# def jmrequest_joiner(request):
#
#     if request.method == 'POST':
#
#         id = request.data['id']
#         try:
#
#             requests = Request_Receivers.objects.filter(sender=id, is_active=False).last()
#
#             return Response(
#                 data={
#                     'status': 0,
#                     'message': 'Récupération éffectué',
#                     'requests_receivers':{
#                         'id': requests.id,
#                         'is_active': requests.is_active,
#                         'state': requests.state,
#                         # 'sender': requests.sender
#                         # 'requette': requests.receivers,
#                         # 'card': requests.card,
#                         # 'list_receivers': requests.list_receivers
#                     }
#                 }
#             )
#         except:
#             return Response(
#                 data={
#                     'status': 1,
#                     'message': 'Aucune information à propos de ce requette'})



@api_view(['POST'])
def jmrequest_joiner(request):

    if request.method == 'POST':

        id = request.data['id']
        try:

            requests = Request_Receivers.objects.filter(sender=id, is_active=False).last()
            serializer = Request_ReceiversSerializer(requests)
            # serializer = RequestSerializer(requests)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={
                    'status': 1,
                    'message': 'Aucune information à propos de ce requette'})












@api_view(['POST'])
def invitation(request):
    """

   Cette Fonction permet de renvoyer l'ensemble des requettes de l'utilisateur
    """

    if request.method == 'POST':

        senders = request.data['sender']
        requests = Request_Receivers.objects.filter(sender=senders)
        serializer = Request_ReceiversSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)