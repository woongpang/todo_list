from django.urls import path
from .views import TodoLists, TodoListDetail

urlpatterns = [
    path("", TodoLists.as_view()),
    path("<int:pk>/", TodoListDetail.as_view()),
]