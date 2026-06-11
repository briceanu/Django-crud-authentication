import json

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from django_crud.authentication import get_authenticated_user
from django_crud.users.serializes import UserUpdateSerializer

User = get_user_model()


def _serialize_user(user):
	return {
		"id": str(user.id),
		"username": user.username,
		"email": user.email,
		"age": user.age,
		"is_active": user.is_active,
	}


def users_list(request):
	if request.method != "GET":
		return JsonResponse({"error": "Only GET allowed"}, status=405)

	users = [
		{
			"id": str(user.id),
			"username": user.username,
			"email": user.email,
			"age": user.age,
			"is_active": user.is_active,
		}
		for user in User.objects.all()
	]
	return JsonResponse({"data": users})

@csrf_exempt
def user_detail(request):
	if request.method != "GET":
		return JsonResponse({"error": "Only GET allowed"}, status=405)

	user = get_authenticated_user(request)
	
	if not user:
		return JsonResponse(
            {"error": "Invalid credentials"},
            status=401,
        )

	return JsonResponse({"data": _serialize_user(user)})


@csrf_exempt
def user_create(request):
	if request.method != "POST":
		return JsonResponse({"error": "Only POST allowed"}, status=405)
	try:
		data = json.loads(request.body or "{}")
	except json.JSONDecodeError:
		return JsonResponse({"error": "Invalid JSON"}, status=400)

	username = data.get("username")
	email = data.get("email")
	age = data.get("age")
	password = data.get("password")
	if data.get('age') < 18:
		return JsonResponse({"error": "Age must be 18+"}, status=400)

	if not username or not email or not age or not password:
		return JsonResponse(
			{"error": "username, email, age and password are required"},
			status=400,
		)
	try:
		user = User(
			username=username,
			email=email,
			age=age,
		)
		user.set_password(password)
		user.save()
	except IntegrityError:
		return JsonResponse(
            {"error": "Username or email already exists"},
            status=400
        )
	except ValidationError as e:
		return JsonResponse({"error": e.message_dict}, status=400)
	return JsonResponse({"data": _serialize_user(user)}, status=201)


@csrf_exempt
def user_update(request, pk):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT allowed"}, status=405)

    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    if user.pk != pk:
        return JsonResponse({"error": "Not allowed to update this user"}, status=403)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = UserUpdateSerializer(
        user,
        data=data,
        partial=True
    )

    if serializer.is_valid():
        user = serializer.save()

        # handle password separately (if provided)
        password = data.get("password")
        if password:
            user.set_password(password)
            user.save()

        return JsonResponse({"data": _serialize_user(user)})

    return JsonResponse({"errors": serializer.errors}, status=400)



@csrf_exempt
def user_delete(request, pk):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE allowed"}, status=405)

    authenticated_user = get_authenticated_user(request)
    if not authenticated_user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    if authenticated_user.pk != pk:
        return JsonResponse(
            {"error": "Not allowed to delete this user"},
            status=403
        )

    user = User.objects.filter(pk=pk).first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()

    return JsonResponse({"data": "Deleted successfully"})