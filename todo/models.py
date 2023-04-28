from django.db import models


class TodoList(models.Model):
    title = models.CharField(
        max_length=150,
    )
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(
        null=True,
        blank=True,
    )
    completion_at = models.DateField(
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="todolists",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Todolists"