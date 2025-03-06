from django.db.models import F
from django.db.transaction import atomic
from rest_framework import serializers

from orders.models import Item, ItemQuantity, Order


class ItemsField(serializers.Field):
    """Кастомный field для позиций."""

    default_error_messages = {
        "empty_list": "Не выбрано ни одной позиции.",
        "incorrect_type": (
            "Неверный тип позиции, ожидается: dict, получен: {item_type}."
        ),
        "incorrect_keys": (
            "Неверные ключи словаря, ожидаются: {id, quantity}, получены:"
            " {item_keys}."
        ),
        "item_not_exist": "Позиция с id {item_id} не существует.",
        "quantity_less_than_1": (
            "Количество позиции {item_id} не может быть меньше 1."
        ),
        "item_repeat": "Позиция {item_id} передан больше 1 раза.",
    }

    def to_representation(self, items):
        return items.values().annotate(amount=F("itemquantity__quantity"))

    def to_internal_value(self, items):
        if not items:
            self.fail("empty_list")

        used_items = set()
        for item in items:
            if not isinstance(item, dict):
                self.fail("incorrect_type", item_type=type(item))

            if set(item.keys()) != {"id", "quantity"}:
                self.fail("incorrect_keys", item_keys=item.keys())

            item_id = item["id"]

            if not Item.objects.filter(id=item).exists():
                self.fail("item_not_exist", item_id=item_id)

            if int(item["quantity"]) < 1:
                self.fail("quantity_less_than_1", item_id=item_id)

            if item_id in used_items:
                self.fail("item_repeat", item_id=item_id)

            used_items.add(item_id)

        return items


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "price", "amount"]


class ShortOrderSerializer(serializers.ModelSerializer):
    """Serializer для краткого описания заказа."""

    # image = CustomBase64ImageField()

    class Meta:
        model = Order
        fields = ["id", "table_number", "total_price", "status"]
        read_only_fields = ["__all__"]


class ReadOrderSerializer(ShortOrderSerializer):
    """Serializer для полного описания заказа."""

    items = ItemsField()

    class Meta:
        model = Order
        exclude = ["created_at"]


class WriteOrderSerializer(ReadOrderSerializer):
    """Serializer для записи заказов."""

    @staticmethod
    def itemquantity_bulk_create(order, items):
        """Bulk creation для позиций."""

        ItemQuantity.objects.bulk_create(
            [
                ItemQuantity(
                    order=order,
                    item_id=item["id"],
                    quantity=item["amount"],
                )
                for item in items
            ]
        )

    @atomic
    def create(self, validated_data):
        request = self.context.get("request")
        items = validated_data.pop("items")
        order = Order(**validated_data)
        order.save()
        self.itemquantity_bulk_create(order, items)
        return order
