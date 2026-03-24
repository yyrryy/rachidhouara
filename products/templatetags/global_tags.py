from django import template
from main.models import Produit, Category
from django.template.defaultfilters import stringfilter
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
register = template.Library()

@register.simple_tag
def allproducts():
    return 44

@register.simple_tag
def allcategories():
    return Category.objects.all()


@register.filter(name='contains')
def contains(value, substring):
    """Checks if the value contains the given substring."""
    return substring in value

@register.filter(name='split')
def split_string(value, delimiter):
    """Splits the string by the given delimiter."""
    if isinstance(value, str):
        return value.split(delimiter)
    return value

@register.simple_tag
def firstctg():
    return Category.objects.order_by('code').first()

@register.filter(name='intspace')
@stringfilter
def intspace(value):
    # Split the value into integer and decimal parts

    if len(value)>1:
        parts = str(value).split('.')
    # Format the integer part with spaces as thousands separators
        integer_part = "{:,}".format(int(parts[0])).replace(',', ' ')

        # If there's a decimal part, join it back
        formatted_number = integer_part + ('.' + parts[1] if len(parts) > 1 else '')

        return formatted_number
    else:
        return value
@register.filter(name='dateadd')
@stringfilter
def dateadd(value):
    date_time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')  # Include milliseconds and timezone info

    # Step 2: Add one hour to the datetime object
    new_date_time = date_time + timedelta(hours=1)

    # Step 3: Create a new variable with the new date and hour
    new_value = new_date_time.strftime('%Y-%m-%d %H:%M')

    # Step 4: Return the new variable
    return new_value
