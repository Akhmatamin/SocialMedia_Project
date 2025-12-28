from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import *

class PostMediaInline(TabularInline):
    model = PostMedia

class CommentInline(TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('hashtags',)
    inlines = [PostMediaInline]

admin.site.register(UserProfile)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(Follow)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Hashtag)
admin.site.register(SaveItem)


