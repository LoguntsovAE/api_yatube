from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        post = get_object_or_404(self.queryset, pk=pk)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments

    def partial_update(self, request, pk, post_id=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        if request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, post_id=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        if request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
