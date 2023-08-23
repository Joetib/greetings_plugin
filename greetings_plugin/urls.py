from django.urls import path
from .views import GreetingsViewSet

app_name = "greetings_plugin"
urlpatterns = [
    path('v1/greet/', GreetingsViewSet.as_view(), name="greet")
]