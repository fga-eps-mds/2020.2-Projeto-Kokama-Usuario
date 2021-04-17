from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from rest_framework.decorators import api_view
from .forms import StoryForm
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
)
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.http import HttpResponse


stories_per_page = 25



@require_http_methods(["GET"])
def list_story(request):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = "historia/lista_de_historias")
        try:
            search_query = request.GET.get('search', '').lower()
            response = requests.get(url)
            stories = response.json()
            search_list = []
            if search_query != '':
                for story in stories:
                    if search_query.lower() in story['title'].lower():
                        search_list.append(story)
                    else:
                        for word in story['text'].split(",.?!;()"):
                            if search_query.lower() in word.lower():
                                search_list.append(story)
                                break
                            
                stories = search_list.copy()

            p = Paginator(stories, stories_per_page, allow_empty_first_page=True)
            try:
                page_num = request.GET.get('page')
                page = p.get_page(page_num)
            except:
                page = p.page(1)
            return render(request, 'list_story.html', {
                'page': page, 
                'num_pages': p.num_pages, 
                'search_query': search_query, 
                'learn_base_url': config('LEARN_MICROSERVICE_URL')})
        except:
            return Response(
                {'error': 'Erro interno do servidor'},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')


@require_http_methods(["GET"])
def delete_story(request, id):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}/{id}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = "lista_de_historias", id = id)
        try:
            requests.delete(url)
            return redirect('/historia/lista_de_historias')
        except:
            return Response(
                {'error': 'Erro interno do servidor'},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')


@require_http_methods(["GET", "POST"])
def add_story(request, id):
    if request.user.is_superuser:
        if request.method == "GET":
            if id:
                url = '{base_url}/{parameter}/{id}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = 'historia/lista_de_historias', id=id)
                response = requests.get(url)
                story = response.json()
                story_form = StoryForm(data=story)
            else:
                story_form = StoryForm()
            return render(request, 'add_story.html', { 'story_form': story_form })
        elif request.method == "POST":
            story_form = StoryForm(data=request.POST)
            if (story_form.is_valid()):
                url = '{base_url}/{parameter}/{id}'.format(base_url = config('LEARN_MICROSERVICE_URL'), parameter = "historia/adicionar_historia", id = id)
                requests.post(url, data=request.POST)
                return redirect('/historia/lista_de_historias')
            else:
                return render(request, 'add_story.html', { 'story_form': story_form })

    else:
        return redirect('/')