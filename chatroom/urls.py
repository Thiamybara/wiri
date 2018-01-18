from django.conf.urls import url
from users.views import *
from chatroom.views import *
from chatroom import views as myapp_views


urlpatterns = [
    url(r'^$', MessageList.as_view()),
    url(r'^group/$', ChatGroupList.as_view()),
    url(r'^media/$', MediaList.as_view()),
    url(r'^getGroupList/$', myapp_views.getGroupList, name='getGroupList'),
    url(r'^addUserGroup/$', myapp_views.addUserGroup, name='addUserGroup'),

]
