from django.shortcuts import render
from mainapp.context_processors import get_links_menu


def main(request):
    title = 'главная'
    heading = 'новинки сцены'
    links_menu = get_links_menu(request, title=title, heading=heading)
    return render(request, 'index.html', context=links_menu)


def contact(request):
    title = 'контакты'
    links_menu = get_links_menu(request, title=title)
    return render(request, 'contact.html', context=links_menu)
