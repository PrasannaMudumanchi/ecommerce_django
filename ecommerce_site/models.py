from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.
CATEGORY_CHOICES =(
    ('S','Shirt'),
    ('SQ','Sport wear'),
    ('OW','Out wear')
)
LABEL_CHOICES =(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)
class Item(models.Model):
    title= models.CharField(max_length=100)
    price =models.FloatField()
    category =models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label =models.CharField(choices=LABEL_CHOICES,max_length=2)
    discount_price =models.FloatField(null=True,blank=True )
    slug = models.SlugField()
    description = models.TextField()
    def get_absolute_url(self):
        return reverse("ecommerce_site:product", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse("ecommerce_site:add_to_cart", kwargs={
            'slug': self.slug
        })

    def remove_cart_from_url(self):
        return reverse("ecommerce_site:remove_cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.title
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price() 
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date =models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered =models.BooleanField(default=False)
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()       
        return total

    def __str__(self):
        return self.user.first_name
