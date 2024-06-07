from django.urls import path, include

from mp import views as mp_views

urlpatterns = [
    path('statapps/<int:id>', mp_views.one_statapp, name='statapp'),
    path('dounload_statapps/<int:id>', mp_views.dounload_statapps, name='dounload_statapps'),
    path('add_statapp/', mp_views.create_static_app, name='create_static_app'),
    path('create_or_update_chapter/<int:statapp_id>', mp_views.create_or_update_chapter,
         name='create_or_update_chapter'),

    path('calculator/', include('calculator.urls'), name='calculator'),
    path('html_order_generator/', mp_views.html_order_generator, name='html_order_generator'),
    path('doctrack/', include("doctrack.urls"), name='doctrack'),
    path('document_debts/', include("document_debts.urls"), name='document_debts'),
]
