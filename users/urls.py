from django.conf.urls import url
from users.views import *
from users import views as myapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', UserList.as_view()),
    url(r'^interests/$', InterestList.as_view()),
    url(r'^favourite/$', FavouriteContactList.as_view()),
    # url(r'^interests/media/$', myapp_views.media, name='media'),

    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^inscription/$', myapp_views.inscription, name='inscription'),
    url(r'^validation/$', myapp_views.validation_Code, name='validation_Code'),
    url(r'^contacts/$', myapp_views.contacts, name='contacts'),
    url(r'^authentification/$',myapp_views.authentification, name='authentification'),
    url(r'^listInterest/$', myapp_views.listInterest, name='listInterest'),
    url(r'^complements_info/$', myapp_views.complements_info, name='complements_info'),
    url(r'^save_interest/$', myapp_views.save_interest, name='save_interest'),
    url(r'^addFavoriteContact/$', myapp_views.addFavoriteContact, name='addFavoriteContact'),
    url(r'^addFavoriteContact2/$', myapp_views.addFavoriteContact2, name='addFavoriteContact2'),
    url(r'^getFavoriteContact/$', myapp_views.getFavoriteContact, name='getFavoriteContact'),
    url(r'^modify_info/$', myapp_views.modify_info, name='modify_info'),
    url(r'^modify_password/$', myapp_views.modify_password, name='modify_password'),
    url(r'^edit_photo/$', myapp_views.edit_photo, name='edit_photo'),
    url(r'^save_image/$', myapp_views.save_image, name='save_image'),
    url(r'^email/$', myapp_views.email, name='email'),
    # url(r'^verif_user/$', myapp_views.verif_user, name='verif_user'),
    url(r'^verif_user/(?P<telephone>[0-9]+)/$', myapp_views.verif_user, name='verif_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)