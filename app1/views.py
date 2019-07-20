import random

from django.shortcuts import render, redirect

# Create your views here.
from app1.models import App1
from app1.models import Paragraph


def read(request):
    # получаем все закончиенные тексты
    poems = App1.objects.filter(ended=True)
    if poems.count() == 0:
        return render(request, 'noPoemsBanner.html')
    poem = random.choice(poems)
    paragraphs = list(Paragraph.objects.filter(app1=poem))
    # TODO: сделать красивый шаблон
    return render(request, 'readAPoem.html', {'poem': poem, 'paragraphs': paragraphs, 'poems': poems})


def readOne(request, poemId):
    poem = App1.objects.get(pk=poemId)
    paragraphs = Paragraph.objects.filter(app1=poem)
    return render(request, 'readOnePoem.html', {'poem': poem, 'paragraphs': paragraphs})


def write(request):
    if request.method == 'GET':
        poems = App1.objects.filter(ended=False)
        if poems.count() == 0:
            return render(request, 'writeANewPoem.html')
        else:
            poem = random.choice(poems)
            paragraphs = Paragraph.objects.filter(app1=poem)
            prg = list(paragraphs)[-1]
            return render(request, 'writeAPoem.html', {'poem': poem, 'prg': prg})
    if request.method == 'POST':
        if 'button1' in request.POST or 'button2' in request.POST:
            poemId = request.POST['poemId']
            if (poemId == "-1"):
                poem = App1()
                poem.name = request.POST['poemName']
            else:
                poem = App1.objects.get(pk=poemId)

            if ('button2' in request.POST) and (request.POST['button2'] == 'Закончить'):
                poem.ended = True
            poem.save()
            prg = Paragraph()
            prg.app1 = poem
            prg.text = request.POST['text']
            prg.author = request.POST.get('author')
            prg.save()
        if 'button4' in request.POST:
            return redirect('/write')
        if 'button3' in request.POST:
            return render(request, 'writeANewPoem.html')
        return redirect('/read')
