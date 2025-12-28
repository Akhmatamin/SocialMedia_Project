from django_filters import FilterSet
from .models import *

class UserProfileFilter(FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'username':['icontains'],
            'bio':['icontains'],
        }

class HashtagFilter(FilterSet):
    class Meta:
        model = Hashtag
        fields = {
            'hashtag':['exact'],
}