import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from reporter.models import Report
def index(request):
    Report.objects.create(responsible=request.user, process="google_to_html - Открыта главная страница", text="gthtml.open")
    return render(request, 'googletohtml.html')


@cache_page(60)
@api_view(['GET'])
def googtogtml(request):
    rows = []

    search_key = request.GET.get('search_key', '')
    json_path = os.path.join(os.path.dirname(__file__), "avrora-406106-93f9ab7f68b1.json")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    client = gspread.authorize(creds)

    spreadsheet_id = '1OjAiacrrZy9JlKFi2ir0hzZX7VEwX-EMxS5hIDGea9E'
    sheet = client.open_by_key(spreadsheet_id).worksheet('Telecom')

    data = sheet.get_all_values()
    data = data[3:]
    for row in data:
        if search_key in row[30]:

            rows.append(row)
    Report.objects.create(responsible=request.user, process="google_to_html - Обработано", text="gthtml.handled")
    return Response({'rows': rows}, status=200)


