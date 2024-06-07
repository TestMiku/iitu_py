import os
import subprocess

from django.shortcuts import render
from django.views.generic import ListView

from egov_modules.utils import PYTHON_PATH, SCRIPT_PATH
from portal_avh import settings


class EgovCreateOrderView(ListView):
    template_name = 'egov_modules/egov_create_order.html'
    context_object_name = 'egov_create_order'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'egov_create_order': self.context_object_name})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.FILES:
            uploaded_file = request.FILES['schema_plan_land_plot']

            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            data = {
                "choice_licensor": request.POST.get('choice_licensor'),
                "full_name_representative": request.POST.get('full_name_representative'),
                "phone_number": request.POST.get('phone_number'),
                "location_land_plot": request.POST.get('location_land_plot'),
                "requested_right_use": request.POST.get('requested_right_use'),
                "area": request.POST.get('area'),
                "purpose_use_land_plot": request.POST.get('purpose_use_land_plot'),
                "schema_plan_land_plot": file_path,
            }

            # Вызываем скрипт для отправки данных в ЕГОВ
            subprocess.Popen([
                PYTHON_PATH,
                SCRIPT_PATH,
                data['choice_licensor'],
                data['full_name_representative'],
                data['phone_number'],
                data['location_land_plot'],
                data['requested_right_use'],
                data['area'],
                data['purpose_use_land_plot'],
                data['schema_plan_land_plot']
            ])

            return render(request, self.template_name, {'egov_create_order': self.context_object_name})
