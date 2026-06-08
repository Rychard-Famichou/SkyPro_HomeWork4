from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def status_badge(value):
    if value:
        return mark_safe('<span class="badge bg-success">Опубликовано</span>')
    return mark_safe('<span class="badge bg-secondary">Черновик</span>')
