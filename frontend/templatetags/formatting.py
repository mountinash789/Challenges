from django import template

register = template.Library()


@register.filter(name='decode_plotline')
def decode_plotline(obj):
    if obj:
        return obj.replace("\\", "\\\\")
    return obj


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
