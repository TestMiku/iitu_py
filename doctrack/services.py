import pytz

from doctrack.models import DTGroup, DTStatus


def can_change_status(request, dt_request):

    statuses = DTStatus.objects.all()
    if not request.user.is_superuser and statuses:
        results = []
        for status in statuses:
            if status.groups.all():
                for group in status.groups.all():
                    if request.user.role in group.avh_role.all():
                        results.append(status)
        statuses = results
    is_can_change_status = True
    if dt_request.status not in statuses:
        is_can_change_status = False
    return statuses, is_can_change_status


def can_view_documents(request):
    groups = DTGroup.objects.all()
    if not request.user.is_superuser and groups:
        results = []
        for group in groups:
            if "тех" in group.name.lower():
                results.append(group)

        for group in results:
            if request.user.role in group.avh_role.all():
                return True

        return False
    return False


def get_user_group(user):
    groups = DTGroup.objects.all()
    for group in groups:
        if user.role in group.avh_role.all():
            return group


def get_formatted_date(date):
    utc_format = pytz.timezone("Asia/Almaty")
    date = date.astimezone(utc_format)
    date_formatted = date.strftime("%d.%m.%Y %H:%M")
    date_encoded = date_formatted.encode("utf-16le")
    return date_encoded.decode("utf-16le")
