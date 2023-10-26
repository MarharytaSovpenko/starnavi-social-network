from blog.serializers import PostSerializer
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from blog.models import Post
from rest_framework.response import Response
from rest_framework.decorators import action


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related("author")
    pagination_class = PageNumberPagination
    pagination_class.page_size = 7

    def perform_create(self, serializer):

        author = self.request.user

        validated_data = serializer.validated_data.copy()
        validated_data.pop("likes", None)

        Post.objects.create(author=author, **validated_data)

    @action(detail=True, methods=["POST"])
    def add_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            return Response(
                {"detail": "User already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post.likes.add(user)
        post.save()

        return Response(
            {"detail": "Like added successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["POST"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response(
                {"detail": "Like removed successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "User hasn't liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )
