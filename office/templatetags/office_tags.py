from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(key, str):
        keys = key.split('.')
        val = dictionary
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return None
        return val
    return dictionary.get(key)

