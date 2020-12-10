import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    current_user = request.user

    return render(request, "network/index.html", {'current_user': current_user, 'page_obj': page_obj})


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


@login_required
def create_post(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        content = request.POST['new_post']
        newPost = Post(user=current_user, content=content)
        newPost.save()
        return HttpResponseRedirect(reverse('index'))

def userProfile(request, username):
    current_user = request.user
    target_user = User.objects.get(username=username)
    total_followers = Follow.objects.filter(following=target_user).count()
    total_following = Follow.objects.filter(follower=target_user).count()

    posts = Post.objects.filter(user=target_user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if current_user.is_authenticated:
        try:
            Follow.objects.get(follower=request.user, following=target_user)
            is_follower = True

        except ObjectDoesNotExist as e:
            is_follower = False

    else:
        is_follower = None

    context = {
        "target_user": target_user,
        "total_followers": total_followers,
        "total_following": total_following,
        "page_obj": page_obj,
        "is_follower": is_follower,
        "current_user": current_user
    }
    return render(request, "network/userProfile.html", context)


@csrf_exempt
def follow(request):
    if request.method == 'PUT':
        current_user = request.user
        data = json.loads(request.body)

        if data["whatDo"] == 'Follow':
            targetUser = User.objects.get(username=data["target_User"])
            newFollower = Follow(follower=current_user, following=targetUser)
            newFollower.save()
            return HttpResponse(status=200)

        else:
            targetUser = User.objects.get(username=data["target_User"])
            follower = Follow.objects.get(follower=current_user, following=targetUser)
            follower.delete()
            return HttpResponse(status=200)


@csrf_exempt
def like(request):
    if request.method == 'PUT':
        current_user = request.user
        data = json.loads(request.body)
        target_post = data["target_Post"]
        target_post = target_post.replace("post_", "")

        if data["whatDo"] == 'Like':
            targetPost = Post.objects.get(id=target_post)
            targetPost.liked_by.add(current_user)
            targetPost.total_likes += 1
            targetPost.save()
            return HttpResponse(status=200)

        else:
            targetPost = Post.objects.get(id=target_post)
            targetPost.liked_by.remove(current_user)
            targetPost.total_likes -= 1
            targetPost.save()
            return HttpResponse(status=200)

@csrf_exempt
def editPost(request):
    if request.method == 'PUT':
        current_user = request.user
        data = json.loads(request.body)
        target_post = data["target_Post"]
        target_post = target_post.replace("post_", "")

        targetPost = Post.objects.get(id=target_post)
        targetPost.content = data["newContent"]
        targetPost.save()
        return HttpResponse(status=200)

def followPage(request):
    current_user = request.user
    followerObjects = Follow.objects.filter(follower=current_user)
    listOfUsers = []

    for item in followerObjects:
        listOfUsers.append(item.following)

    posts = Post.objects.filter(user__in=listOfUsers).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/followPage.html", {'current_user': current_user, 'page_obj': page_obj})