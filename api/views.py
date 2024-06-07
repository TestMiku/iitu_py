from rest_framework import generics
from main.models import AvhUser
from .serializers import UserSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = AvhUser.objects.all()
    serializer_class = UserSerializer
