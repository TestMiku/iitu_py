import io
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, HttpResponseServerError

import json

import openpyxl
# Create your views here.
from avh_services import read_json

def main(request):
    
    return render(request, 'json_to_excel/main.html')

def handle_7_11_2(request):
    if request.method == 'POST':
        json_path = r"/mnt/adem-otchet/7_11_2.json"#'/mnt/adem-otchet/7_11_2.json'
        wb = openpyxl.Workbook()
        ws = wb.active
        headers = False
        for row in read_json(json_path, "oprovider", "orderstatus"):
            if not headers:
                ws.append(list(row.keys()))
                headers = True
            ws.append(list(row.values()))
        bytes_io = io.BytesIO()
        wb.save(bytes_io)
        bytes_io.seek(0)
        return FileResponse(bytes_io, filename="data_.xlsx")
    return render(request, 'json_to_excel/7_11_2.html')