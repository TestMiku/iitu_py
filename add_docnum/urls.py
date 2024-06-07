from django.urls import path
from .views import main, handle_uploaded_file

urlpatterns = [
    path('add-docnum/', main, name='add_docnum'),
    path('upload-file/', handle_uploaded_file, name='handle_uploaded_file'),
    # path('handle-pdf-file', v.handle_pdf_file, name='handle_pdf_file'),
]