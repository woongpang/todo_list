from rest_framework.serializers import ModelSerializer
from .models import TodoList
from users.serializers import UserSerializer


class TodoSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = (
            "pk",
            "title",
            "is_complete",
            "created_at",
            "updated_at",
        )


class TodoDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TodoList
        fields = "__all__"


class TodoDetailListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        exclude = ("user",)