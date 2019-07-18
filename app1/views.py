import random

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from app1.models import App1


def read(request):
    # получаем все закончиенные тексты
    poems = App1.objects.filter(ended=True)
    if poems.count() == 0:
        return render(request, 'noPoemsBanner.html', {})
    poem = random.choice(poems)
    # TODO: сделать красивый шаблон
    return render(request, 'readAPoem.html', {'poem': poem})


def write(request):
    if request.method == 'GET':
        poems = App1.objects.filter(ended=False)
        if poems.count() == 0:
            poem = App1()
            poem.text = ""
            poem.save()
            return render(request, 'writeANewPoem.html', {'poem': poem})
        else:
            poem = random.choice(poems)
            if poem.text=='':
                return render(request, 'writeAPoem.html', {'poem': poem.text,
                                                           'poemId': poem.id, 'poemName': poem.name})
            else:
                return render(request, 'writeAPoem.html', {'poem': poem.text.splitlines()[-1],
                                                       'poemId': poem.id, 'poemName':poem.name})
    if request.method == 'POST':
        if 'button1' in request.POST or 'button2' in request.POST:
            poemId = request.POST['poemId']
            poem = App1.objects.get(pk=poemId)
            poemName = request.POST['poemName']
            if ('button1' in request.POST) and (request.POST['button1'] == 'Добавить'):
                poem.text = poem.text + request.POST['text'] + '\n'
                poem.name = poemName
            if ('button2' in request.POST) and (request.POST['button2'] == 'Закончить'):
                poem.text = poem.text + request.POST['text']
                poem.name = poemName
                poem.ended = True
        else:
            poem = App1()
            poem.text = ""
            poem.save()
            return render(request, 'writeANewPoem.html', {'poem': poem})
        poem.save()
        return redirect('/read')