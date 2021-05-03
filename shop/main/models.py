from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    name = models.CharField(max_length = 100)
    brand = models.CharField(max_length = 100)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    imageName = models.CharField(max_length = 32, default = "missing.jpg")
    productType = models.CharField(max_length = 16)
    details = models.TextField()

    def __str__(self):
        return self.name

    @property
    def stock(self):
        total = 0

        for order in ImportOrderIndividual.objects.filter(product = self):
            total += order.quantity

        for order in CartOrderIndividual.objects.filter(product = self):
            total -= order.quantity

        return total

    @property
    def totalValue(self):
        return self.stock * float(self.unitPrice)


class Customer(models.Model):

    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    address = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.username


class CustomerCartOrder(models.Model):

    orderDate = models.DateTimeField(auto_now = False, null = True)
    shippedDate = models.DateTimeField(auto_now = False, null = True)
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return str(self.id)


class ImportOrder(models.Model):

    vendor = models.CharField(max_length = 50)
    vendorPrice = models.DecimalField(max_digits=10, decimal_places=2)
    arrivedDate = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.id

class CartOrderIndividual(models.Model):

    cartOrder = models.ForeignKey(CustomerCartOrder, null = False, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = False, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.cartOrder) + str(self.product)

class ImportOrderIndividual(models.Model):

    importOrder = models.ForeignKey(ImportOrder, null = False, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = False, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.importOrder) + str(self.product)


def get_sentinel_user():
    return Customer.objects.get_or_create(username = 'deleted')[0]

class Review(models.Model):
    
    customer = models.ForeignKey(Customer, null = False, on_delete = models.SET(get_sentinel_user))
    product = models.ForeignKey(Product, null = False, on_delete = models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content