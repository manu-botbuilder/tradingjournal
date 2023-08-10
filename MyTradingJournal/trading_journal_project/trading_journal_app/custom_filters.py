from django.template.defaultfilters import stringfilter


@stringfilter
def int_to_string(value):
    return value