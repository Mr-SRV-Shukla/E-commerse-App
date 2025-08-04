from django import template

register=template.Library()

@register.simple_tag
def format_category(categories, product="Products"):
    return f"{categories}{product}"
