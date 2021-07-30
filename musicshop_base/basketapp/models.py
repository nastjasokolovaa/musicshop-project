from django.db import models
from django.utils.functional import cached_property
from mainapp.models import Product
import musicshop


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(
        musicshop.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    add_datetime = models.DateTimeField(
        verbose_name='время добавления',
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'product')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_items(user):
        return user.basket.select_related().order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        super(Basket, self).save(*args, **kwargs)
