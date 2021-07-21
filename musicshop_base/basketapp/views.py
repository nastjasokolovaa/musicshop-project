from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from basketapp.models import Basket
from mainapp.context_processors import get_links_menu
from mainapp.models import Product


@login_required()
def basket(request):
    title = 'корзина'
    if request.user.is_authenticated:
        context = get_links_menu(request=request, title=title)
        return render(request, 'basket.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def basket_remove_all(request):
    basket = Basket.objects.filter(user=request.user)
    for item in basket:
        item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def basket_edit(request, pk, quantity):
    basket = Basket.objects.filter(user=request.user, pk=pk).first()
    basket_record = get_object_or_404(Basket, pk=pk)
    if not basket:
        return HttpResponseNotFound()
    basket.quantity = quantity
    basket.save()
    if quantity == 0:
        basket_remove(request, pk=pk)

    basket = Basket.objects.filter(user=request.user)
    tpl = render_to_string('includes/inc_basket_list.html', {
        'basket': basket,
    })
    return JsonResponse({
        'basket_list': tpl,
        'total_cost': f'{sum(list(map(lambda x: x.product_cost, basket)))} руб',
        'total_quantity': f'({sum(list(map(lambda x: x.quantity, basket)))} шт.)',
    })
