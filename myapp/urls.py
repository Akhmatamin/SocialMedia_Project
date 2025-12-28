from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework import routers

router = DefaultRouter()

router.register(r'followings',FollowerViewSet,basename='following')
router.register(r'hashtags',HashtagViewSet,basename='hashtags')
router.register(r'story',StoryViewSet,basename='stories')
router.register(r'userprofile',UserProfileViewSet,basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('post/', PostListAPIView.as_view(), name='post-list'),
    path('posts/', PostAPIView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/',PostCommentAPIView.as_view(), name='post-comments'),
    path('posts/<int:pk>/users-liked/',UsersLikedAPIView.as_view(), name='users-liked'),
    path('posts/<int:pk>/like/',PostLikeAPIView.as_view(), name='post-likes'),
]