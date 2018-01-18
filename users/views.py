# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import Http404
from random import randint
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Interest
from rest_framework import status
from users.serializers import UserSerializer, InterestSerializer, FavouriteContactSerializer
from rest_framework.serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from base64 import b64decode
from django.core.files.base import ContentFile
import base64

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.db.models import Q




import imghdr # Used to validate images
#import urllib2 # Used to download images
import urllib.request # Used to download images
from urllib.parse import urljoin
# import urlparse # Cleans up image urls

from io import StringIO
import io

#import cStringIO # Used to imitate reading from byte file
#from PIL import Image # Holds downloaded image and verifies it
import copy # Copies instances of Image







def createActivationToken():
    return randint(100000, 1000000)



class InterestList(APIView):


    def get(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class FavouriteContactList(APIView):

    def get(self, request):
        favourite = FavouriteContact.objects.all()
        serializer = FavouriteContactSerializer(favourite, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FavouriteContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class UserList(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        if data["telephone"]:
            data["activation_token"] = createActivationToken()
            data["is_active"] = False
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance




class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
def inscription(request):

    """ Permet de gerer l'inscription d'un utilisateur.

    Le scenario d'inscription d'un utilisateur sur Wiri se fait comme suit:
        1 - l'utilisateur saisi un numero de telephone qui existe deja en base
            a - le compte associe a ce numero est actif: on demande a l'utilisateur d'aller se connecter
            b - le compte associe a ce numero est inactif: on lui envoi un token d'activation et on lui demande de poursuivre son inscription
        2 - l'utilisateur saisi un numero de telephone qui n'existe pas en base: On lui creer un compte et on lui demande de l'activer

    """

    telephone = request.data['telephone']

    try:
        u = User.objects.get(telephone=telephone)
        if u.is_active == True:
            return Response(data={
                'status': -1,
                'message': 'Vous etes deja inscrit. Connectez-vous pour acceder a Wiri.',
            })
        else:
            return Response(data={
                'status': 1,
                'message': 'Votre compte n\'est pas encore active. Veuillez saisir le code envoye par SMS',
                'user': {
                    'id': u.id,
                    'telephone': u.telephone,
                    'activation_token': u.activation_token,
                },
            })
    except:
        u = User()
        u.telephone = telephone
        u.is_active = False
        u.activation_token = createActivationToken()
        u.save()
        return Response(data={
            'status': 0,
            'message': 'Votre inscription est bien prise en compte, Veuillez saisir le code envoye par SMS',
            'user': {
                'id': u.id,
                'telephone': u.telephone,
                'activation_token': u.activation_token,
            },
        })





@api_view(['PUT'])
def validation_Code(request):

    if request.method == "PUT":
        try:
            u = User.objects.get(activation_token=request.data["code"], telephone=request.data["telephone"])
            u.activation_token = None
            u.is_active = True
            u.save()
            return Response(data={
                'status': 0,
                'message': 'Votre compte Wiri est active avec succes.',
            })

        except:
            return Response(data={
                'status': 1,
                'message': 'Echec de l\'activation du compte. Verifiez votre code s\'il vous plait.',
            })


# Compléments d'information
@api_view(['PUT'])
def complements_info(request):

    """ Permet de compléter les informations de l'utilisateur

        Le scenario du complément d'information d'un utilisateur sur Wiri se fait comme suit:

            - l'utilisateur doit d'abord exister en base de donnée et son compte soit actif:
            l'utilisateur doit remplir son prénom , nom , email et mot de passe qui sont insérés en base de donnée

        """



    if request.method == "PUT":

        try:

            numero = request.data['telephone']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']

            user = User.objects.get(telephone=numero)
            if user is not None:

                user.first_name= first_name
                user.last_name=last_name
                user.email=email
                user.password=password
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'Bienvenue sur wiri, votre profil a été bien pris prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password,
                    },})
        except:
            return Response(data={'status': 1, 'message': 'Echec de l\' enregistrement des informations complémentaires'})




@api_view(['PUT'])
def save_interest(request):

    """ Permet de modifier les centres d'interet d'un utilisateur.

        Le scenario de l'enregistrement des centres d'intéret d'un utilisateur sur Wiri se fait comme suit:

            1 - l'utilisateur saisi un numero de telephone qui existe deja en base et
            un tableau des centres d'intérets que l'utilisateur a choisit
             et qui sont insérés en base de données

        """


    if request.method == "PUT":
        telephone = request.data['telephone']
        user = User.objects.get(telephone=telephone)
        print(user)

        interest = request.data['interest']
        print (interest)

        i = 0
        print(' debut boucle ')
        while i < (len(interest)):
            print (interest[i])
            user.interest.add(interest[i])
            i += 1

        print (' fin boucle ')
        user.save()


        return Response(
                    data={'status': 0, 'message': 'Vos centres d\' interet ont bien été enregsitrés'})
    else:

        return Response(data={'status': 1, 'message': 'Echec de l\' enregsitrement du centre d\'interet'})





# Liste de centre d'intéret
@api_view(['GET'])
def listInterest(request, numero):
    try:
        listInterest = User.objects.values('interest').filter(telephone=numero)
        serialiser = InterestSerializer(listInterest)
        return Response(data={listInterest})
    except User.DoesNotExist:
            raise Http404




# L'ensemble des contacts qui sont dans wiri
@api_view(['GET'])
def contacts(request):

    if request.method == "GET":
        try:
            u = User.objects.filter(is_active=True)
            serialiser = UserSerializer(u, many=True)
            return Response(serialiser.data)
        except:
            return Response(data={'status': -1, 'message': ' Utilisateur inextant '})



#ok
@api_view(['POST'])
def authentification(request):

    if request.method == "POST":

        telephone = request.data['telephone']
        password = request.data['password']

        try:
            user = User.objects.get(telephone=telephone)
            # if user.is_active == True:
            if user.telephone == telephone and user.password==password:
                return Response(
                    data={'status': 0,
                          'message': 'L authentification reussit',
                          'user': {
                              'id': user.id,
                              'telephone': user.telephone,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'email': user.email,
                              'password': user.password,
                              #'photo': base64.encodebytes(user.photo),
                              # 'interest': user.interest
                            },
                          })
            else:
                return Response(data={'status':1, 'message':'Le Login ou le mot de passe est inccorect'})
        except:
            return Response(data={'status': 1, 'message': 'Le Login ou le mot de passe est inccorect'})











# ok
@api_view(['GET'])
def verif_user(request, telephone):

    if request.method == "GET":

        # telephone = request.data['telephone']

        try:
            user = User.objects.get(telephone=telephone)
            # if user.is_active == True:
            if user.telephone == telephone and user.is_active == True:
                return Response(
                    data={'status': 0,
                          'message': 'True',
                          'user': {
                              'id': user.id,
                              'telephone': user.telephone,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'email': user.email,
                              'password': user.password,
                                },
                          })
            else:
                return Response(data={'status': 1, 'message': 'False'})
        except:
            return Response(data={'status': 1, 'message': 'False'})





# #ok
# @api_view(['POST'])
# def verif_user(request):
#
#     if request.method == "POST":
#
#         telephone = request.data['telephone']
#
#         try:
#             user = User.objects.get(telephone=telephone)
#             # if user.is_active == True:
#             if user.telephone == telephone and user.is_active==True:
#                 return Response(
#                     data={'status': 0,
#                           'message': 'Utilisateur existant',
#                           'user': {
#                               'id': user.id,
#                               'telephone': user.telephone,
#                               'first_name': user.first_name,
#                               'last_name': user.last_name,
#                               'email': user.email,
#                               'password': user.password,
#                             },
#                           })
#             else:
#                 return Response(data={'status':1, 'message':'Utilisateur nest pas de WIRI'})
#         except:
#             return Response(data={'status': 1, 'message': 'Le Login ou le mot de passe est inccorect'})











@api_view(['POST'])
def addFavoriteContact(request):

    if request.method == "POST":
        try:
            idContact = request.data['id']
            listeContact = request.data['favouriteContact']
            print (listeContact)

            favouriteContacts = FavouriteContact()

            id_user = User.objects.get(id=idContact)
            favouriteContacts.userss = id_user
            print (favouriteContacts.userss)

            i = 0
            print(' debut boucle ')

            while i < (len(listeContact)):
                print (listeContact[i])
                # favouriteContacts.users.add(listeContact[i])
                # favouriteContacts.users.add(listeContact[i]) à voir
                i += 1
                print (' fin boucle ')

            favouriteContacts.save()

            return Response(
                data={
                    'status': 0,
                    'message': 'Enregistrement effectué avec success ',
                    # 'favourite': favouriteContacts.userss
                })

        except:
            return Response(data={'status': 1, 'message': 'Echec de l\'enregistrement'})




@api_view(['POST'])
def getFavoriteContact(request):

    if request.method == "POST":

            idContact = request.data['id']
            favouriteContact = FavouriteContact.objects.get(userss=idContact)
            serializer = FavouriteContactSerializer(favouriteContact)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data={'status': 1, 'message': 'Affichage non effectué'})




# La bonne
@api_view(['POST'])
def addFavoriteContact2(request):

    serializer = FavouriteContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)







@api_view(['PUT'])
def modify_info(request):
    if request.method == "PUT":

        try:
            numero = request.data['telephone']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']

            user = User.objects.get(telephone=numero)
            if user is not None:

                user.first_name= first_name
                user.last_name=last_name
                user.email=email
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre profil a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                    },})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification des informations'})




@api_view(['PUT'])
def modify_password(request):
    if request.method == "PUT":

        try:

            old_password = request.data['old_password']
            new_password = request.data['new_password']

            numero = request.data['telephone']

            user = User.objects.get(telephone=numero)

            if user is not None and user.password==old_password:

                user.password= new_password
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre mot de passe a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'telephone': user.telephone,
                        'password': user.password
                    },})
            else:
                return Response(data={'status': 1, 'message': 'Echec de la modification du mot de passe'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification du mot de passe'})






@api_view(['PUT'])
def edit_photo(request):
    if request.method == "PUT":

        try:
            numero = request.data['telephone']
            photo = request.data['photo']
            user = User.objects.get(telephone=numero)

            if user is not None:

                user.photo= photo
                user.save()

                return Response(data={
                    'status': 0,
                    'message': 'La modification de votre photo a été bien prise en compte',
                    'user': {
                        'id': user.id,
                        'photo': user.photo,
                    },})
            else:
                return Response(data={'status': 1, 'message': 'Echec de la modification du photo de profil'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de la modification du photo de profil'})






@api_view(['PUT'])
def save_image(request):

    if request.method == "PUT":
        try:
            numero = request.data['telephone']

            photo = request.data['photo']
            print (' cc ')
            user = User.objects.get(telephone=numero)
            print (' ok 1')

            # request.data['photo'] = str(user.telephone) + '.png'
            user.photo = photo
            print (user.photo)
            print (' ok 2')

            user.save()
            print (' ok 3')
            return Response(data={'status': 0, 'message': 'Success Photo'})

        except:
            return Response(data={'status': 1, 'message': 'Echec de la Photo'})






@api_view(['PUT'])
def forget_password(request):

    if request.method == "PUT":

        try:
            numero = request.data['telephone']
            email = request.data['email']


            photo = request.data['photo']
            print (' cc ')
            user = User.objects.get(telephone=numero)
            print (' ok 1')

            # request.data['photo'] = str(user.telephone) + '.png'
            user.photo = photo
            print (user.photo)
            print (' ok 2')

            user.save()
            print (' ok 3')
            return Response(data={'status': 0, 'message': 'Success Photo'})

        except:
            return Response(data={'status': 1, 'message': 'Echec de la Photo'})





@api_view(['PUT'])
def email(request):

    if request.method == "PUT":
        try:
            # user = User.objects.get(email=email)
            emails = request.data['email']
            # num = request.data['telephone']

            user = User.objects.filter(Q(email=emails) | Q(telephone=emails))
            print (user)

            print(' ok 1')
            print(user[0].email)

            # print (user[6])
            print(' ok 2')

            if user is not None:
                print (' cccccc ')
                new_password = randint(100000, 1000000)
                print (new_password)

                print (' 1111111111 ')
                user[0].password = new_password
                print (user[0].password)
                print (' 2222222222 ')

                print (user[0].password)

                print(' ok 3')

                user[0].save(update_fields=['password'])
                print(' ok 4')
                user[0].save()
                print(' ok 5')


                send_mail('Nouveau mot de passe', 'Your password '+str(new_password), '',
                          [user[0].email])
                return Response(data={'status': 0, 'message': 'Success Email'})

            else:
                return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email  1'})
        except:
            return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email 2'})










# @api_view(['POST'])
# def email(request):
#
# if request.method == "POST":
#
#     try:
#
#         numero = request.data['telephone']
#         email = request.data['email']
#
#         user = User.objects.get(email=email)
#         # user = User.objects.filter(Q(email=email) | Q(telephone=numero))
#         print (user)
#
#         print(' ok 1')
#         # print (user.get('email'))
#
#         if user is not None:
#
#             new_password = randint(100000, 1000000)
#             print (new_password)
#
#             print (user.email)
#
#             print(' ok 2')
#
#             send_mail('Nouveau mot de passe', 'Your password ' + str(new_password),
#                       'alioune.mane@qualshore.com',
#                       [user.email])
#
#             print(' ok 3')
#
#             return Response(data={'status': 0, 'message': 'Success Email'})
#
#         else:
#             return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email  1'})
#
#     except:
#         return Response(data={'status': 1, 'message': 'Echec de l\' envoie de l\'email 2'})













    # subject = request.POST.get('subject', '')
    # message = request.POST.get('message', '')
    # from_email = request.POST.get('from_email', '')
    # if subject and message and from_email:


    #     try:
    #         send_mail(subject, message, from_email, ['admin@example.com'])
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')



    # send_mail('<Your subject>', '<Your message>', 'alioune.mane@qualshore.com', ['alioune.mane@qualshore.com'])
    # return HttpResponse(' Envoyé ')

























#
# @api_view(['PUT'])
# def valid_img(img):
#     """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
#     type = img.format
#     if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
#         try:
#             img.verify()
#             return True
#         except:
#             return False
#     else: return False
#
#
#
#
# @api_view(['PUT'])
# def download_image(url):
#     """Downloads an image and makes sure it's verified.
#
#     Returns a PIL Image if the image is valid, otherwise raises an exception.
#     """
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'} # More likely to get a response if server thinks you're a browser
#     r = urllib.request.Request(url, headers=headers)
#     request = urllib.request.urlopen(r, timeout=10)
#     image_data = StringIO.StringIO(request.read()) # StringIO imitates a file, needed for verification step
#     # image_data = CStringIO.StringIO(request.read()) # StringIO imitates a file, needed for verification step
#     img = Image.open(image_data) # Creates an instance of PIL Image class - PIL does the verification of file
#     img_copy = copy.copy(img) # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
#     if valid_img(img_copy):
#         return img
#     else:
#         # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
#         return Response('An invalid image was detected when attempting to save a Product!')
#
#
#
# @api_view(['PUT'])
# def save_image(request, ):
#     url = ''
#
#
#
#     numero = request.data['telephone']
#     photo = request.data['photo']
#     user = User.objects.get(telephone=numero)
#
#     if user.photo != '' and url != '':
#         image = download_image(url) # See function definition below
#         try:
#             filename = urljoin.urlparse(url).path.split('/')[-1]
#             user.photo = filename
#             tempfile = image
#             tempfile_io = StringIO.StringIO() # Will make a file-like object in memory that you can then save
#             tempfile.save(tempfile_io, format=image.format)
#             user.photo.save(filename, ContentFile(tempfile_io.getvalue()), save=False) # Set save=False otherwise you will have a looping save method
#             return Response(' Enregistrement effectué ')
#         except:
#             # print ("Error trying to save model: saving image failed: ")
#             return Response('  Erreur enregistrement image')





