from django import template

register = template.Library()


@register.filter
def user_connected(object, user_id):
    """Returns if user has a connection set up"""
    return object.user_connected(user_id)
