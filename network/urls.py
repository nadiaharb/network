
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts", views.allposts, name="allposts"),
    path("profile/<str:username>", views.profile, name='profile'),
    path("edit/<int:id>", views.edit, name="edit"),
    path("following/<str:username>", views.following, name="following"),
    #API routes

    path("editpost/<int:id>", views.editpost, name="editpost"),
    path("likes/<int:id>", views.likes, name="likes"),
    path("likedposts/<int:id>", views.likedposts, name="likedposts"),
    path("alllikedposts/<str:user>", views.all_likedposts, name="alllikedposts"),

]
