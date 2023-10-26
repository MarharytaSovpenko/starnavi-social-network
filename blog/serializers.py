from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )

    class Meta:
        model = Post
        fields = ("id", "author", "title", "description", "created_at", "likes")
