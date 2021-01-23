from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
