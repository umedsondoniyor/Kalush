from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_filter_url(context, view):
    request = context['request']
    params = request.GET.copy()

    # Remove existing 'view' parameter
    if 'view' in params:
        del params['view']

    # Set the 'view' parameter to the desired value
    params['view'] = view

    return f"?{params.urlencode()}"


@register.simple_tag
def querystring_with_sort(request, key, value):
    updated = request.GET.copy()
    updated[key] = value
    return updated.urlencode()

