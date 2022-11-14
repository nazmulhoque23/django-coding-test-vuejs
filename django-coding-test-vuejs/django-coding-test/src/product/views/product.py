from django.views import generic
from django.db.models import Count,Min, Max
from django.views.generic import ListView
from product.models import Variant
from product.models import ProductVariantPrice, Product, ProductVariant, Variant
from django.shortcuts import get_object_or_404

class ProductListView(ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    paginate_by =3 

    def get_queryset(self):
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        if title != '' and title is not None:
            new_context = Product.objects.filter(title__icontains = title)

        elif (price_from !='' and price_from is not None)  and (price_to !='' and price_to is not None):
           price_to = ProductVariantPrice.objects.all().aggregate(Max('price'))['price__max']
           new_context = ProductVariantPrice.objects.filter(price__range= (price_from, price_to))
            
        
        # elif variant != '' and variant is not None:
        #     variant_context = ProductVariant.objects.filter(variant_title__icontains = variant)
        #     return variant_context

        else:
            new_context = Product.objects.all()
            
        return new_context 

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['variant_context'] = ProductVariantPrice.objects.all()
        context['variant'] = Variant.objects.all()
        context['product_variant'] = ProductVariant.objects.all()
        #values('variant__title')
        return context
    

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
