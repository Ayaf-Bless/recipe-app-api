from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewsSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializers

    def get_queryset(self):
        """return objects the current authed user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    # def perform_create(self, request, *args, **kwargs):
    #     """create tags"""
    def perform_create(self, serializer):
        """create tags and assign it to a user"""
        serializer.save(user=self.request.user)
