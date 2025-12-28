from http.client import HTTPResponse

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializer import *
from django.db.models import Count


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializer

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.annotate(comments_count=Count('comments',distinct=True),
                                     likes_count=Count('likes',distinct=True)).select_related('user')

class PostAPIView(generics.ListCreateAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.annotate(comments_count=Count('comments',distinct=True),
                                     likes_count=Count('likes',distinct=True)).select_related('user')


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class PostCommentAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id).select_related('user')

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(user=self.request.user, post_id=post_id)


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        if liked:
            return Response({'message':'liked'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'not liked'},status=status.HTTP_200_OK)

class UsersLikedAPIView(generics.ListAPIView):
    serializer_class = UserLiked

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return UserProfile.objects.filter(postlike__post_id=post_id).distinct().select_related('user')



class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer