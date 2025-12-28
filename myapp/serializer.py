from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','password','email','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect username or password")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return{
            'username': instance.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','checkmark','image']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['content']

class PostListSerializer(serializers.ModelSerializer):
    media_post = ContentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['media_post']


class UserDetailSerializer(serializers.ModelSerializer):
    user_post = PostListSerializer(many=True, read_only=True)
    posts_count = serializers.IntegerField(read_only=True,source='user_post.count')
    followers_count = serializers.IntegerField(read_only=True,source='followers.count')
    followings_count = serializers.IntegerField(read_only=True,source='followings.count')
    class Meta:
        model = UserProfile
        fields = ['id','username','image','bio','website',
                  'checkmark','followers_count','followings_count','posts_count','user_post']

class FollowersSerializer(serializers.ModelSerializer):
    follower = UsernameSerializer(read_only=True)
    following = UsernameSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['follower', 'following']



class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['hashtag']


class PostDetailSerializer(serializers.ModelSerializer):
    media_post = ContentSerializer(read_only=True, many=True)
    user = UsernameSerializer(read_only=True)
    comments_count = serializers.IntegerField(default=0,read_only=True)
    likes_count = serializers.IntegerField(default=0,read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id','media_post','user','description','hashtags','comments_count','likes_count','created_at','updated_at',]



class CommentSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user','text','parent','created_at']

class UserLiked(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    class Meta:
        model = PostLike
        fields = ['user','created_at']

class StorySerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    class Meta:
        model = Story
        fields = ['id','user','image','video','created_at']

class SaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveItem
        fields = '__all__'
