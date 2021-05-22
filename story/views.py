from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from .forms import StoryForm
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
)
from django.core.paginator import Paginator
from django.http import HttpResponse

STORY_LIST_URL = 'ensino/lista_de_historias'
SERVER_ERROR = 'Erro interno do servidor'
STORIES_PER_PAGE = 25
baseurl = '{base_url}/{parameter}/{id}'

def is_word_in_title(match, title_list):
    for title in title_list:
        if match.lower() in title.lower():
            return True
    return False

def is_word_in_text(match, text):
    for word in text.split(",.?!;() "):
        if match.lower() in word.lower():
            return True
    return False

def get_search_list(match, query_list):
    search_list = []
    for story in query_list:
        if is_word_in_title(match, [story['title_portuguese'], story['title_kokama']]):
            search_list.append(story)
        else:
            if is_word_in_text(match, story['text_portuguese']):
                search_list.append(story)
            elif is_word_in_text(match, story['text_kokama']):
                search_list.append(story)

    return search_list


@require_http_methods(["GET"])
def list_story(request, url=''):
    if request.user.is_superuser:
        try:
            if url == '':
                url = '{base_url}/{parameter}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL)
            response = requests.get(url)
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
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')


@require_http_methods(["GET", "DELETE"])
def delete_story(request, id, url = ''):
    if request.user.is_superuser:
        try:
            if url == '':
                url = baseurl.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL, id = id)
            
            requests.delete(url)
            return redirect('/historia/lista_de_historias')
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')

def add_story_get(request, id, url = ''):
    if id:
        try:
            if url == '':
                url = baseurl.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL, id=id)
            
            response = requests.get(url)
            if response.status_code != HTTP_200_OK:
                return HttpResponse(
                    SERVER_ERROR,
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            else:
                story = response.json()
                print(request)
                story_form = StoryForm(data=story)
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        story_form = StoryForm()
    return render(request, 'add_story.html', { 'story_form': story_form, 'id': id })


def add_story_post(request, id, url):
    story_form = StoryForm(data=request.POST)
    if (story_form.is_valid()):
        try:
            if id:
                if url == '':
                    url = baseurl.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL, id=id)
                response = requests.put(url, data=request.POST)
                if response.status_code != HTTP_200_OK:
                    return HttpResponse(
                        SERVER_ERROR,
                        status=HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                url = '{base_url}/{parameter}/'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = STORY_LIST_URL)
                response = requests.post(url, data=request.POST)
                if response.status_code != HTTP_200_OK:
                    return HttpResponse(
                        SERVER_ERROR,
                        status=HTTP_500_INTERNAL_SERVER_ERROR,
                    )
        except Exception:
            return HttpResponse(
                SERVER_ERROR,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return redirect('/historia/lista_de_historias')
    else:
        return render(request, 'add_story.html', { 'story_form': story_form })


@require_http_methods(["GET", "POST"])
def add_story(request, id, url):
    if request.user.is_superuser:
        if request.method == "GET":
            return add_story_get(request, id)
        elif request.method == "POST":
            return add_story_post(request, id, url)
    else:
        return redirect('/')
