from chatroom.models import *
from rest_framework import serializers

class ChatGroupSerializer(serializers.ModelSerializer):
    # spot =  SpotSerializer(read_only=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'



class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


