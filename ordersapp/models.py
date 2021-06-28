from django.conf import settings
from django.db import models

from basketapp.models import Basket
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RD'
    CANCEL = 'CNC'
    DELIVERED = 'DVD'

    STATUSES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Обработан'),
        (PAID, 'Оплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен'),
        (DELIVERED, 'Выдан'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, verbose_name='создан')
    updated = models.DateField(auto_now=True, verbose_name='обновлен')
    is_active = models.BooleanField(default=True)
    status = models.CharField(choices=STATUSES, default=FORMING, max_length=3, verbose_name='статус')

    class Meta:
        ordering = ('-created',)  # сортировка по умолчанию от более новых к старым заказам
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        "return total quantity for user"
        items = self.orderitems.select_related()
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

    def get_total_cost(self):
        "return total sum for user"
        items = self.orderitems.select_related()
        totalcost = sum(list(map(lambda x: x.get_product_cost(), items)))
        return totalcost

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')
    add_datetime = models.DateField(verbose_name='время добавления', auto_now_add=True)

    def get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

