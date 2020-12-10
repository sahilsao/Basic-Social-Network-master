
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.userProfile, name="userProfile"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name="like"),
    path("editPost", views.editPost, name="editPost"),
    path("followPage", views.followPage, name="followPage"),
]
