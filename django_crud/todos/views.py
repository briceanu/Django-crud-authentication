from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django_crud.authentication import get_authenticated_user
from django_crud.todos.models import Todo


@csrf_exempt
def filter_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    filter_value = request.GET.get("title", "")

    todos = list(
        Todo.objects.filter(
            user=user,
            title__icontains=filter_value
        ).values()
    )

    return JsonResponse({"data": todos})


@csrf_exempt
def todo_create(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    todo = Todo.objects.create(
        user=user,
        title=data.get("title"),
        description=data.get("description", ""),
        completed=data.get("completed", False),
    )

    return JsonResponse({
        "data": {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
        }
    }, status=201)


@csrf_exempt
def todo_update(request, pk):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT allowed"}, status=405)

    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    todo = Todo.objects.filter(pk=pk).first()
    if not todo:
        return JsonResponse({"error": "Todo not found"}, status=404)

    if todo.user != user:
        return JsonResponse(
            {"error": "Not allowed to modify this todo"},
            status=403
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    todo.completed = data.get("completed", todo.completed)
    todo.save()

    return JsonResponse({"data": "Updated successfully"})


@csrf_exempt
def todo_delete(request, pk):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE allowed"}, status=405)

    user = get_authenticated_user(request)
    if not user:
        return JsonResponse({"error": "Unauthenticated"}, status=401)

    todo = Todo.objects.filter(pk=pk).first()
    if not todo:
        return JsonResponse({"error": "Todo not found"}, status=404)

    if todo.user != user:
        return JsonResponse(
            {"error": "Not allowed to delete this todo"},
            status=403
        )

    todo.delete()

    return JsonResponse({"data": "Deleted successfully"})