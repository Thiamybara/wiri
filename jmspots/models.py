from django.db import models
from users.models import User
from chatroom.models import ChatGroup


class Spot(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return str(self.latitude)+' '+str(self.longitude)+' '+str(self.name)



class Event(models.Model):
    name = models.CharField(max_length=105)
    description = models.CharField(max_length=255, blank=True, null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    chatroom = models.OneToOneField(ChatGroup, blank=True, null=True)



    def __str__(self):
        return self.name

    #
    # def natural_keys(self):
    #     return self.event.id, self.event.name, self.event.description, self.event.jm_tag, str(self.event.created)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name



class Card(models.Model):
    file = models.FileField(null=True, upload_to='cards/')
    jm_tag = models.CharField(max_length=150, unique=True)
    institution = models.OneToOneField(Institution, blank=True, null=True)
    event = models.OneToOneField(Event, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.institution)




class UserCard(models.Model):
    sender = models.ForeignKey(User, related_name='sender_card', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(User, related_name='receivers_card')
    #card = models.ManyToManyField(Card, null=True, blank=True)
    card = models.ForeignKey(Card, null=True, blank=True)
    date_created = models.DateTimeField(null=True)

    def __str__(self):
        return self.sender



class UserCardFavourite(models.Model):
    sender = models.ForeignKey(User, related_name='sender_cardfavourite', on_delete=models.CASCADE)
    #receivers = models.ManyToManyField(User, related_name='receivers_card')
    card = models.ManyToManyField(Card)
    date_created = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.sender)