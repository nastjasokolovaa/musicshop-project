from django.shortcuts import get_object_or_404

from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def basket(request):
    basket_list = []
    if request.user.is_authenticated:
        basket_list = Basket.objects.filter(user=request.user)
    return {
        'basket': basket_list
    }


def get_links():
    links_ = [{'href': 'index', 'name': 'главная'},
              {'href': 'mainapp:products', 'name': 'продукты'},
              {'href': 'contact', 'name': 'контакты'}]
    return links_


def get_auth(request):
    name = ShopUser.objects.filter(username=request.user.username).first()
    auth_ = [{'href': 'auth:edit', 'name': name}]
    return auth_


def get_links_menu(request, title, heading=None):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    popular_products = Product.objects.all().order_by('raiting').reverse()[:4]
    new_products = Product.objects.filter(new_product=True)[:3]

    links_menu = {
        'links': list(get_links()),
        'auth': list(get_auth(request)),
        'topic': 'тренды',
        'heading': heading,
        'title': title,
        'products': products,
        'categories': categories,
        'popular_products': popular_products,
        'new_products': new_products,
    }
    return links_menu
