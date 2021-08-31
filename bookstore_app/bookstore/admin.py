from django.contrib import admin

# Register your models here.
from .models import Book, Author, Customer, Order

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(Order)
