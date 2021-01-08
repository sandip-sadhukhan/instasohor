from django.urls import path
from . import views

urlpatterns = [
    # user activity
    # default feed here
    path('', views.feed, name="feed"),
    # add a post
    path('add-post/', views.addPost, name="addPost"),
    # searching
    path('search/', views.search, name="search"),
    # view a single post
    path('post/<int:id>/', views.post, name="post"),
    # user profile
    path('u/<str:username>/', views.user, name="user"),
    # your profile
    path('profile/', views.profile, name="profile"),
    # edit profile
    path('edit-profile/', views.editProfile, name="editProfile"),
    # show followers
    path('u/<str:username>/followers/', views.followers, name='followers'),
    # show followers
    path('u/<str:username>/following/', views.following, name='following'),
    # toggle follow
    path('toggle-follow/<str:username>/', views.toggleFollow, name='toggleFollow'),
    # single post
    path('p/<int:id>/', views.singlePost, name='singlePost'),
    # comment
    path('c/<int:postId>/', views.comment, name='comment'),
    # like
    path('l/<int:postId>/', views.like, name='like'),
    # delete
    path('d/<int:postId>/', views.delete, name='delete'),

    # authentication
    # register
    path('register/', views.register, name="register"),
]
