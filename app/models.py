from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    title = models.CharField(max_length=255, unique=False, null=False, blank=False)
    url = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(null=True, blank=False, default=0)


@receiver(post_save, sender=Product)
def create_url(sender, instance, signal, created, **kwargs):
    product = instance
    if product.url is None:
        product.url = 'product_{0}'.format(product.id)
        product.save()