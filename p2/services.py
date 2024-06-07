from django.apps import apps

# from p2.models import Comment


def get_request_from_ip_address(request):
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip_address:
        ip_address = ip_address.split(",")[0].strip()
    else:
        ip_address = request.META.get("REMOTE_ADDR")

    return f"{ip_address}"


def add_comment(
    entity,
    entity_id,
    user,
    comment,
    attached_entity=None,
    attached_entity_id=None,
    request=None,
):
    if not user.is_authenticated:
        user = None
        if request:
            comment = f"{get_request_from_ip_address(request)}: {comment}"
        else:
            return "Отказ доступа"
    # new_comment = Comment.objects.create(
    #     entity=entity,
    #     entity_id=entity_id,
    #     user=user,
    #     comment=comment,
    #     attached_entity=attached_entity,
    #     attached_entity_id=attached_entity_id,
    # )
    return "new_comment"


def get_entity_by_id(entity_name, entity_id):
    try:
        entity_model = apps.get_model(app_label="p2", model_name=entity_name)
        entity = entity_model.objects.get(id=entity_id)
        return entity
    except entity_model.DoesNotExist:
        return None
