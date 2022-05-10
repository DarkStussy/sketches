from django.contrib.auth.models import User
from django.db import models


class ExampleImage(models.Model):
    image = models.ImageField(upload_to='example_images/')

    class Meta:
        verbose_name = 'Пример эскиза'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return f'Пример {self.id}'


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='services/images/')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    admin_answer = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ от {self.user.username}"


class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'orders/images/')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения заказов'

    def __str__(self):
        return f"Изображение {self.order.user}"
