from django.conf.urls import url
from .views import list_story, delete_story, add_story

urlpatterns = [
    url(r'^lista_de_historias/$', list_story, name='list_story'),
    url(r'^adicionar_historia/(?P<id>[0-9]*)$', add_story, name="add_story"),
    url(r'^lista_de_historias/(?P<id>[0-9]+)/delete$', delete_story, name="delete_story"),
]