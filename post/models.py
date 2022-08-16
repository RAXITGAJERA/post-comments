from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profilepics")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


# LIKE_CHOICES = (
#     ("Like", "Like"),
#     ("Unlike", "Unlike"),
# )


# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
#     value = models.CharField(choices=LIKE_CHOICES, default="Like", max_length=30)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
