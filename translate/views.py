from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from decouple import config
import requests
from django.http import HttpResponse

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