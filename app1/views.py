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
        else:
            poem = random.choice(poems)
        return render(request, 'writeAPoem.html', {'poem': poem})
    if request.method == 'POST':
        poemId=request.POST['poemId']
        poem = App1.objects.get(pk=poemId)
        if ('button1' in request.POST) and (request.POST['button1'] == 'Добавить'):
            poem.text = poem.text + request.POST['text'] + '\n'
        if ('button2' in request.POST) and (request.POST['button2'] == 'Закончить'):
            poem.text = poem.text + request.POST['text']
            poem.ended = True
        if('button3' in request.POST) and request.POST['button3'] == 'Новая':
            poem = App1()
            poem.text = ""
            poem.save()
            return render(request, 'writeAPoem.html', {'poem': poem})
        poem.save()
        return redirect('/read')