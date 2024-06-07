from django.urls import path

from main import views as main_views
from . import views

urlpatterns = [
    path('', views.distributor, name='distributor'),
    # path('distr/', views.distributor, name='distributor'),
    path('upload/', views.upload_document, name='upload_document'),
    path('projlis', views.ProjectList.as_view(), name='project_list'),
    path('projlis/<int:request_number>/', views.ProjectList.as_view(), name='project_list_with_number'),

    path('download/<int:document_id>/', views.download_document, name='download_document'),

    path('delete/<int:pk>/', views.DocumentDelete.as_view(), name='document_delete'),
    path('get_work_types/', views.get_work_types, name='get_work_types'),
    path('get_doc_types/', views.get_doc_types, name='get_doc_types'),
    path('documents/', views.document_list, name='document_list'),
    path('document-list/', views.document_list, name='document_list'),

    path('create_request', views.create_request, name='create_request'),

    path('confirm_document/<int:document_id>/', views.confirm_document, name='confirm_document'),
    path('reject_document/<int:document_id>/', views.reject_document, name='reject_document'),
    path('add-comment/<int:document_id>/', views.add_comment, name='add_comment'),

    path('bulk-confirm-documents/<int:pk>', views.bulk_confirm_documents, name='bulk_confirm_documents'),
    path('bulk-reject-documents/<int:pk>', views.bulk_reject_documents, name='bulk_reject_documents'),

    path('confirm_document_rent/<int:document_rent_id>/', views.confirm_document_rent, name='confirm_document_rent'),
    path('reject_document_rent/<int:document_rent_id>/', views.reject_document_rent, name='reject_document_rent'),

    path('view_request/<int:request_number>/', views.view_request, name='view_request'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('view_upload_documents/', views.view_upload_document, name='view_upload_documents'),

    path('edit_document/<int:request_number>/', views.edit_request_documents, name='edit_document'),
    path('edit_document_rent/<int:request_number>/', views.edit_document_rent, name='edit_document_rent'),

    path('download_crm_excel/', views.download_crm_excel, name='download_crm_excel'),

    path('rejected_documents/', views.view_rejected_documents, name='rejected_documents'),
    path('increase_history_count/<int:request_number>/', views.increase_history_count, name='increase_history_count'),

    path('approve_request_full/<int:request_number>/', views.approve_request_full, name='approve_request_full'),
    path('approve_request/<int:request_number>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:request_number>/', views.reject_request, name='reject_request'),
    path('close_request_full/<str:request_number>/', views.close_request_full, name='close_request_full'),

    path('upload_additional_document/<int:request_id>/', views.upload_additional_document, name='upload_additional_document'),

    # path('request_history/<int:request_number>/', views.request_history_view, name='request_history'),

    path('close_request/<int:request_number>/', views.close_request, name='close_request'),

    path('request_history/<int:request_number>/', views.request_history, name='request_history'),
    path('download_all_documents/<int:request_number>/', views.download_all_documents, name='download_all_documents'),

    path('comments/<str:entity>/<int:entity_id>', views.comments, name='comments'),
]
