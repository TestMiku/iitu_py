import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import generic, View
from nomenclature.models import Nomenclature, NomenclatureOrder
from nomenclature.services import ParseXLSXDataToNomenclatureModel


class ExcelGuideView(generic.ListView):
    template_name = 'nomenclature/excel_guide.html'
    context_object_name = 'excel_guide'
    paginate_by = 50
    parse_service = ParseXLSXDataToNomenclatureModel
    parse_template = 'nomenclature/templates/nomenclature/nomenclatures.xlsx'

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Nomenclature.objects.filter(name__icontains=search).order_by('name')
        return Nomenclature.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nomenclature_list = self.get_queryset()
        paginator = Paginator(nomenclature_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            nomenclatures = paginator.page(page)
        except PageNotAnInteger:
            nomenclatures = paginator.page(1)
        except EmptyPage:
            nomenclatures = paginator.page(paginator.num_pages)

        context['nomenclatures'] = nomenclatures
        context['is_paginated'] = nomenclatures.has_other_pages()
        context['page_obj'] = nomenclatures

        return context

    def get(self, request, *args, **kwargs):
        # NomenclatureOrder.objects.all().delete()
        # Nomenclature.objects.all().delete()
        # self.parse_service(self.parse_template).parse()

        search = request.GET.get('search')
        page = request.GET.get('page')
        if search and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = self.get_queryset().filter(Q(name__icontains=search) | Q(name__istartswith=search[0].upper())).order_by('name')
            paginator = Paginator(data, self.paginate_by)
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)

            html = render_to_string('nomenclature/search_results.html', {'nomenclatures': data, 'is_paginated': data.has_other_pages(), 'page_obj': data})
            return JsonResponse({'html': html})
        else:
            return super().get(request, *args, **kwargs)


class AddToOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nomenclatures = data.get('nomenclatures', [])
            created_orders = []

            for index, nomenclature_data in enumerate(nomenclatures):
                nomenclature = Nomenclature.objects.get(id=nomenclature_data['id'])
                nomenclature_order = NomenclatureOrder(
                    nomenclature=nomenclature,
                    key_search=nomenclature_data['key_search'],
                    quantity=nomenclature_data['quantity'],
                    invoice_line=int(f'{str(index + 1)}0'),
                    quantity_entered=nomenclature_data['quantity_entered'],
                    total_sum=nomenclature_data['total_sum']
                )
                nomenclature_order.save()
                created_orders.append(nomenclature_order.id)

            return JsonResponse({'success': True, 'created_orders': created_orders})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class DownloadSelectedOrders(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            orders = data.get('orders', [])
            orders_data = NomenclatureOrder.objects.filter(id__in=orders).order_by('nomenclature__key_product')

            data = {
                "import_data": [
                    [
                        'Ключ продукта',
                        'Ед. измерений',
                        'Количество',
                        'Строка счета',
                        'Количество введенное',
                        'Итоговая сумма'
                    ],
                    *[[order.nomenclature.key_product, order.nomenclature.unit, (i+1)*10, order.invoice_line, int(order.quantity_entered), int(order.total_sum)] for i, order in enumerate(orders_data)]
                ]
            }

            response_data = json.dumps(data, ensure_ascii=False).encode('utf8')
            return HttpResponse(response_data, content_type='application/json; charset=utf-8')

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
