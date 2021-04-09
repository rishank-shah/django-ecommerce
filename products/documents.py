from .models import Product
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'product-index'

    class Django:
        model = Product

        fields = [
            "name",
            "category",
            "description",
            "slug",
            "thumbnail"
        ]