from django.conf.urls import url

#from users import views as myapp_views
from jmspots import views as myapp_views



from django.conf.urls import url
from jmrequests.views import *
from jmrequests import views as myapp_views

urlpatterns = [
    url(r'^$', RequestList.as_view()),
    url(r'^requestReceivers/$', Request_ReceiversList.as_view()),
    url(r'^jmrequest_join_me/$', myapp_views.jmrequest_join_me, name='jmrequest_join_me'),
    url(r'^jmrequest_join_me_card/$', myapp_views.jmrequest_join_me_card, name='jmrequest_join_me_card'),
    url(r'^jmrequest_joiner/$', myapp_views.jmrequest_joiner, name='jmrequest_joiner'),
    url(r'^invitation/$', myapp_views.invitation, name='invitation'),
]