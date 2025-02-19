from .serializers import CustomerSerializer
from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from customer.models import User

from.permissions import IsOwnerOrReadOnly


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = User.objects.filter(is_customer=True)
    permission_classes = [IsOwnerOrReadOnly]


'''
class CustomerListAPIView(ListAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerSerializer


class CustomerDetailAPIView(RetrieveAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerSerializer


class CustomerCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_customer=True)


class CustomerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    model = User


class CustomerChangePasswordAPIView(UpdateAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerChangePasswordSerializer
    permission_classes = [IsOwnerOrReadOnly]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteAPIView(DestroyAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerSerializer
    permission_classes = [IsOwnerOrReadOnly]
'''
