from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$',views.home, name = 'home'),
    url(r'^logout/',views.user_logout, name = 'logout'),
    url(r'^login/', views.login,name = 'login'),
    url(r'^profile/(?P<author_id>\w+)/tweet/(?P<tweet_id>\w+)',views.tweet_page,name='tweet'),
    url(r'^profile/(?P<id>\w+)',views.tweets,name = 'tweets'),
    url(r'^users/',views.users_page,name = 'users_page'),
    url(r'^test/',views.test,name = 'test')
]
