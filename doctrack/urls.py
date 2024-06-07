from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='doctrack'),
    path('change_type_work', views.change_type_work, name='change_type_work'),
    
    # Заявки
    path('info/<int:pk>', views.request_info, name='request_info'),
    path('delete/<int:pk>', views.request_delete, name='request_delete'),
    path('restore/<int:pk>', views.request_restore, name='request_restore'),
    path('edit/<int:id>', views.request_update, name='request_update'),
    path('add', views.request_add, name='request_add'),
    
    # Массовые действия
    path('change_document_status/<int:pk>', views.change_document_status, name='change_document_status'),
    path('get_date_current_status/<int:request_pk>/<int:status_id>', views.get_date_current_status, name='get_date_current_status'),
    path('is_rejected_status/<int:request_pk>/<int:status_id>', views.is_rejected_status, name='is_rejected_status'),
    path('comment_for_rejected_order/<int:request_pk>', views.comment_for_rejected_order, name='comment_for_rejected_order'),
    
    # Документы
    path('add_document/<int:request_id>', views.add_document, name='add_document'),
    path('add_document_request/<int:request_id>', views.add_document_request, name='add_document_request'),
    path('update_document/<int:request_id>/<int:document_id>', views.update_document, name='update_document'),
    path('delete_document/<int:document_id>', views.delete_document, name='delete_document'),

    path('unsubscribe/<int:request_pk>', views.unsubscribe, name='request_unsubscribe'),
    path('subscribe/<int:request_pk>', views.subscribe, name='request_subscribe'),
    path('change_status/<int:request_pk>', views.change_status, name='request_change_status'),
]
