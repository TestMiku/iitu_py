from django.urls import path
import pdf_to_json_for_1c.views as v

urlpatterns = [
    path('', v.main, name='pdf_to_json_for_1c'),
    # path('handle-pdf-file', v.handle_pdf_file, name='handle_pdf_file'),
    path('send-to-1c', v.send_to_1c, name='send_to_1c'),
]