from django import template

register = template.Library()

@register.filter
def unique(queryset, field):
    """Return unique values from queryset based on field"""
    seen = set()
    unique_items = []
    
    for item in queryset:
        value = getattr(item, field)
        if value not in seen:
            seen.add(value)
            unique_items.append(item)
    
    return unique_items 