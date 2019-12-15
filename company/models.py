from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver

from customer.models import (
    User,
    Cart,
    Wishlist,
)

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "subcategories"


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    rate = models.FloatField(default=0)
    description = models.CharField(max_length=1000, blank=True)
    in_stock = models.IntegerField(default=0)
    company = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(
        default="product_images/default.jpg", upload_to='product_images', blank=True, null=True)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


@receiver(pre_save, sender=User)
def pre_save_company_receiver(sender, **kwargs):
    if kwargs.get('instance').is_company == True:
        kwargs.get('instance').username = kwargs.get('instance').email


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.FloatField(default=0)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + '- quantity- ' + str(self.quantity)


class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.wishlist.user.first_name + '-' + self.product.name


class Order(models.Model):
    order = models.OneToOneField(
        CartItem, on_delete=models.CASCADE, primary_key=True, related_name="order")

    def __str__(self):
        return self.order


@receiver(pre_save, sender=Order)
def post_save_order_receiver(sender, **kwargs):
    order = kwargs.get('instance').order
    if order.product.in_stock >= order.quantity:
        order.product.in_stock -= order.quantity
    else:
        order.quantity = order.product.in_stock
        order.product.in_stock = 0
    order.is_ordered = True
    order.product.save()
    order.save()


@receiver(post_save, sender=CartItem)
def post_save_cartitem_receiver(sender, **kwargs):
    if kwargs['created']:
        cost = kwargs.get(
            'instance').quantity * kwargs.get('instance').product.rate
        kwargs.get('instance').cost = cost
        kwargs.get('instance').save()
