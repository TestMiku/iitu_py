 
1. В "settings.py" можно изменять  INSTALLED_APPS добавлять свои новые созданные apps после "#np's apps"
2. Другие изменения в "settings.py" нужно согласовать с коммандой
3. У каждого разраба есть своя ветка (np, mp, gp)  в котором есть urls.py. по ссылке "host:post/np/" будут попадаться в вашу ветку. Все ссылки на ваши приложении прописывать там
4. В папках "media/", "templates/", "static/" - хранить все элементы в своих папках внутри этих папок (на пример:
    "media/np/", "templates/np/", "static/np/")




Для того что бы запутить проект следуйте инструкции: 

0. установите питон 3.11
1. установите pip
2. установите virtualenv - "pip install virtualenv" 
3. Создайте виртуальное окружение - "python virtualenv .venv"
4. Запустите виртуальное окружение - ".venv\Scripts\activate"
5. В главной директории (где лежит manage.py) установите все нужные библиотеки - "pip install -r requirements.txt"
6. Запустите проект - "python manage.py runserver"

