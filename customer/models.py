from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    profile_images = models.ImageField(
        default="profile_images/default.jpg", upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        if self.is_company:
            return self.first_name
        elif self.is_customer:
            return self.first_name + " " + self.last_name
        else:
            return self.username


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="cart")

    def __str__(self):
        return self.user.first_name + "'s cart"


class Wishlist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="wishlist")

    def __str__(self):
        return self.user.first_name + "'s wishlist"


class SavedForLater(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="savedforlater")

    def __str__(self):
        return self.user.first_name + "'s saved for later"


@receiver(post_save, sender=User)
def create_components(sender, **kwargs):
    if kwargs['created'] and kwargs.get('instance').is_customer == True:
        cart = Cart.objects.create(user=kwargs.get('instance'))
        wishlist = Wishlist.objects.create(user=kwargs.get('instance'))
        savedforlater = SavedForLater.objects.create(
            user=kwargs.get('instance'))

        kwargs.get('instance').username = kwargs.get('instance').email
        print("DONE")


@receiver(pre_save, sender=User)
def pre_save_customer_receiver(sender, **kwargs):
    if kwargs.get('instance').is_customer == True:
        kwargs.get('instance').username = kwargs.get('instance').email