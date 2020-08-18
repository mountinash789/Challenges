from django import template

register = template.Library()


@register.filter(name='decode_plotline')
def decode_plotline(obj):
    if obj:
        return obj.replace("\\", "\\\\")
    return obj
