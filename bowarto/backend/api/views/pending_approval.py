from rest_framework import generics, status
from rest_framework.decorators import authentication_classes, action
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from rest_framework.response import Response
from ..models import PendingApproval, School, User
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
        if PendingApproval.objects.filter(user=request.user).exists():
            return Response({"message": "User already has pending approval"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)


@authentication_classes([JWTAuthentication])
class PendingApprovalDetail(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = PendingApprovalSerializer
    queryset = PendingApproval.objects.all()

    @allow_admin
    @action(detail=True, methods=['post'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
class ApproveApprovalView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = PendingApproval.objects.all()
    serializer_class = PendingApprovalSerializer

    @allow_admin
    def destroy(self, request, *args, **kwargs):
        approval = self.get_object()
        approval.user.school = approval.school
        approval.user.save()
        approval.delete()

        return Response({'detail': 'Approval successfully accepted'},
                        status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
class RejectApprovalView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = PendingApproval.objects.all()
    serializer_class = PendingApprovalSerializer

    @allow_admin
    def destroy(self, request, *args, **kwargs):
        approval = self.get_object()
        if not User.objects.filter(school=approval.school).exists():
            approval.school.delete()
        approval.delete()

        return Response({'detail': 'Approval successfully rejected'},
                        status=status.HTTP_200_OK)
