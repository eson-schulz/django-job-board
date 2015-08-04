import bleach
from django import template
import datetime
from jobs import settings

register = template.Library()


# Thanks to https://djangosnippets.org/snippets/116/
def dayssince(value):
    "Returns number of days between today and value."
    today = datetime.date.today()
    diff  = today - value
    if diff.days > 1:
        return '%s days ago' % diff.days
    elif diff.days == 1:
        return 'yesterday'
    elif diff.days == 0:
        return 'today'
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")


@register.filter(is_safe=True)
def bleach_escape(text):
    allowed_tags = settings.ALLOWED_TAGS
    return bleach.clean(text, allowed_tags)


register.filter('dayssince', dayssince)