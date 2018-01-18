from django.db import models
from users.models import *



class ChatGroup(models.Model):
    content = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    userss = models.ForeignKey(User, related_name='admin_group', on_delete=models.CASCADE)
    users =  models.ManyToManyField(User, related_name='group_users')

    def __str__(self):
        return str(self.created)


class Message(models.Model):
    content = models.CharField(max_length=255)
    users =  models.ForeignKey(User, on_delete=models.CASCADE)
    # users =  models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.FileField(null=True, upload_to='chatroom/')
    chatgroup = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Media(models.Model):
    image = models.FileField(null=True, upload_to='medias/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


