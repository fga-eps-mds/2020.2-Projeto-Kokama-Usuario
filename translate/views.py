from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from django.http import HttpResponse
# from .forms import KokamaWordForm, TypePronunciationForm, PortugueseWordFormSet, PhrasesFormSet
# from .models import Bird
from .forms import PhraseFormSet, WordPortugueseFormSet, WordKokamaForm, PronunciationChoisesForm

# Create your views here.
@require_http_methods(["GET"])
def get_word_list(request):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = "traducao/lista_de_palavras")

        try:
            response = requests.get(url)
            translations = response.json()
            return render(request, 'word_list.html', {'translations': translations, 'translate_base_url': config('TRANSLATE_MICROSERVICE_URL')})
        except:
            return HttpResponse('<h1>Erro interno do servidor</h1>', status=500)
    else:
        return redirect('/')

@require_http_methods(["GET"])
def delete_translate(request, id):
    if request.user.is_superuser:
        url = '{base_url}/{parameter}/{id}'.format(base_url = config('TRANSLATE_MICROSERVICE_URL'), parameter = "traducao/lista_de_palavras", id = id)
        requests.delete(url)
        return redirect('/traducao/lista_de_palavras')
    else:
        return redirect('/')

@require_http_methods(["GET", "POST"])
def add_translate(request, id):
    if request.user.is_superuser:
        if request.method == "GET":
            phrase_formset = PhraseFormSet(prefix='phrase')
            word_portuguses_formset = WordPortugueseFormSet(prefix='word-portuguese')
            word_kokama_form = WordKokamaForm()
            pronunciation_choises_form = PronunciationChoisesForm()
            # queryset=Bird.objects.none()
            return render(request, 'add_word.html', {
                'phrase_formset': phrase_formset,
                'word_portuguses_formset': word_portuguses_formset,
                'word_kokama_form': word_kokama_form,
                'pronunciation_choises_form': pronunciation_choises_form

            })
        elif request.method == "POST":
            phrase_formset = PhraseFormSet(prefix='phrase')
            word_portuguses_formset = WordPortugueseFormSet(prefix='word-portuguese')
            word_kokama_form = WordKokamaForm()
            pronunciation_choises_form = PronunciationChoisesForm()
            return redirect('/traducao/lista_de_palavras')
    else:
        return redirect('/')