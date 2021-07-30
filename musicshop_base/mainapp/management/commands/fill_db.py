import json
import os

from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')
        for product in products:
            category_name = product['category']

            _category = ProductCategory.objects.get(name=category_name)

            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.create_superuser('msuser', 'user@store.local', '1z2x3c', age='18')
        ShopUser.objects.create_user('shoper', 'shoper@v.com', '123zxc', age='25')
