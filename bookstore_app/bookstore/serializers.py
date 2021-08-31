from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import Book, Author, Customer, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        exclude = []


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birthday', 'books']


class CustomerOrderSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'address', 'customer', 'books', 'full_price']
    url = NestedHyperlinkedIdentityField(
        read_only=True,
        view_name='customer-order-detail',
        parent_lookup_kwargs={'customer_pk': 'customer__pk'}
    )
    full_price = serializers.SerializerMethodField('_get_computed_price')

    def _get_computed_price(self, order):
        return sum(map(lambda x: x.price, order.books.all()))


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    orders = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='customer-order-detail',
        parent_lookup_kwargs={'customer_pk': 'customer__pk'})

    class Meta:
        model = Customer
        fields = '__all__'
