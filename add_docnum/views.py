from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseNotFound, HttpResponseServerError
from .services import add_docnumber


def handle_uploaded_file(request):
    if request.method == 'POST':
        #print(request.FILES)
        if request.FILES.get('file_19_20_upload'):
            print("IN SECOND file_19_20_upload")
            file_19_20 = request.FILES['file_19_20_upload']
            response = add_docnumber.update_19_20(file_19_20)
            return response

        if 'file_upload' in request.FILES:
            file = request.FILES['file_upload']
            response = add_docnumber.add_document_number(file)
            if isinstance(response, FileResponse):
                return response
            else:
                return response
    else:
        return HttpResponse("Неверный запрос: файл не загружен.", status=400)
    return HttpResponse(content_type='ERROR!')

def main(request):
    # Тут остальной код без изменений
    return render(request, 'add_docnumber/index.html')



