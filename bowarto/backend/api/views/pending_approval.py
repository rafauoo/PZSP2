from rest_framework import generics
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from rest_framework.response import Response
from ..models import PendingApproval
from ..permissions import allow_authenticated, allow_admin, allow_user
from ..serializers.pending_approval import PendingApprovalSerializer


@authentication_classes([JWTAuthentication])
class PendingApprovalList(generics.ListCreateAPIView):
    serializer_class = PendingApprovalSerializer
    queryset = PendingApproval.objects.all()

    @allow_admin
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_user
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['user'] = request.user.id

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)


@authentication_classes([JWTAuthentication])
class PendingApprovalDetail(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = PendingApprovalSerializer
    queryset = PendingApproval.objects.all()

    @allow_admin
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin
    def delete(self, request, *args, **kwargs):
        approval_id = self.kwargs.get('id')

        approval = get_object_or_404(PendingApproval, id=approval_id)
        approval.user.school = approval.school
        approval.user.save()

        return super().delete(request, *args, **kwargs)
