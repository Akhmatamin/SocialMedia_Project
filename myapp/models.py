from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone


class UserProfile(AbstractUser):
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="profile_images/",null=True, blank=True)
    website = models.URLField(null=True,blank=True)
    age = models.PositiveSmallIntegerField(null=True,blank=True)
    checkmark = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)
    public_account = models.BooleanField(default=True)


    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='follower_username')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='following_username')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} - {self.following.username}'


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=64,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.hashtag}'


class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='post_username')
    description = models.TextField(null=True,blank=True)
    hashtags = models.ManyToManyField(Hashtag,related_name='hashtag_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comments_enable = models.BooleanField(default=True)
    saved = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f'Posts by {self.user},{self.created_at}'

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_post')
    content = models.FileField(upload_to='media/')


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user}'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user}'

class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'CommentLike {self.user}'

def default_expiry():
    return timezone.now() + timedelta(hours=24)

class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="story_images/", null=True, blank=True)
    video = models.FileField(upload_to="story_videos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return f'Story by {self.user}'

class SaveItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return f'Saved {self.post}'



class Chat(models.Model):
    users = models.ManyToManyField(UserProfile)
    date_oppened = models.DateField(auto_now_add=True)


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="messages_images/", null=True, blank=True)
    files = models.FileField(upload_to='messages_files/',null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)



