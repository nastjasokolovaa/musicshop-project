from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.name} {self.id} - {self.created_at}'

    is_active = models.BooleanField(
        verbose_name='активна/не активна',
        default=True
    )


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='название продукта',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='product_img',
        blank=True,
    )
    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=256,
        blank=True,
    )
    description = models.TextField(
        verbose_name='описание продукта',
        blank=True,
        max_length=500,
    )
    price = models.DecimalField(
        verbose_name='цена продукта',
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    old_price = models.DecimalField(
        verbose_name='старая цена продукта',
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество на складе',
        default=0
    )
    new_product = models.BooleanField(
        verbose_name='новинка/не новинка',
        default=False,
    )
    hot_product = models.BooleanField(
        verbose_name='со скидкой/без скидки',
        default=False,
    )

    raiting = models.PositiveSmallIntegerField(
        verbose_name='рейтинг',
        default=0,
    )

    def __str__(self):
        return f'{self.name} {self.category}'

    is_active = models.BooleanField(
        verbose_name='активна',
        default=True
    )
    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
