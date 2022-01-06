from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import os
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Following, Liked
import json
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, TemplateView


def index(request):
    user = request.user
    posts = Post.objects.all().order_by('-date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'posts': posts, 'user': user, 'page_obj': page_obj}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def allposts(request):
    posts = Post.objects.all().order_by('-date')
    posts_json = serializers.serialize("json", posts)

    posts = Post.objects.all().order_by('-date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # data = list(Post.objects.values())
   # user = request.user
    if request.user.is_authenticated:
        user = request.user
        liked=Liked.objects.filter(username=user,liked=True)


        liked_posts=[]



        for i in liked:
          liked_posts.append('likebtn' + str(i.post.id))
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
               instance = form.save(commit=False)
               instance.username = request.user
               instance.save()

               return HttpResponseRedirect('/allposts')
        else:
           form = forms.PostForm()

    else:
      context = {'posts': posts,  'posts_json': posts_json, 'page_obj': page_obj}
      return render(request, 'network/allposts.html', context)






    # return JsonResponse([post.serialize() for post in posts], safe=False)
    context={'posts': posts, 'user': user, 'posts_json': posts_json, 'page_obj': page_obj,
                   'liked_posts':liked_posts,
                    'form': form
                   }
    return render(request, 'network/allposts.html',context)


def profile(request, username):
    username = User.objects.get(username=username)
    posts = Post.objects.filter(username=username).order_by('-date')

    followers = Following.objects.filter(subscription=username).count()
    subscriptions = Following.objects.filter(username=username).count()
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    if request.user.is_authenticated:
           user = request.user
           current_user = User.objects.get(username=user)
           liked = Liked.objects.filter(username=current_user, liked=True)

           if Following.objects.filter(username=current_user, subscription=username).exists():
               x=True
           else:
               x=False

           liked_posts = []

           for i in liked:
               liked_posts.append('likebtn' + str(i.post.id))

           try:
               follow = Following.objects.get(username=current_user, subscription=username)
               message = 'Yau are following this user'
               if request.method == "POST":
                   follow.delete()
                   return HttpResponseRedirect(reverse("profile", kwargs={'username': username}))

           except ObjectDoesNotExist:
               message = 'Yau are not following this user'
               if request.method == "POST":
                   follow, created = Following.objects.get_or_create(username=current_user, subscription=username,
                                                                     subat=0,
                                                                     subto=0)

                   # context={'username':username, 'posts':posts,'current_user':current_user, 'ex':ex }
                   return HttpResponseRedirect(reverse("profile", kwargs={'username': username}))

    else:
        return render(request, "network/profile.html",
                      {'username': username, 'posts': posts,
                       'followers': followers, 'subscriptions': subscriptions, 'page_obj': page_obj,
                       })

    return render(request, "network/profile.html",
                  {'username': username, 'posts': posts, 'current_user': current_user, 'message': message,
                   'followers': followers, 'subscriptions': subscriptions, 'page_obj': page_obj,
                   'liked_posts':liked_posts, 'x':x})

@login_required
@csrf_exempt
def edit(request, id):
    mypost = Post.objects.get(id=id)
    post = serializers.serialize('json', [Post.objects.get(id=id)])

    if request.method == "GET":
        return HttpResponse(post)

    if request.method == "POST":
        data = json.loads(request.body)
        mypost.text = data['text']
        mypost.save()
        return HttpResponseRedirect(reverse("allposts"))

@login_required
def following(request, username):
    username = User.objects.get(username=username)
    if Following.objects.filter(username=request.user).exists():
        current_user = Following.objects.filter(username=request.user)
        all_subscriptions = [i.subscription.username for i in current_user]

        posts = []

        for i in all_subscriptions:
            subs = User.objects.get(username=i)
            posts += Post.objects.filter(username=subs).order_by('-date')
        liked = Liked.objects.filter(username=username, liked=True)

        liked_posts = []





        for i in liked:
            liked_posts.append('likebtn'+str(i.post.id))

        p = Paginator(posts, 10)
        page_number = request.GET.get('page')

        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        return render(request, "network/following.html",
                      {'current_user': current_user,
                       'all_subscriptions': all_subscriptions,
                       'posts': posts,
                       'subs': subs,
                       'page_obj': page_obj,
                       'liked_posts':liked_posts
                       })

    else:
        current_user = request.user
        message = "You not following anyone"
        return render(request, "network/following.html",
                      {'current_user': current_user,
                       'message': message
                       })


@csrf_exempt
def editpostold(request, id):
    try:
        post = Post.objects.filter(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "No post found."}, status=404)

    if request.method == "GET":
        post = list(post.values())
        return JsonResponse(post, safe=False)

    elif request.method == "POST":

        post = Post.objects.filter(id=id)
        post.text = request.Post["text"]

        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PATCH request required."
        }, status=400)


@csrf_exempt
def editpost(request, id):
    if request.method == "GET":
        post = Post.objects.filter(id=id)
        post = list(post.values())
        return JsonResponse(post, safe=False)

    if request.method == 'POST' and request.is_ajax():
        try:
            post = Post.objects.get(id=id)
            post.text = request.POST['text']
            post.save()
            return HttpResponse(status=204)
        except Post.DoesNotExist:
            return JsonResponse({"error": "No post found."}, status=404)
    else:
        return JsonResponse({
            "error": "GET or PATCH request required."
        }, status=400)





@login_required
@csrf_exempt
def likes(request, id):
    if request.method == "GET":
        post = Post.objects.filter(id=id)
        post = list(post.values())
        return JsonResponse(post, safe=False)

    if request.method == 'POST' and request.is_ajax():
        try:
            post = Post.objects.get(id=id)
            user = User.objects.get(username=request.user)
            post.likes = request.POST['likes']
            post.save()


            return HttpResponse(status=204)
        except Post.DoesNotExist:
            return JsonResponse({"error": "No post found."}, status=404)
    else:
        return JsonResponse({
            "error": "GET or PATCH request required."
        }, status=400)


@csrf_exempt
def likedposts(request, id):
    if request.method == "GET":
      try:
        post = Post.objects.get(id=id)
        user = User.objects.get(username=request.user)
        liked_post=Liked.objects.get(post=post, username=user)
        return HttpResponse(liked_post)
      except Post.DoesNotExist:
       return JsonResponse({"error": "No post found."}, status=404)
    if request.method == 'POST':

       post = Post.objects.get(id=id)
       user = User.objects.get(username=request.user)
       if Liked.objects.filter(post=post, username=user):
           liked_post=Liked.objects.filter(post=post, username=user)
           liked = request.POST['liked']
           unliked = request.POST['unliked']
           liked_post.update(liked=liked, unliked=unliked)
           return HttpResponse(status=204)

       else:
           liked_post = Liked.objects.create(post=post, username=user)
           liked_post.liked = request.POST['liked']
           liked_post.unliked=request.POST['unliked']
           liked_post.save()
           return HttpResponse(status=204)




def all_likedposts(request,user):
    user = User.objects.get(username=request.user)
    liked_posts=Liked.objects.filter(username=user,liked=True)
    posts_id=[]


    for i in liked_posts:
        posts_id.append(i.post.id)
    return JsonResponse(posts_id, safe=False)

class RestrictedView(LoginRequiredMixin, TemplateView):
    template_name = 'network/following.html'
    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You are not allowed here."