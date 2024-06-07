import decimal
from django import template
from .. import models

register = template.Library()


@register.filter
def balance(account: models.Account, project_region: models.ProjectRegion) -> decimal.Decimal:
    return account.balance(project_region)
