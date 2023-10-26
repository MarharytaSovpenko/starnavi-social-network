from django.contrib.auth import get_user_model
from rest_framework import generics

from rest_framework.permissions import AllowAny


from user.serializers import UserSerializer, UserActivitySerializer


class UserSerializerMixin:
    serializer_class = UserSerializer


class CreateUserView(UserSerializerMixin, generics.CreateAPIView):
    permission_classes = (AllowAny,)


class ManageUserView(UserSerializerMixin, generics.RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user


class UserActivityView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserActivitySerializer
