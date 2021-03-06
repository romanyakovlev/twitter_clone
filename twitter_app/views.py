# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_
from .models import Tweet, Follow, Like, Comments, UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
import re
from twitter_app.forms import UserProfileForm

#   Представление домашней страницы

def home(request):

#      Проверяем, имеет ли залогиненный юзер людей, которых он зафолловил
#      если нет - отображаем любые твиты с помощью GET запроса
        if request.method == 'GET':
            validator = request.GET.get('tweets')
#      Отображаем твиты для инкогнито
        followed_by_you = Tweet.objects.all()
#      Отображаем зафоловленные твиты (если они есть)
        if request.user.is_authenticated:
            person = Follow.objects.get(person=User.objects.get(id=request.user.id))
            followed_by_you = Tweet.objects.filter(author__in = person.follows.all()).all()
        if validator == 'all':
            followed_by_you = Tweet.objects.all()

        followed_by_you = followed_by_you.order_by('-date')

        likes_count = []
        for tweet_ in followed_by_you:
            try:
                likes_count.append(len(Like.objects.get(tweet=tweet_).person.all()))
            except:
                likes_count.append(len([]))

        return render(request,'twitter_app/home.html',{
        'tweets':zip(followed_by_you, likes_count),
        'likes_count': likes_count,
        'author':request.user,'len':len(followed_by_you)})

# Представление страницы твитов определенного пользователя

def tweets(request,id):

    null_text_error = ''

#   Добавляем твит, если пользователь авторизован и длина текстового поля не равна 0

    if request.method == 'POST':
        tweet = request.POST.get('tweet')
        if request.user.is_authenticated == True:
            if len(tweet) != 0:
                Tweet(text = tweet,author = request.user).save()
            else:
                null_text_error = 'You must fill text field'
        else:
            return HttpResponseRedirect('/profile/%s' % id)

#  Фолловим/Отписываемся от пользователя при помощи метода GET

    if request.method == 'GET':
        follow_agree = request.GET.get('follow')
        if follow_agree is not None:
            person = Follow.objects.get(person=User.objects.get(id=request.user.id))
            person.save()
            u1 = User.objects.get(id=id)
            u1.save()
            if u1 in person.follows.all():
                person.follows.remove(u1)
            else:
                person.follows.add(u1)
            person.save()
            return HttpResponseRedirect('/profile/%s' % id)

    if request.user.is_authenticated():
        follow_list = Follow.objects.get(person=User.objects.get(id=request.user.id)).follows.all()
    else:
        follow_list = []

    tweets_list = Tweet.objects.filter(author_id=id).order_by('-date')

    likes_count = []

    for tweet_ in tweets_list:
        try:
            likes_count.append(len(Like.objects.get(tweet=tweet_).person.all()))
        except:
            likes_count.append(len([]))

    user_avatar = UserProfile.objects.get(user=User.objects.get(id=id))

    return render(request,'twitter_app/tweets.html',{'author_tweets':User.objects.get(id=id),
    'follows':follow_list,
    'authors_page_id':id,'tweets':zip(tweets_list, likes_count),'author':request.user,
    'null_text_error':null_text_error,
    'authenticated':request.user.is_authenticated(),
    'avatar':user_avatar,})

# Отдельная страница одного Твита

def tweet_page(request,author_id,tweet_id):

    tweet =Tweet.objects.get(id=tweet_id)

    # Попытка получить количество лайнов, если нету - обрабатывает
    # исключение и создает объект

    try:
        Like.objects.get(tweet=tweet)
    except:
        Like(tweet=tweet).save()
    likes = Like.objects.get(tweet=tweet).person

    # Ставим лайк/дислайк для твитта

    if request.method == 'GET':
        like = request.GET.get('like')
        if like and request.user not in likes.all():
            likes.add(User.objects.get(id=request.user.id))
            return HttpResponseRedirect('/profile/'+author_id+'/tweet/'+tweet_id)
        elif like and request.user in likes.all():
            likes.remove(User.objects.get(id=request.user.id))
            return HttpResponseRedirect('/profile/'+author_id+'/tweet/'+tweet_id)

    is_user_liked = request.user in likes.all()

    #   Работа с хэштегами: выделение имен пользовователей в твитте

    if request.method == "POST":
        text = request.POST.get('text')
        user_profile = UserProfile.objects.get(user=request.user)
        Comments(user=user_profile,comment=tweet,text=text).save()

    comments = Comments.objects.filter(comment=tweet)

    s = tweet.text
    user_words = re.findall(r'(?:\s|^)([$]\w+)(?:\s|$)',s)
    words = s.split(' ')
    user_id = []
    for x in words:
        if x in user_words:
            user_id.append(User.objects.get(username=x[1:]).id)
        else: user_id.append(None)

    return render(request,'twitter_app/tweet_page.html',{'tweet':tweet,
    'author':request.user,'words':zip(words,user_id),
    'user_words':user_words,'user_id':user_id,
    'likes':len(likes.all()),'author_id':author_id,
    'is_user_liked':is_user_liked,
    'authenticated':request.user.is_authenticated(),
    'comments':comments,})

# Страница входа

def login(request):

    error = False
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=login, password=password)
        if user is not None:
            login_(request, user)
        return HttpResponseRedirect('/')
    else:
        error = True
    return render(request,'twitter_app/login.html')

# Страница выхода

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def users_page(request):
    users = User.objects.all()
    user_avatar = UserProfile.objects.all()
    return render(request,'twitter_app/users_page.html',{'users':user_avatar,'author':request.user})


#   Тесты в http:127.0.0.1:8000/test/

def test(request):
    print(vars(request))
    test_user = UserProfile.objects.get(user = User.objects.get(id=1))
    return render(request,'twitter_app/test.html',{'test':test_user.avatar.url})

def del_tweet(request):
    if request.method == "GET":
        id_ = request.GET.get('del_id')
        Tweet.objects.get(id=id_).delete()
        return HttpResponseRedirect('/profile/'+str(request.user.id))

def edit_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm({'image':userprofile.avatar})
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile.avatar = form.cleaned_data['image']
            userprofile.save()
            return HttpResponseRedirect('/profile/{}'.format(request.user.id))
    return render(request, 'twitter_app/profile.html',{'userprofile': userprofile, 'selecteduser': request.user, 'form': form})
