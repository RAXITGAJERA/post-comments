from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import redirect, render

from .models import Comment, Post, Profile


# Create Profile
def create_profile(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        profile_picture = request.FILES["profile_picture"]

        if password != password2:
            messages.error(request, "your password not match")
            return redirect("createprofilepage")
        else:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, profile_picture=profile_picture)
            if profile:
                messages.success(request, "Profile Created Please Login")
                return redirect("loginpage")
    return render(request, "Signup.html")


# for login
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "login success")
            return redirect("indexpage")
        else:
            messages.error(request, "your detail not match in database")
            return redirect("loginpage")
    return render(request, "login.html")


# for logout
def logout(request):
    auth_logout(request)
    return redirect("loginpage")


# for display all post
def index(request):
    postdata = (
        Post.objects.prefetch_related("comment_post")
        .annotate(c_count=Count("comment_post__id", distinct=True), like=Count("likes", distinct=True))
        .values("id", "profile__profile_picture", "user__username", "date_posted", "post", "c_count", "like")
        .distinct()
    )
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == "POST":
        posts = request.POST["posts"]
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.create(user=request.user, post=posts, profile=profile)
        messages.success(request, "POST Uploaded")
    construct = {"postdata": postdata, "profileimage": profileimage}
    return render(request, "index.html", construct)


# for edit post
def edit_post(request, id):
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    data = Post.objects.get(id=id)
    construct = {"data": data, "profileimage": profileimage}
    return render(request, "editpost.html", construct)


def update_post(request):
    id = request.POST["post_id"]
    editpost = Post.objects.get(id=id)
    editpost.post = request.POST["posts"]
    editpost.save()
    messages.success(request, "POST Updated")
    return redirect("indexpage")


def like_post(request, id):
    if request.method == "POST":
        like = Post.objects.get(id=id)
        if like.likes.filter(id=request.user.id).exists():
            messages.success(request, "You Already Like This POST ")

        else:
            like.likes.add(request.user)
            messages.success(request, "POST Like")
        return redirect("indexpage")


def dislike_post(request, id):
    if request.method == "POST":
        like = Post.objects.get(id=id)
        like.likes.remove(request.user)
        messages.success(request, "POST Unlike")
        return redirect("indexpage")


# for delete post
def deletet_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("indexpage")


# for add comment and show comments
def addcoments(request, id):
    postdata = (
        Post.objects.prefetch_related("comment_post")
        .annotate(c_count=Count("comment_post__id", distinct=True), like=Count("likes", distinct=True))
        .values("id", "profile__profile_picture", "user__username", "date_posted", "post", "c_count", "like")
        .distinct()
        .get(id=id)
    )
    comments = Comment.objects.filter(post_id=id)
    construct = {"postdata": postdata, "comments": comments}
    return render(request, "commentspost.html", construct)


def comments_post(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        comments = request.POST.get("comments")
        user = request.user
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        comment = Comment(comments=comments, user_id=user, post_id=post, profile=profile)
        comment.save()
    return redirect("indexpage")


# for edit comments
def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    return render(request, "editcomment.html", {"comment": comment})


def update_comment(request):
    id = request.POST["comment_id"]
    comment = Comment.objects.get(id=id)
    comment.comments = request.POST["comments"]
    comment.save()
    messages.success(request, "Comment Updated")
    return redirect("indexpage")


# for delete comment
def deletet_comments(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    messages.success(request, "Comment Deleted")
    return redirect("indexpage")
