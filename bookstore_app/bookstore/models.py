import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_non_admin(value):
    """

    :type value: User
    """
    if value.is_staff:
        raise ValidationError("Customer cannot be staff")


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    birthday = models.DateField("date of birth")

    def __str__(self):
        return "Author {0} ({1})".format(self.name, str(self.id))


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication = models.DateField("date of publication")
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.10))


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, validators=[validate_non_admin], primary_key=True)
    cart = models.ManyToManyField(Book)


class Order(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)



