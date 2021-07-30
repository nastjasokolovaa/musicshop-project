from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm, ShopUserProfileEditForm
from authapp.models import ShopUser
from mainapp.context_processors import get_links_menu


def login(request):
    title = 'вход'
    links_menu = get_links_menu(request=request, title=title)
    login_form = ShopUserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    links_menu.update(
        {
            'title': title,
            'login_form': login_form,
            'next': next,
        }
    )
    return render(request, 'login.html', context=links_menu)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'
    links_menu = get_links_menu(request=request, title=title)
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            send_verify_link(user)

            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    links_menu.update(
        {
            'title': title,
            'register_form': register_form,
        }
    )

    return render(request, 'register.html', links_menu)


def edit(request):
    title = 'редактирование'
    links_menu = get_links_menu(request=request, title=title)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    links_menu.update(
        {
            'title': title,
            'edit_form': edit_form,
            'profile_form': profile_form
        }
    )

    return render(request, 'edit.html', links_menu)


def send_verify_link(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activetion: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    title = 'Верификация'
    links_menu = get_links_menu(request=request, title=title)
    user = ShopUser.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    links_menu.update(
        {
            'title': title,
        }
    )
    return render(request, 'verify.html', links_menu)
