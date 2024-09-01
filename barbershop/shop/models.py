from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import Sum, F
from PIL import Image
import io

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output_size = (300, 300)  # You can adjust this size
            img.thumbnail(output_size)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85)
            output.seek(0)
            self.image = ContentFile(output.read(), name=f"{self.name}.jpg")
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.get_full_name()}"
    
    def update_total(self):
        total = self.orderitem_set.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0
        self.total = total
        self.save()

    def save(self, *args, **kwargs):
        if self.total is None:
            self.total = 0
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total(self):
        return self.product.price * self.quantity