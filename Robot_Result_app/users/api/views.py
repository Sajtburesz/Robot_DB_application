from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins, viewsets

from users.api.serializers import UserSerializer,UserAvatarSerializer
from users.models import User


class UserViewSet(mixins.UpdateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
    
class AvatarUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        user_object = self.request.user
        return user_object