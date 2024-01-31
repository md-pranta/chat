from account.models import Account
from django.db import models
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
# Create your models here.
# internal module
from .validators import icon_size, image_extension


def server_icon(instance, filename):
    return f"server/{instance.id}/icon/{filename}"


def server_banner(instance, filename):
    return f"category/{instance.id}/banner/{filename}"


def category_icon(instance, filename):
    return f"category/{instance.id}/icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon, null=True, blank=True)

    # chexking if icon already uploaded then delete the previous one first then upload the new icon.
    def save(self, *args, **kwargs):
        if self.id:
            exist = get_object_or_404(Category, id=self.id)
            if exist.icon != self.icon:
                exist.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    # if category one object is deleted then delte the icon assioted to it working by django signals.

    @receiver(models.signals.pre_delete, sender='server.Category')
    def category_delete(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='server_category')
    description = models.CharField(max_length=250, null=True)
    member = models.ManyToManyField(Account)

    def __str__(self) -> str:
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channel_server')
    banner = models.ImageField(
        upload_to=server_banner, null=True, blank=True, validators=[image_extension])
    icon = models.ImageField(upload_to=server_icon,
                             null=True, blank=True, validators=[icon_size, image_extension])

    # chexking if icon already uploaded then delete the previous one first then upload the new icon.
    def save(self, *args, **kwargs):
        if self.id:
            exist = get_object_or_404(Channel, id=self.id)
            if exist.icon != self.icon:
                exist.icon.delete(save=False)
            if exist.banner != self.banner:
                exist.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    # if category one object is deleted then delte the icon assioted to it working by django signals.

    @receiver(models.signals.pre_delete, sender='server.Channel')
    def channel_delete(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon' or field.name == 'banner':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self) -> str:
        return self.name
