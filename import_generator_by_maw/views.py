from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib import messages

from reporter.models import Report
from .models import GoogleSheetData
from .serializers import AllGoogleSheetDataSerializer, AccountNumberSerializer
from django.db import connection
import re
import gspread
from openpyxl import load_workbook


# Create your views here.

def get_data_from_google_sheet(request) -> render:
    if request.method == 'POST':
        Report.objects.create(responsible=request.user, process="generator_maw - Данные обновлены",
                              text="generator_maw.reload_data")
        GoogleSheetData.objects.all().delete()

        gc = gspread.service_account(filename="import_generator_by_maw/credentials.json")
        sh = gc.open("МАШ Сверка(продажа)")
        code_worksheet = sh.get_worksheet_by_id(1773088625)
        ex_dict: dict[str, str] = {}
        for row in code_worksheet.get_all_values()[1:]:
            ex_dict[row[0]] = row[1]

        worksheet = sh.get_worksheet_by_id(986908701)
        headers: list[str] = [row.replace(' ', '') for row in worksheet.row_values(2)]
        print(headers)
        all_values = worksheet.get_all_values()
        target_headers = ['Номенклатура', '№счета', 'Кол-во', 'Ед.изм', 'Цена,тг',
                          'Номерзаказа']  # Будет Налог утончить
        target_column_index = [headers.index(header) + 1 for header in target_headers]


        for row in all_values[2:]:
            values = [row[index - 1] for index in target_column_index]
            if (not values[1] or values[1] == 'не будет счета'):
                continue

            account_number_match = re.search(r'\d+', values[1])
            account_number_splited = account_number_match[0] if account_number_match else ''
            table_type= 'secondary' if values[0] not in ex_dict else 'main'
            GoogleSheetData.objects.create(
                nomenclature=values[0],
                account_number=values[1],
                account_number_splited=account_number_splited,
                quantity=values[2] if values[2] else None,
                unit_measurement=values[3],
                price=values[4],
                nomenclature_code=ex_dict[values[0]] if values[0] in ex_dict else '',
                order_number=values[5],
                tax=None,
                table_type= table_type,
            )
        messages.success(request, 'Успешно обновлено')
    Report.objects.create(responsible=request.user, process="generator_maw - Открыт главная страница",
                          text="generator_maw.open")
    return redirect('import_maw')



@api_view(['GET'])
def search_by_account_number(request: Request) -> Response:
    acc_num = request.GET.get('account_number')
    filters: dict[str, str] = {}
    if acc_num:
        filters["account_number__iregex"] = rf'^{acc_num}\s+'
        data = GoogleSheetData.objects.filter(**filters).values('account_number').distinct()
        return Response(AccountNumberSerializer(data, many=True).data)
    return Response({})


@api_view(['GET'])
def get_all_values_by_account_number(request: Request) -> Response:
    acc_num = request.GET.get('account_number')
    filters: dict[str, str] = {}
    if acc_num:
        filters["account_number__iregex"] = acc_num
        data = GoogleSheetData.objects.filter(**filters)
        return Response(AllGoogleSheetDataSerializer(data, many=True).data)
    return Response({})


def main(request) -> render:
    Report.objects.create(responsible=request.user, process="generator_maw - Открыт главная страница",
                          text="generator_maw.open")
    return render(request, 'import_generator_by_maw/main.html')