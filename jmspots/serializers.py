from jmspots.models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    spot = SpotSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'



class InstitutionSerializer(serializers.ModelSerializer):
    spot = SpotSerializer(read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    institution = InstitutionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Card
        fields = '__all__'


class UserCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = '__all__'


class UserCardFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCardFavourite
        fields = '__all__'