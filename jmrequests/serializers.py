from jmrequests.models import *
from rest_framework import serializers
from jmspots.serializers import SpotSerializer, CardSerializer
from users.serializers import UserSerializer




class RequestSerializer(serializers.ModelSerializer):

    spot =  SpotSerializer(read_only=True)
    card = CardSerializer(read_only=True)
    # sender = UserSerializer(read_only=True)
    # receivers = Request_ReceiversSerializer(read_only=True)


    class Meta:
        model = Request
        fields = '__all__'



class Request_ReceiversSerializer(serializers.ModelSerializer):

    # spot =  SpotSerializer(read_only=True)
    # card = CardSerializer(read_only=True)


    # sender = UserSerializer(read_only=True)
    # list_receivers = UserSerializer(read_only=True)
    # receivers = RequestSerializer(read_only=True)


    class Meta:
        model = Request_Receivers
        fields = '__all__'


