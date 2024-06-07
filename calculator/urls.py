from django.contrib import admin
from django.urls import path, include
from calculator import views as c_views

urlpatterns = [
    path('', c_views.main, name='calculator'),
    path('set_prices/', c_views.set_prices, name='set_prices'),
    path('set_orders/', c_views.set_orders, name='set_orders'),
    path('set_order_fast/', c_views.set_order_fast, name='set_order_fast'),
    path('remove_orders/', c_views.remove_orders, name='remove_orders'),
    path('find/', c_views.find_order, name='find_calculator'),
    path('change_nds/', c_views.change_nds, name='change_nds'),
    path('zero-order', c_views.zero_order, name='zero_order'),
    path('hand_update_7_35/', c_views.test, name='test'),
    path('hand_update_19_45/', c_views.test2, name='test2'),
    path('hand_update_7_11_2/', c_views.hand_update_7_11_2, name='hand_update_7_11_2'),
    path('export_excel/', c_views.export_excel, name='export_excel'),
    path('excel_import_19_45/', c_views.excel_import_19_45, name='excel_import_19_45'),
    path('update_21_22/', c_views.update_21_22, name='update_21_22'),
    # path('list/', c_views.list_order, name='list_calculator'),
    # path('my/', c_views.my_order, name='my_calculator'),
    # path('view/<int:order_id>', c_views.view_order, name='view'),
    # path('export_html_file/<int:order_id>', c_views.export_html_file, name='export_html_file'),

    # path('list/', c_views.list_order, name='list_calculator'),
    # path('19_45/', c_views.import_19_45, name='19_45'),
]
