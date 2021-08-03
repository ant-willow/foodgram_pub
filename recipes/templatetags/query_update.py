from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_update(context, **kwargs):
    request = context['request']
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value != 0:
            updated[key] = value
        else:
            updated.pop(key)

    return f'?{updated.urlencode()}'
