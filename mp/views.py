# Create your views here.

def one_statapp(request, id):
    statapp = StaticApp.objects.get(pk=id)
    return render(request, "mp/one_statapp.html", {"statapp": statapp})

def dounload_statapps(request, id):
    statapp = StaticApp.objects.get(pk=id)
    import requests
    url = "https://portal.avh.kz/api/reports/"
    headers = {'Content-Type': 'application/json'}
    body = {"responsible": f'{request.user}', "process": f"Скачивание - {statapp.name}","text": "Скачивание - {statapp.name}"}
    requests.post(url, headers=headers, json=body)
    return render(request, "mp/one_statapp.html", {"statapp": statapp, "download_link": statapp.file_field.url})
    




from .forms import StaticAppForm


def create_static_app(request):
    if request.method == 'POST':
        form = StaticAppForm(request.POST, request.FILES)
        if form.is_valid():
            static_app = form.save()  # Save the form data to a new StaticApp object
            return redirect(
                f'/mp/create_or_update_chapter/{static_app.id}')  # Redirect to a success page or another URL

    else:
        form = StaticAppForm()

    return render(request, 'mp/static_app_create.html', {'form': form})


from django.shortcuts import render, redirect
from mp.models import StaticApp
from main.models import Chapter, AvhRole
from .forms import ChapterForm


def create_chapter(title=None, link=None):
    # Если title или link не переданы, устанавливаем значения по умолчанию
    if not title:
        title = "Default Title"
    if not link:
        link = "Default Link"

    # Задаем значения по умолчанию для short_description и roles
    default_short_description = "Напишите описание"
    default_roles = [AvhRole.objects.get(id=1), AvhRole.objects.get(id=2)]

    # Создаем новый объект Chapter с переданными или значениями по умолчанию
    chapter = Chapter(
        title=title,
        link=link,
        short_description=default_short_description,
    )
    chapter.save()

    # Добавляем роли к объекту Chapter
    chapter.roles.set(default_roles)

    # Можете выполнить другие действия, например, перенаправить пользователя на страницу с созданным объектом
    return chapter


def create_or_update_chapter(request, statapp_id):
    # Если chapter_id указан, то это обновление, иначе - создание новой записи
    chapters = Chapter.objects.filter(link=f"/mp/statapps/{statapp_id}")
    statapp = StaticApp.objects.get(pk=statapp_id)
    chapter = None
    if chapters:
        chapter = chapters.last()
    else:
        chapter = create_chapter(statapp.name, f"/mp/statapps/{statapp.id}")

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            chapter = form.save()
            return redirect(f"/mp/statapps/{statapp.id}")
    else:
        form = ChapterForm(instance=chapter)

    return render(request, 'mp/chapter_form.html', {'form': form, 'chapter': chapter})


def html_order_generator(request):
    return render(request, "mp/html_order_generator.html")
