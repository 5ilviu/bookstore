from django.contrib.auth.models import User
# Create your views here.
from rest_framework import viewsets, views, mixins, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from .models import Book, Author, Customer, Order
from .serializers import UserSerializer, BookSerializer, AuthorSerializer, CustomerSerializer, CustomerOrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    order = CustomerOrderSerializer
    permission_classes = [IsAuthenticated]


class CustomerOrderViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    serializer_class = CustomerOrderSerializer
    customer = CustomerSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.kwargs['customer_pk'])

    def create(self, request, *args, **kwargs):
        customer = Customer.objects.get(user_id=2)
        address = request.data['address'] or customer.address or 'idk'
        return super().create(request, *args, **kwargs)


class PlainOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
