from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from rest_framework.decorators import api_view
from .forms import StoryForm
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.http import HttpResponse

STORY_LIST_URL = 'historia/lista_de_historias'
SERVER_ERROR = 'Erro interno do servidor'
STORIES_PER_PAGE = 25


# Os viewsset tão cagando a autenticação das adições, exclusões e edições
# A auth antes do view(ou viewset), ou seja, nos outros microsserviços
# View intermediária entre o request daqui e o certo
# Método só pode ser acessado por um IP especifico (?)

def get_search_list(match, query_list):
    search_list = []
    for story in query_list:
        if match.lower() in story['title'].lower():
            search_list.append(story)
        else:
            for word in story['text'].split(",.?!;()"):
                if match.lower() in word.lower():
                    search_list.append(story)
                    break
    return search_list


def login():
    s = requests.Session()
    username = config('LEARN_USERNAME')
    password = config('LEARN_PASSWORD')
    url = '{base_url}/{parameter}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = 'login/')
    try:
        response = s.post(url, data={'username': username, 'password': password})
        if response.status_code == HTTP_400_BAD_REQUEST:
            return False
    except Exception:
        return False

    return s


@require_http_methods(["GET"])
def list_story(request):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = 'historias')
        session = login()
        try:
            if not session:
                return Response(HTTP_500_INTERNAL_SERVER_ERROR)

            response = session.get(url)
            stories = response.json()
            search_query = request.GET.get('search', '').lower()
            if search_query != '':
                search_list = get_search_list(search_query, stories)     
                stories = search_list.copy()

            p = Paginator(stories, STORIES_PER_PAGE, allow_empty_first_page=True)
            try:
                page_num = request.GET.get('page')
                page = p.get_page(page_num)
            except Exception:
                page = p.page(1)
            return render(request, 'list_story.html', {
                'page': page, 
                'num_pages': p.num_pages, 
                'search_query': search_query, 
            })

        except Exception:
            print("Deu exception")
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')

@require_http_methods(["POST", "GET", "DELETE"])
def delete_story(request, id):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}/{id}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL, id = id)
        try:
            session = login()
            print(dir(session))
            if not session:
                return HttpResponse(
                    SERVER_ERROR,
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            requests.delete(url)

            return redirect('/historia/lista_de_historias')
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')

def add_story_get(request, id):
    if id:
        try:
            url = '{base_url}/{parameter}/{id}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = 'historia/lista_de_historias', id=id)
            session = login()
            if not session:
                return HttpResponse(
                    SERVER_ERROR,
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            response = session.get(url)
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        story = response.json()
        story_form = StoryForm(data=story)
    else:
        story_form = StoryForm()
    return render(request, 'add_story.html', { 'story_form': story_form, 'id': id })

def add_story_post(request, id):
    story_form = StoryForm(data=request.POST)
    session = login()
    if not session:
        return HttpResponse(
            SERVER_ERROR,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if (story_form.is_valid()):
        try:
            if id:
                url = '{base_url}/{parameter}/{id}/'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL, id = id)
                requests.put(url, data=request.POST)
            else:
                url = '{base_url}/{parameter}/'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL)
                requests.post(url, data=request.POST)
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return redirect('/historia/lista_de_historias')
    else:
        return render(request, 'add_story.html', { 'story_form': story_form })


@require_http_methods(["GET", "POST"])
def add_story(request, id):
    if request.user.is_superuser:
        if request.method == "GET":
            return add_story_get(request, id)
        elif request.method == "POST":
            return add_story_post(request, id)
    else:
        return redirect('/')
