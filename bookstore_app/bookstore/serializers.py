from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Book, Author


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        exclude = []


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'birthday', 'books']
