from django.views.generic import DetailView, ListView

from products.models import Product, ProductPhoto, Category


class ProductDetailView(DetailView):
    """ Представление для отображения детальной страницы товара """
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """ Отдаёт содержание страницы при get запросе """
        context = super().get_context_data(**kwargs)
        context['photo'] = [i.photo.url for i in ProductPhoto.objects.filter(product=self.object)]
        return context


class BaseProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "products/product_detail.html"

    def get_queryset(self):
        products = self.model.objects.prefetch_related(
            "product_photo"
        )
        for product in products:
            for i in product.product_photo.all():
                print(i.photo.url)

        return products


def get_products_dict(category_id: int):
    objects_dict = Product.objects.prefetch_related(
            "product_photo"
        ).filter(category_id=category_id)
    data = [{
        'name': i.name,
        'description': i.description,
        'photos': [
            j.photo for j in i.product_photo.all()]
    } for i in objects_dict]

    return data


def get_category_dict():
    category_dict = {i.category_name: i.id for i in Category.objects.filter(activity=True)}
    return category_dict
