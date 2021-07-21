from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductsEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory
from django.views.generic.list import ListView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'users/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'users/user_create_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/создание пользователя'
        return context


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'users/user_create_update.html'
    success_url = reverse_lazy('adminapp:users')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка/Редактирование пользователя'

        return context


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка/Удаление пользователя'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'categories/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/Категории'
        return context


class ProductCategoryDetailView(DetailView):
    model = ProductCategory
    template_name = 'categories/category.html'
    context_object_name = 'category'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/Категория'
        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'categories/category_create_update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/создание категории'
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'categories/category_create_update.html'
    fields = '__all__'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка/Редактирование категории'

        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка/Удаление категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        if category_id == 0:
            product_list = Product.objects.all()
            category = {'name': 'все', 'pk': '0'}
        else:
            product_list = Product.objects.filter(category_id=category_id)
            category = ProductCategory.objects.filter(id=category_id).first()

        paginator = Paginator(product_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        context['objects'] = product_list
        context['category'] = category
        context['title'] = 'Админка/Продукты'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Админка/Подробнее о продукте'
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_create_update.html'
    form_class = ProductsEditForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = ProductCategory.objects.filter(id=self.kwargs['pk']).first()
        context['title'] = 'админка/создание продукта'
        context['category'] = category
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_create_update.html'
    fields = '__all__'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = ProductCategory.objects.filter(id=self.kwargs['pk']).first()
        context['title'] = 'админка/создание продукта'
        context['category'] = category
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/удаление продукта'
        return context
