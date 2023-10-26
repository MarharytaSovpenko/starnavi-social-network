from django.urls import path, include
from rest_framework import routers

from blog.views import PostsViewSet


router = routers.DefaultRouter()
router.register("posts", PostsViewSet, basename="post")

urlpatterns = [path("", include(router.urls))]

app_name = "blog"
