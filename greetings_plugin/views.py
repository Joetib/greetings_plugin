from django.shortcuts import render
from .models import Greeting
from .seializers import GreetingSerializer
from django.db.models import QuerySet
# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import HttpRequest
from auth_backends.backends import EdXOAuth2
import requests
import logging
logger = logging.getLogger(__name__)
class GreetingsViewSet(ListCreateAPIView,RetrieveAPIView):
    """
    **Use Cases**

        Request Created Greetings as well as create new Greetings

    **Example Requests**

        GET /api/greetings/v1/greet/

    **Response Values**

        Body consists of the following fields:
        
        * next: Paginator url to get next batch of content
        * previous: Paginator url to get previous page
        * count: Number of items
        * num_pages: Total number of paginator pages
        * current_page: Index of the current page
        * start: Paginator start index
        * results: List of Greeting Objects
            Sub-fields include the following
            
            
            * id: The database id of the greeting
            * text: The content of the greeting message
            * user: The user who sent the greeting
            * created_at: The timestamp when the greeting was created
            "last_modified_at: Timestamp for when the greeting was last modified
        
        * reply_for_world (optional): Sent only for post requests with "hello" as  text 
            Sub-Fields include the following
                * detail: Error detail. Send if the user is not authenticated
                * Details of Greeting Object as specified above if the sub-request with "world" as text
                  was successful.


    **Parameters:**

        text:
            The greeting content eg. Hello 
    **Returns**

        * 200 on success with above fields.
        * 400 if an invalid parameter was sent or the text was not provided
          for an authenticated request.
        * 401 if the user is not authenticated

        Example Post response:

            {
                "id": 1,
                "text": "hello",
                "user": 2,
                "created_at": "2023-08-23T16:32:42.440179Z",
                "last_modified_at": "2023-08-23T16:32:42.440267Z"            
            }

        Example Get Response:
            {
                "reply_for_world": {
                    "detail": "Authentication credentials were not provided."
                },
                "id": 3,
                "text": "hello",
                "user": 4,
                "created_at": "2023-08-23T18:35:53.993477Z",
                "last_modified_at": "2023-08-23T18:35:53.993594Z"
            }
    """
    model = Greeting
    queryset = Greeting.objects.all()
    serializer_class = GreetingSerializer
    permission_classes = [IsAuthenticated]
    authentication_backends  = [
        EdXOAuth2
    ]


    def get_queryset(self) ->  QuerySet[Greeting]:
        """Ensure Users can only view their own greetings unless they are superusers."""
        queryset: QuerySet[Greeting] = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)
    
    def create(self, request: HttpRequest, *args, **kwargs):
        """Create a new greeting for a post request."""
        serializer: GreetingSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        greeting_text = serializer.validated_data["text"]
        # log greeting from user.
        logger.info(f"Greeting from {request.user.username}: {greeting_text}")
        self.perform_create(serializer)
        response = {}
        if greeting_text == "hello":
            # initiate a secondary request to this same endpoint with the text="world" using requests
            response_data = requests.post( request.build_absolute_uri(request.get_full_path()), json={"text": "goodbye"})
            response = {"reply_for_world": response_data.json()}
        headers = self.get_success_headers(serializer.data)
        return Response({
                **response,
                **serializer.data,
            }, status=status.HTTP_201_CREATED, headers=headers,
        )
    
    def perform_create(self, serializer: GreetingSerializer) -> None:
        return serializer.save(user=self.request.user)
