from django.contrib.auth.models import User
from django.db import models
from main.models import ExampleImage
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('last_name').null = False
User._meta.get_field('last_name').blank = False


class FavoritePhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ManyToManyField(ExampleImage, blank=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные пользователей'

    def __str__(self):
        return f'Избранное фото {self.user.username}'
