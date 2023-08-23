from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class Greeting(models.Model):
    """
    Model Reference for storing greetings in the database
    """
    user = models.ForeignKey(User, related_name="greetings", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


    def __str__(self) -> str:
        return self.text