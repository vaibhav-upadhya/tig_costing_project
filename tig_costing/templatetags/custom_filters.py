from django import template

register = template.Library()

@register.filter
def key(value_dict, key_name):
    """Fetches the value for a given key in a dictionary."""
    if isinstance(value_dict, dict):
        return value_dict.get(key_name, "")
    return ""