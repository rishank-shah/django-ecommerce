from .models import Product,Company,Category
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

@registry.register_document
class ProductDocument(Document):

    category = fields.ObjectField(
        properties={
            'category_name': fields.TextField()
        }
    )

    company = fields.ObjectField(
        properties={
            'company_name': fields.TextField()
        }
    )

    class Index:
        name = 'product-index'

    class Django:
        model = Product

        fields = [
            "name",
            "description",
            "slug",
            "thumbnail"
        ]

        related_models = [
            Company,
            Category
        ]
    
    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related(
            'category',
            'company'
        )
    
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.product_set.all()
        elif isinstance(related_instance, Company):
            return related_instance.product_set.all()