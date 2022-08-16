from django.contrib import admin

from .models import Comment, Post, Profile

# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["profile", "post_id", "date_posted", "comments", "user_id"][::-1]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["profile", "date_posted", "post", "user"][::-1]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_picture", "user"][::-1]


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ["post", "user"]
