from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


def get_authenticated_user(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]

        payload = AccessToken(token)

        user_id = payload["user_id"]

        return User.objects.get(id=user_id)

    except Exception:
        return None