# store/models.py

from django.db import models
from django.urls import reverse
from ElectronicShop import settings
from django.utils import timezone

# Modèle pour représenter une catégorie de produits
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

# Modèle pour représenter un produit
class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)  # comme un ID unique
    price = models.FloatField(default=0.0)
    old_price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    details = models.TextField(blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    thumbnail_detail = models.ImageField(upload_to="products", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

# Modèle pour représenter une commande (article)
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

# Modèle pour représenter un panier
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        cart_orders = self.orders.filter(ordered=False)  # Filter only the cart orders
        for order in cart_orders:
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        super().delete(*args, **kwargs)  # Delete the cart instance
        
        
# Modèle pour représenter une liste de souhaits
class Souhait(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)