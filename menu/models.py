from django.db import models
from account.models import User

class Foods(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to='foods/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name="Блюдо")
    fullname = models.CharField(max_length=50, verbose_name="ФИО")
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        permissions = [
            ("can_deactivate_order", "Может деактивировать заказ"),
            ("can_view_all_orders", "Может просматривать все заказы"),
        ]

    def __str__(self):
        return f"Заказ #{self.id} - {self.food.name}"