from django.utils.text import slugify
import random,string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def product_unique_slug_generator_using_name(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8)
        )
        return product_unique_slug_generator_using_name(instance, new_slug=new_slug)
    return slug


def product_image_directory_path(instance, filename):
    return 'product_image/{0}/{1}'.format(instance.product.slug ,filename)


def product_thumbnail_directory_path(instance, filename):
    return 'product_thumbnail/{0}/{1}'.format(instance.slug ,filename)


def product_category_name_unique_slug_generator_using_name(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.category_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8)
        )
        return product_category_name_unique_slug_generator_using_name(instance, new_slug=new_slug)
    return slug


def product_company_name_unique_slug_generator_using_name(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.company_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8)
        )
        return product_company_name_unique_slug_generator_using_name(instance, new_slug=new_slug)
    return slug