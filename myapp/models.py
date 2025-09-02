from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone


class UserProfile(AbstractUser):
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="profile_images/",null=True, blank=True)
    website = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} - {self.following.username}'

class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    video = models.FileField(upload_to="post_videos/", null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Posts by {self.user}'

class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.like} {self.user}'

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=64,null=True,blank=True)
    post = models.ManyToManyField(Post)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.hashtag} {self.post}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user}'

class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
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

