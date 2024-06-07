from django.shortcuts import render, get_object_or_404, redirect
from .forms import HandbookModelForm
from .models import Handbook


def add_data(request):
    form = HandbookModelForm()
    handbooks = Handbook.objects.all()
    print("handbooks:", handbooks)

    if request.method == 'POST':
        form = HandbookModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/handbook/show')

    return render(request, 'handbook_bekzhan/add_data.html', {'form': form})


def success(request):
    return render(request, 'handbook_bekzhan/success.html')


def show_data(request):
    codes = Handbook.objects.values_list('code', flat=True).distinct()
    quantities = Handbook.objects.values_list('quantity', flat=True).distinct()
    names = Handbook.objects.values_list('name', flat=True).distinct()
    units = Handbook.objects.values_list('unit', flat=True).distinct()
    categories = Handbook.objects.values_list('category', flat=True).distinct()


    code_query = request.GET.get('code')
    quantity_query = request.GET.get('quantity')
    name_query = request.GET.get('name')
    unit_query = request.GET.get('unit')
    category_query = request.GET.get('category')

    filters = {}
    if code_query:
        filters['code__iregex'] = code_query
    if quantity_query:
        filters['quantity__iregex'] = quantity_query
    if name_query:
        filters['name__iregex'] = name_query
    if unit_query:
        filters['unit__iregex'] = unit_query
    if category_query:
        filters['category__iregex'] = category_query

    data = Handbook.objects.filter(**filters)
    
    return render(request, 'handbook_bekzhan/show_data.html', {
        'data': data, 
        'codes': codes,
        'quantities': quantities,
        'names': names,
        'units': units,
        'categories': categories,
        'code_query': code_query, 
        'quantity_query': quantity_query, 
        'name_query': name_query, 
        'unit_query': unit_query, 
        'category_query': category_query
    })


def edit_data(request, pk):
    instance = get_object_or_404(Handbook, pk=pk)
    if request.method == 'POST':
        form = HandbookModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HandbookModelForm(instance=instance)
    return render(request, 'handbook_bekzhan/edit_data.html', {'form': form})


def delete_data(request, pk):
    instance = get_object_or_404(Handbook, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect('success')
    return render(request, 'handbook_bekzhan/delete_data.html', {'instance': instance})
