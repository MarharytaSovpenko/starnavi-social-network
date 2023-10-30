from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


def get_anonymous_user():
    return get_user_model().objects.get_or_create(
        gmail="anonymous", password="anonymous"
    )[0]


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_anonymous_user),
        related_name="authored_posts",
    )
    title = models.CharField(max_length=125, unique=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="liked_posts",
        through="LikeDate",
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class LikeDate(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET(get_anonymous_user)
    )
    date_of_like = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("author", "post")
