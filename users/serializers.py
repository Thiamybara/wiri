from users.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class InterestSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        return obj.image.url

    class Meta:
        model = Interest
        fields = '__all__'


class FavouriteContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteContact
        fields = '__all__'