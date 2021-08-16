from rest_framework import serializers
from .models import Post

# create serialixer
class PostSerializer(serializers.ModelSerializer):
    # required meta
    class Meta:
        model = Post
        fields = (
            'pk',
            'title',
            'custom_id',
            'category',
            'publish_date',
            'last_update',
        )
