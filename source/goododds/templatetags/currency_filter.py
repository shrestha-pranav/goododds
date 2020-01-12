# Add payment currency template
from django import template

register = template.Library()

def currency(credits):
    return f"${credits//100:d}.{credits%100:02d}"

register.filter('currency', currency)
