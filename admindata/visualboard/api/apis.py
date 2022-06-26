from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.http.response import Http404

from visualboard.utils import msg_ok
from visualboard.models import AdminUsers
from visualboard.models import UserInformation
from visualboard.api.serializers import UserInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserInformation.objects.order_by("-id")
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        return msg_ok()
    
    def list(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk)
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)