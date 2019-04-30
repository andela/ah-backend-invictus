import string
import random

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None, **kwargs):
    if new_slug is not None:
        slug = new_slug
    slug = slugify(instance.title)
    print(slug)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        random_string = random_string_generator(size=4)
        new_slug = slug+"-"+random_string
        print(new_slug)
        return new_slug
    return slug
