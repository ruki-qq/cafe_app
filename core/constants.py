from enum import Enum

MIN_TABLE_NUMBER = MIN_ITEM_PRICE = ITEM_AMOUNT_MIN = 1
MAX_TABLE_NUMBER = 50
MAX_ITEM_NAME_LEN = 30
MAX_ITEM_DESC_LEN = 200


ITEM_AMOUNT_MIN_ERR_MSG = (
    f"Количество позиции в заказе не может быть меньше {ITEM_AMOUNT_MIN}."
)
ITEM_AMOUNT_MAX_ERR_MSG = (
    "Количество {0} превышает доступное количество для позиции {1}.)"
)


class Status(Enum):
    PAID = "Оплачено"
    PENDING = "В ожидании"
    READY = "Готово"
