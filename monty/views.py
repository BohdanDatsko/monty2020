from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from monty.models import User
from monty.serializers import UserSerializer
from monty.permissions import IsLoggedInUserOrAdmin, IsUserAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permissions_classes = []

        if self.action == 'create':
            permissions_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permissions_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permissions_classes = [IsUserAdmin]
        return [permission() for permission in permissions_classes]
