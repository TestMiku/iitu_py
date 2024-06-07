"""portal_avh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from admin_global_search.views import GlobalSearchView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from contract_report.views import main_sync_caller, show_debtdoc
from main import views as main_views
from nomenclature.views import AddToOrderView, DownloadSelectedOrders

admin.site.site_header = _("Аврора")
admin.site.site_title = _("Аврора")


urlpatterns = [
    path('', include("main.urls")),

    path('login/', main_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change_password/', main_views.change_password, name='password_change'),
    path('change_password/done/', main_views.LoginView.as_view(), name='password_change_done'),

    path('admin/', admin.site.urls),
    path("search/", GlobalSearchView.as_view(), name="admin_global_search"),
    path('avh-modules/', include('avh_modules.urls')),
    path('egov-modules/', include('egov_modules.urls')),

    path('mp/', include('mp.urls')),
    path('np/', include('np.urls')),
    path('gp/', include('gp.urls')),
    path('p1/', include('p1.urls')),
    path('p2/', include('p2.urls')),
    path('anu/', include('anu.urls')),

    # api
    path("api/", include("api.urls")),

    # anonymous
    path("gtoh/", include("google_to_html.urls")),
    path('nomenclature_add_to_order/', AddToOrderView.as_view(), name='nomenclature_add_to_order'),
    path('nomenclature/orders/download/', DownloadSelectedOrders.as_view(), name='download_selected_orders'),
  

    # Damir
    path("debt_on_doc/", show_debtdoc,  name="debt_on_doc"),
    path("main_sync_caller/", main_sync_caller,  name="main_sync_caller"),
    

    # Nurs
    path('deadline/', include('visual_deadline.urls')),
    path("import-generator-by-maw/", include("import_generator_by_maw.urls")),
    path('calculator-emr/', include('calculator_emr.urls')),
    path('process_excel/', include('contract_report.urls')),
    path('og-by-kcell/', include('order_generator_by_kcell.urls')),
    path('designer-rfe/', include('designer_requests_for_equipment.urls')),
    path('pdf-t-jsn-f1c/', include('pdf_to_json_for_1c.urls')),
    path('json-to-excel/', include('json_to_excel.urls')),
    path('constructor-do/', include('constructor_do.urls', namespace='constructor-do')),

    path('groups/13/', include('add_docnum.urls')),

    # Yernur's path
    path('report-kartel/', include('report_kartel.urls')),
    path('handbook/', include('handbook_bekzhan.urls')), 
    
    path('notifications/', include('notifications.urls')),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
