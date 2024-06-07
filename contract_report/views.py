from contract_report.scripts.debt_on_doc import main_sync
from .models import Adem_19_20, ESF_A77, Merged_model, Supplier
from datetime import datetime
from django.shortcuts import render
import json
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import os
from django.views.decorators.http import require_GET, require_POST
from dateutil import parser


def import_adem_data():
    Adem_19_20.objects.all().delete()
    save_path = 'contract_report/adem'
    for file_name in os.listdir(save_path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            os.remove(os.path.join(save_path, file_name)) 
            
    try:
        file_path = 'contract_report/adem/19_20.json'
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                datascheta_str = item.get('datascheta', '')

                try:
                    datascheta = datetime.fromisoformat(
                        datascheta_str) if datascheta_str else None
                except ValueError:
                    datascheta = None

                docdate_str = item.get('docdate', '')
                docdate = datetime.fromisoformat(
                    docdate_str).date() if docdate_str else None

                # Пропуск создания объекта, если notpayamt1ckzt равен None или 0.00
                notpayamt1ckzt = item.get('notpayamt1ckzt')
                quantity=item.get('quantity')
                
                if notpayamt1ckzt is None or notpayamt1ckzt == 0.0 or notpayamt1ckzt == "0.0" and quantity is None or quantity == '':
                    continue

                Adem_19_20.objects.create(
                    documentno=item.get('documentno', ''),
                    nscheta=item.get('nscheta', ''),
                    datascheta=datascheta,
                    gruppa_proekrov=item.get('gruppa_proekrov', ''),
                    too=item.get('too', ''),
                    postavshik=item.get('postavshik', ''),
                    notpayamt1ckzt=notpayamt1ckzt,
                    bin=item.get('bin', ''),
                    docserviceact=item.get('docserviceact', None),
                    docdate=docdate,
                    quantity=item.get('quantity', None)
                )
        return "Data imported successfully"
    except Exception as e:
        return f"Error importing data: {str(e)}"


def import_esf_a77_data(request):
    ESF_A77.objects.all().delete()
    if request.method == 'POST':
        save_path = 'contract_report/adem'
        excel_file = request.FILES.get('excel_file')
        excel_file_path = save_path + '/' + excel_file.name
        try:
            with open(excel_file_path, 'wb') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
            json_data = excel_to_json(excel_file_path)

            for item in json_data['data']:
                if item.get('Состояние') == 'Принят от поставщика':
                    bin_value = item.get(
                        'БИН / ИИН') if item.get('БИН / ИИН') is not None else None

                    ESF_A77.objects.create(
                        too=item.get('Покупатель', ''),
                        postavshik=item.get('Контрагент', ''),
                        bin=int(item.get('БИН / ИИН', None)
                                ) if item.get('БИН / ИИН') else None,
                        quantity=item.get('Сумма документа', None),
                        dateinvoiced=datetime.strptime(item.get(
                            'Дата оборота', ''), '%d.%m.%Y').date() if item.get('Дата оборота') else None
                    )

            return redirect('merge_models')

        except PermissionError:
            return HttpResponse("Пожалуйста, закройте файл Excel и повторите попытку.")
        except Exception as e:
            return render(request, 'contract_report/contract_report.html', e)
            # return redirect('merge_models')


def excel_to_json(excel_file, json_file=None):
    xls = pd.ExcelFile(excel_file)
    sheet_name = xls.sheet_names[0]

    data = pd.read_excel(excel_file, engine='openpyxl', sheet_name=sheet_name)
    data = data.fillna('')

    # Преобразование всех значений в строки
    # data = data.astype(str)

    if json_file is None:
        json_file = excel_file.split('.')[0] + '.json'

    json_data = data.to_dict(orient='records')
    data_with_count = {"count": len(json_data), "data": json_data}

    return data_with_count


def normalize_spaces(x: str, /) -> str:
    return " ".join(x.split())


def merge_models(request):
    Merged_model.objects.all().delete()
    try:
        adem_objects = Adem_19_20.objects.all()
        esf_objects = ESF_A77.objects.all()
        
        for esf_object in esf_objects:
            adem_objects_filtered = adem_objects.filter(bin=esf_object.bin)
            
            if adem_objects_filtered.exists():  # Если найдены соответствующие объекты
                for adem_object in adem_objects_filtered:
                    Merged_model.objects.create(
                        documentno=adem_object.documentno,
                        nscheta=adem_object.nscheta,
                        datascheta=adem_object.datascheta,
                        too=normalize_spaces(adem_object.too),
                        postavshik=normalize_spaces(adem_object.postavshik),
                        bin=adem_object.bin,
                        notpayamt1ckzt=adem_object.notpayamt1ckzt,
                        gruppa_proekrov=adem_object.gruppa_proekrov,
                        docdate=adem_object.docdate,
                        matched=True
                    )
            else:  # Если не найдены соответствующие объекты
                Merged_model.objects.create(
                    documentno=None,
                    nscheta=None,
                    datascheta=None,
                    too=normalize_spaces(esf_object.too),
                    postavshik=normalize_spaces(esf_object.postavshik),
                    bin=esf_object.bin,
                    notpayamt1ckzt=esf_object.quantity,
                    gruppa_proekrov=None,
                    docdate=esf_object.dateinvoiced,
                    matched=False
                )
                


        # return render(request, 'merge_models_success.html', {'message': "Merge completed successfully"})
        return redirect('process_excel')
    except Exception as e:
        print("Exception", e)
        return redirect('process_excel')

        # return render(request, 'contract_report/contract_report.html', {'error_message': "Error merging data: {str(e)}"})


def show_merged_data(request):
    from django.db.models import Count
    duplicates = Merged_model.objects.values_list('date', 'documentno', 'nscheta', 'datascheta', 'too', 'postavshik', 'bin', 'notpayamt1ckzt', 'gruppa_proekrov', 'docdate').annotate(count=Count('id')).filter(count__gt=1)
    for duplicate in duplicates:
        objects_to_delete = Merged_model.objects.filter(date=duplicate[0], documentno=duplicate[1], nscheta=duplicate[2], datascheta=duplicate[3], too=duplicate[4], postavshik=duplicate[5], bin=duplicate[6], notpayamt1ckzt=duplicate[7], gruppa_proekrov=duplicate[8], docdate=duplicate[9])[1:]
        for obj in objects_to_delete:
            obj.delete()
    merged_data = Merged_model.objects.all()


    return render(request, 'contract_report/contract_report.html', {'merged_data': merged_data})


def get_supplier_data(*args, **kwargs):
    suppliers = []
    for supplier in Supplier.objects.all():
        supplier_data = {
            'id': supplier.id,
            'name': supplier.name,
            'bin': supplier.bin,
            'limit_days': supplier.limit_days,
            'sum_of_limit': supplier.sum_of_limit,
            'too': supplier.too,
        }
        suppliers.append(supplier_data)

    return suppliers


def create_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        bin = request.POST.get('bin')
        limit_days = request.POST.get('limit_days')
        sum_of_limit = request.POST.get('sum_of_limit')
        too = request.POST.get('too').strip()

        new_supplier = Supplier.objects.create(
            name=name, bin=bin, limit_days=limit_days, sum_of_limit=sum_of_limit, too=too)

        supplier_data = {
            'id': new_supplier.id,
            'name': normalize_spaces(new_supplier.name),
            'bin': new_supplier.bin,
            'limit_days': new_supplier.limit_days,
            'sum_of_limit': new_supplier.sum_of_limit,
            'too': normalize_spaces(new_supplier.too),
        }

        return JsonResponse({'success': True, 'supplier': supplier_data})

    return JsonResponse({'error': 'Invalid request method'})


def delete_supplier(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        return JsonResponse({'success': True})
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def suppliers(request):
    supplier_data = get_supplier_data()
    return render(request, 'contract_report/suppliers.html', {'suppliers': supplier_data})


def convert_to_date(value):
    if value is None:
        return None
    try:
        date_object = parser.parse(value)
        formatted_date = date_object.strftime("%d.%m.%Y")
        return formatted_date
    except (ValueError, OverflowError):
        if "." in value:
            # Если есть точка, обрезаем после неё
            value = value.split(".")[0]
        return value


def calculate_days_difference(start_date, end_date):
    if start_date is None or end_date is None:
        return None
    try:
        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
        end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")

        days_difference = (start_date - end_date).days

        return days_difference
    except ValueError:
        return None


def import_supplier_data(request):

    if request.method == 'POST':
        save_path = 'contract_report/adem'
        for file_name in os.listdir(save_path):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                os.remove(os.path.join(save_path, file_name))
        excel_file = request.FILES.get('excel_file')
        excel_file_path = save_path + '/' + excel_file.name
        try:
            with open(excel_file_path, 'wb') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
            json_data = excel_to_json(excel_file_path)

            for item in json_data['data']:
                Supplier.objects.create(
                    name=item.get('Поставщик', ''),
                    bin=item.get('ИИН', ''),
                    limit_days=int(item.get('Лимит дней', None)),
                    sum_of_limit=int(item.get('Сумма лимита', None)),
                    too=item.get('ТОО', None),
                )

            # os.remove(excel_file_path)

            return redirect('suppliers')
        except PermissionError:
            return HttpResponse("Пожалуйста, закройте файл Excel и повторите попытку.")
        except Exception as e:
            return render(request, 'supplier_report/supplier_report.html', {'error': e})


def show_debtdoc(request):
    return render(request, 'contract_report/debts_on_documents.html')

@require_POST
def main_sync_caller(request):
    print("CALLED")
    main_sync()
    return JsonResponse({
        "detail": "OK"
    })
