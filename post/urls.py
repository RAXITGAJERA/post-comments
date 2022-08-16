from django.urls import path

from post import views

urlpatterns = [
    path("", views.login, name="loginpage"),
    path("createprofile/", views.create_profile, name="createprofilepage"),
    path("logout/", views.logout, name="logoutpage"),
    path("index/", views.index, name="indexpage"),
    path("edit/<int:id>/", views.edit_post, name="edit"),
    path("updatepost", views.update_post, name="updatepostpage"),
    path("like/<int:id>/", views.like_post, name="like"),
    path("dislike/<int:id>/", views.dislike_post, name="dislike"),
    path("deletepost/<int:id>/", views.deletet_post, name="delete"),
    path("addcoments/<int:id>/", views.addcoments, name="addcomentspage"),
    path("postcomments", views.comments_post, name="comments"),
    path("editcomment/<int:id>/", views.edit_comment, name="editcomment"),
    path("updatecomment", views.update_comment, name="updatecommentpage"),
    path("deletecomments/<int:id>/", views.deletet_comments, name="deletecomments"),
]
