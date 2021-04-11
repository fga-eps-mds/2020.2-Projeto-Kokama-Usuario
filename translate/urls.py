from django.conf.urls import url
from .views import get_word_list, delete_translate

urlpatterns = [
    url(r'^lista_de_palavras/$', get_word_list, name='get_word_list'),
    url(r'^lista_de_palavras/(?P<id>[0-9]+)/delete$', delete_translate, name="wordlist")
]