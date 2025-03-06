from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core import constants


class Item(models.Model):
    name = models.CharField(
        max_length=constants.MAX_ITEM_NAME_LEN,
        unique=True,
        verbose_name="Название",
    )
    description = models.CharField(
        max_length=constants.MAX_ITEM_DESC_LEN,
    )
    price = models.PositiveIntegerField(
        "Цена",
        validators=[
            MinValueValidator(constants.MIN_ITEM_PRICE),
        ],
    )
    amount = models.PositiveIntegerField(
        "Доступное количество",
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [(status.value, status.name) for status in constants.Status]

    status = models.CharField(
        choices=STATUS_CHOICES,
        default=constants.Status.PAID.value,
        verbose_name="Статус заказа",
    )

    table_number = models.PositiveIntegerField(
        "Номер стола",
        validators=[
            MinValueValidator(constants.MIN_TABLE_NUMBER),
            MaxValueValidator(constants.MAX_TABLE_NUMBER),
        ],
    )

    items = models.ManyToManyField(
        Item,
        related_name="orders",
        verbose_name="Позиции",
        through="ItemQuantity",
    )

    total_price = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        """Высчитывает и сохраняет сумму всего заказа."""

        self.total_price = sum(
            item_quantity.item.price * item_quantity.quantity
            for item_quantity in self.itemquantity_set.all()
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.total_price:.2f}"


class ItemQuantity(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        "Количество",
        default=constants.ITEM_AMOUNT_MIN,
        validators=[
            MinValueValidator(
                constants.ITEM_AMOUNT_MIN, constants.ITEM_AMOUNT_MIN_ERR_MSG
            ),
        ],
    )

    def clean(self):
        """
        Выполняет стандартную валидацию модели, затем валидирует максимальное количество позиций в заказе.
        """

        super().clean()

        if self.item.amount and self.quantity > self.item.amount:
            raise ValidationError(
                constants.ITEM_AMOUNT_MAX_ERR_MSG.format(self.quantity, self.item.name)
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
