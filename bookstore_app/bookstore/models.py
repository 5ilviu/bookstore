import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100, null=True)
    cart = models.ManyToManyField(Book, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    books = models.ManyToManyField(Book)
    address = models.CharField(max_length=100)

    def _get_computed_price(self):
        return sum(map(lambda x: x.price, self.books))

    def get_queryset(self):
        qs = super(Order, self).get_queryset().annotate(
            link=self._get_computed_price)
        return qs





