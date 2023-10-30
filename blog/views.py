from blog.serializers import PostSerializer
from django.db.models import Count
from blog.models import Post, LikeDate
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
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

    @action(detail=True, methods=["get"])
    def analytics_on_likes(self, request, pk=None):
        post = self.get_object()
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        likes = LikeDate.objects.filter(post=post)

        if date_from:
            likes = likes.filter(date_of_like__date__gte=date_from)

        if date_to:
            likes = likes.filter(date_of_like__date__lte=date_to)

        likes_by_day = likes.values("date_of_like__date").annotate(
            like_count=Count("id")
        )

        formatted_likes = [
            {"date": item["date_of_like__date"], "like_count": item["like_count"]}
            for item in likes_by_day
        ]

        return Response(formatted_likes)
