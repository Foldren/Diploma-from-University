from django.shortcuts import render
from index.models import Color, Shop, Product
# from django.http import HttpResponse
from pytils.translit import slugify

def Index(request):
    product_data = None

    if request.method == 'POST':
        color_id = request.POST.get('id_product')
        product_data = Color.objects.select_related("product_card").get(id=color_id)

        product_element = Product.objects.get(id=product_data.product_card_id)
        comp_name_address = Shop.objects.get(id=product_element.shop_info_id)

        first_color = Color.objects.filter(id=color_id)
        products_color = Color.objects.filter(product_card_id=product_element)
        sorted_colors = first_color.union(products_color)

        transliterate_name_shop = slugify(comp_name_address.comp_name)
        breadcrumps = request.POST.get('breadcrumps')

    return render(request, "product_card.html", {"product_info": product_data, "comp_info": comp_name_address, "product_colors": sorted_colors, "trans_name_shop": transliterate_name_shop, "breadcrumps_catalog": breadcrumps})