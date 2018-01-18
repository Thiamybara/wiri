from django.conf.urls import url
from jmspots.views import *
from jmspots import views as myapp_views


urlpatterns = [

    url(r'^$', CategorytList.as_view()),
    url(r'^card/$', CardList.as_view()),
    url(r'^event/$', EventList.as_view()),
    url(r'^institution/$', InstitutionList.as_view()),
    url(r'^spot/$', SpotList.as_view()),
    url(r'^usercard/$', UserCardList.as_view()),
    url(r'^usercardfavourite/$', UserCardFavouriteList.as_view()),
    url(r'^listFavourite/$', myapp_views.listFavourite, name='listFavourite'),

    #url(r'^listcardInstitutionelEvent/$', myapp_views.listcardInstitutionelEvent, name='listcardInstitutionelEvent'),

]