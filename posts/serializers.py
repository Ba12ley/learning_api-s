from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post


User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username'
        )

# create serializer
class PostSerializer(serializers.ModelSerializer):

    owner = serializers.HyperlinkedIdentityField(many=False, view_name='owner-detail')
    # required meta
    class Meta:
        model = Post
        fields = (
            'pk',
            'owner',
            'title',
            'custom_id',
            'category',
            'publish_date',
            'last_update',
        )
