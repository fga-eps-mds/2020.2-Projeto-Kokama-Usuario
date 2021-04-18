from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from .forms import WordKokamaForm, WordPortugueseFormSet, PronunciationChoisesForm, PhraseFormSet
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.paginator import Paginator

word_per_page = 25


# Create your views here.
@require_http_methods(["GET"])
def get_word_list(request):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = "traducao/lista_de_palavras")
        try:
            search_query = request.GET.get('search', '').lower()
            response = requests.get(url)
            translations = response.json()
            search_list = []
            if search_query != '':
                for translate in translations:
                    # Transformar em função e tratar palavras parecidas
                    if search_query.lower() in translate['word_kokama'].lower():
                        search_list.append(translate)
                    else:
                        for word in translate['translations']:
                            if search_query.lower() in word.lower():
                                search_list.append(translate)
                                break
                            
                translations = search_list.copy()

            p = Paginator(translations, word_per_page, allow_empty_first_page=True)
            try:
                page_num = request.GET.get('page')
                page = p.get_page(page_num)
            except:
                page = p.page(1)
            return render(request, 'word_list.html', {
                'page': page, 
                'num_pages': p.num_pages, 
                'search_query': search_query, 
            })
        except:
            return HttpResponse(
                'Erro interno do servidor',
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')

@require_http_methods(["GET"])
def delete_translate(request, id):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}/{id}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = "traducao/lista_de_palavras", id = id)
        try:
            requests.delete(url)
            return redirect('/traducao/lista_de_palavras')
        except:
            return HttpResponse(
                'Erro interno do servidor',
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')

@require_http_methods(["GET", "POST"])
def add_translate(request, id):
    if request.user.is_superuser:
        try:
            if request.method == "GET":
                if id:
                    url = '{base_url}/{parameter}/{id}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = 'traducao/dicionario', id=id)
                    data = requests.get(url).json()
                    pronunciation_type = 0
                    if data['pronunciation_type'] == 'feminino':
                        pronunciation_type = 2
                    elif data['pronunciation_type'] == 'masculino':
                        pronunciation_type = 3
                    else:
                        pronunciation_type = 1

                    word_portuguese_data = {
                        'word-portuguese-TOTAL_FORMS': len(data['translations']),
                        'word-portuguese-INITIAL_FORMS': '0',
                        'word-portuguese-MIN_NUM_FORMS': '0',
                        'word-portuguese-MAX_NUM_FORMS': '1000',
                    }
                    for index, word in enumerate(data['translations']):
                        word_portuguese_data['word-portuguese-{}-word_portuguese'.format(index)] = word

                    phrase_data = {
                        'phrase-TOTAL_FORMS': len(data['phrases']),
                        'phrase-INITIAL_FORMS': '0',
                        'phrase-MIN_NUM_FORMS': '0',
                        'phrase-MAX_NUM_FORMS': '1000',
                    }
                    for index, phrase in enumerate(data['phrases']):
                        phrase_data['phrase-{}-phrase_portuguese'.format(index)] = phrase['phrase_portuguese']
                        phrase_data['phrase-{}-phrase_kokama'.format(index)] = phrase['phrase_kokama']

                    phrase_formset = PhraseFormSet(prefix='phrase', data=phrase_data)
                    word_portuguses_formset = WordPortugueseFormSet(prefix='word-portuguese', data=word_portuguese_data)
                    word_kokama_form = WordKokamaForm(data=data)
                    pronunciation_choises_form = PronunciationChoisesForm(data={'pronunciation_choises':pronunciation_type})
                else:
                    phrase_formset = PhraseFormSet(prefix='phrase')
                    word_portuguses_formset = WordPortugueseFormSet(prefix='word-portuguese')
                    word_kokama_form = WordKokamaForm()
                    pronunciation_choises_form = PronunciationChoisesForm()
                return render(request, 'add_word.html', {
                    'phrase_formset': phrase_formset,
                    'word_portuguses_formset': word_portuguses_formset,
                    'word_kokama_form': word_kokama_form,
                    'pronunciation_choises_form': pronunciation_choises_form

                })
            elif request.method == "POST":
                phrase_formset = PhraseFormSet(prefix='phrase', data=request.POST)
                word_portugueses_formset = WordPortugueseFormSet(prefix='word-portuguese', data=request.POST)
                word_kokama_form = WordKokamaForm(data=request.POST)
                pronunciation_choises_form = PronunciationChoisesForm(data=request.POST)
                all_forms_are_valid = phrase_formset.is_valid() and word_portugueses_formset.is_valid() and word_kokama_form.is_valid() and pronunciation_choises_form.is_valid()
                if (all_forms_are_valid):
                    url = '{base_url}/{parameter}/{id}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = "traducao/adicionar_traducao", id = id)
                    requests.post(url, data=request.POST)
                    return redirect('/traducao/lista_de_palavras')
                else:
                    return render(request, 'add_word.html', {
                        'phrase_formset': phrase_formset,
                        'word_portugueses_formset': word_portugueses_formset,
                        'word_kokama_form': word_kokama_form,
                        'pronunciation_choises_form': pronunciation_choises_form
                    })
        except:
            return HttpResponse(
                'Erro interno do servidor',
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return redirect('/')