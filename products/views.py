import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from products.models  import Product, ProductImage, TasteByProduct


class MainProductView(View): 
    def get(self, request): 
        premiums             = Product.objects.all().order_by('-price')[:3]
        fresh_products       = Product.objects.all().order_by('-roasting_date')[:4]

        result_premium       = [{
                    'id'            : premium.id,
                    'name'          : premium.name,
                    'eng_name'      : premium.eng_name,
                    'img'           : [image.url for image in ProductImage.objects.filter(product_id = premium.id)],
                    'roasting_date' : premium.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in TasteByProduct.objects.filter(product_id = premium.id)],
                    'price'         : premium.price
                } for premium in premiums]
        
        result_fresh_product = [{
                    'id'            : fresh_product.id,
                    'name'          : fresh_product.name,
                    'eng_name'      : fresh_product.eng_name,
                    'img'           : [image.url for image in ProductImage.objects.filter(product_id = fresh_product.id)],
                    'roasting_date' : fresh_product.roasting_date,
                    'taste'         : [flavor.taste.name for flavor in TasteByProduct.objects.filter(product_id = fresh_product.id)],
                    'price'         : fresh_product.price
                } for fresh_product in fresh_products]

        return JsonResponse({'premium' : result_premium,'fresh_product' : result_fresh_product}, status = 200)


class CoffeeProductView(View):
    def get(self, request):      
        page             = int(request.GET.get('page', 1)or 1)
        category         = request.GET.get('category')or None
        tastes           = request.GET.getlist('taste')or None
        filter           = request.GET.getlist('filter')or None
        page_size        = 12
        limit            = page_size * page
        offset           = limit - page_size
        
        products         = Product.objects.all().order_by('id')
    
        if category:
            products     = Product.objects.filter(subcategory_id=category).order_by('id')
        
        if tastes:
            products     = products.filter(taste__name__in=tastes).order_by('id').distinct()
        
        if filter:
            if 'Highprice' in filter:
                products = products.order_by('-price')
                if 'Highprice' in filter and 'roast' in filter:
                    products = products.order_by('-roasting_date')
            elif 'Lowprice' in filter:
                products = products.order_by('price')
                if 'Lowprice' in filter and 'roast' in filter:
                    products = products.order_by('-roasting_date')
            elif 'roast' in filter:
                products = products.order_by('-roasting_date')
    
        products = products[offset:limit]
        print(products)
        result_products = [{
                    'id'           : product.id,
                    'name'         : product.name,
                    'eng_name'     : product.eng_name,
                    'img'          : [image.url for image in ProductImage.objects.filter(product_id=product.id)],
                    'taste'        : [flavor.taste.name for flavor in TasteByProduct.objects.filter(product_id = product.id)],
                    'roasting_date': product.roasting_date,
                    'price'        : product.price
                }for product in products]

            
        return JsonResponse(
            {'shop_product_list'   : result_products},
            status = 200
        )