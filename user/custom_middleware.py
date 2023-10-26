from django.contrib.auth import get_user_model
from django.utils.timezone import now


class SetLastRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:

            get_user_model().objects.filter(pk=request.user.pk).update(
                last_request=now()
            )

        return response
