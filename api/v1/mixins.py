from rest_framework import status
from rest_framework.response import Response


class WriteMethodsMixinView:
    """Mixin с методами add и remove для объектов в ViewSets."""

    @staticmethod
    def add_obj(serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def remove_obj(field, obj_id, obj_name="Объект"):
        if not field.filter(id=obj_id).exists():
            return Response(
                {"errors": f"{obj_name} с таким ID не найден!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        field.remove(obj_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
