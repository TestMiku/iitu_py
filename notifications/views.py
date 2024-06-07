from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Notification

@login_required
def notification_list(request):
    if request.method == 'POST' and 'delete_selected' in request.POST:
        selected_notifications = request.POST.getlist('selected_notifications')
        Notification.objects.filter(id__in=selected_notifications, to_whom=request.user).delete()
        return redirect('notifications:list')

    notifications = Notification.objects.filter(to_whom=request.user).order_by('-created_at')

    formatted_notifications = []
    for notification in notifications:
        created_at = notification.created_at
        if created_at.date() == timezone.now().date():
            date_str = created_at.strftime('%H:%M')
        elif created_at.date() == (timezone.now().date() - timezone.timedelta(days=1)):
            date_str = 'Вчера'
        else:
            date_str = created_at.strftime('%m.%d')
        formatted_notifications.append({
            'id': notification.id,
            'title': notification.title,
            'body': notification.body,
            'from_whom': notification.from_whom,
            'date_str': date_str,
            'is_read': notification.is_read,
        })

    context = {
        'notifications': formatted_notifications,
        'notifications_count': len(formatted_notifications),
    }
    return render(request, 'notifications/notifications.html', context)

@login_required
@csrf_exempt
def mark_as_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('id')
        try:
            notification = Notification.objects.get(id=notification_id, to_whom=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def latest_notifications(request):
    notifications = Notification.objects.filter(to_whom=request.user).order_by('-created_at')[:5]
    data = [
        {
            'title': notification.title,
        }
        for notification in notifications
    ]
    return JsonResponse(data, safe=False)


# ------------------------------------------
#         Шаблон создания уведомления
# ------------------------------------------
#
# from myapp.notifications.models import Notification
#
# def document_status_changed(document, new_status):
#     title = f"Статус документа {document.title} изменен"
#     body = f"Статус документа {document.title} изменен с '{document.status}' на '{new_status}'"
#     Notification.create_notification(from_user=document.modified_by, to_user=document.owner, title=title, body=body)