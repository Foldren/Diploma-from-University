from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from index.models import Color, Product, Shop
from pytils.translit import slugify
from math import floor

class CatalogFilter:
    genderUrlHtml = ["", "", 1]
    typeClothesUrlHtml = ["", "", 1]
    subtypeClothesUrlHtml = ["", "", 1]

    def __init__(self, gender=0, type_clothes=0, sub_type_clothes=0):
        if gender:
            self.genderUrlHtml[0] = str(Product.GENDER_LIST[gender-1][1]) + "м"
            self.genderUrlHtml[1] = slugify(self.genderUrlHtml[0])
            self.genderUrlHtml[2] = gender
            if type_clothes:
                self.typeClothesUrlHtml[0] = Product.TYPE_LIST[floor(type_clothes/100) - 1][0]
                self.typeClothesUrlHtml[1] = slugify(self.typeClothesUrlHtml[0])
                self.typeClothesUrlHtml[2] = type_clothes
                if sub_type_clothes:
                    typeClothesIndex = floor(sub_type_clothes / 100) - 1
                    subtypeClothesIndex = sub_type_clothes - (floor(sub_type_clothes / 100) * 100) - 1

                    typeClothes = Product.TYPE_LIST[typeClothesIndex][1]
                    self.subtypeClothesUrlHtml[0] = typeClothes[subtypeClothesIndex][1]
                    self.subtypeClothesUrlHtml[1] = slugify(self.subtypeClothesUrlHtml[0])
                    self.subtypeClothesUrlHtml[2] = sub_type_clothes

    def getGenderValue(gender_str):
        if gender_str == 'Женщинам' or gender_str =="1":
            return 1
        elif gender_str == 'Мужчинам' or gender_str == "2":
            return 2



def Index(request):
    productsGenderFilter = Product.objects.filter(gender=2)
    products = Color.objects.select_related("product_card").filter(product_card__in=productsGenderFilter)
    filterGender = CatalogFilter(2).genderUrlHtml

    return render(request, "catalog.html", {"products": products, "filter_by_gender": filterGender})

def ActionFilterByGender(request):
    if request.method == 'POST':
        genderPost = int(request.POST.get('gender'))
        store_id = request.POST.get("store_id")

        if store_id:
            productsGenderFilter = Product.objects.filter(gender=genderPost, shop_info_id=store_id)
        else:
            productsGenderFilter = Product.objects.filter(gender=genderPost)

        products = Color.objects.select_related("product_card").filter(product_card__in=productsGenderFilter)
        filterGender = CatalogFilter(genderPost).genderUrlHtml


        if store_id:
            shop = Shop.objects.get(id=store_id)
            filter_shop_list = [slugify(shop), store_id, shop.comp_name]
            return render(request, "catalog.html", {"products": products, "filter_by_gender": filterGender, "gender_index": genderPost, "shop_name_filter": filter_shop_list})
        else:
            return render(request, "catalog.html", {"products": products, "filter_by_gender": filterGender, "gender_index": genderPost})
    else:
        return Index(request)

def ActionFilterByTypeClothes(request):
    if request.method == "POST":
        if request.POST.get("gender"):
            genderPost = CatalogFilter.getGenderValue(request.POST.get("gender"))
            typeClothesPost = int(request.POST.get("type_clothes"))
            typeClothesList = [numb for numb in range((floor(typeClothesPost / 100) * 100), (floor(typeClothesPost / 100) * 100) + 100)]
            store_id = request.POST.get("store_id")

            if store_id:
                productsGenderTypeFilter = Product.objects.filter(gender=genderPost, type_product__in=typeClothesList, shop_info_id=store_id)
            else:
                productsGenderTypeFilter = Product.objects.filter(gender=genderPost, type_product__in=typeClothesList)

            products = Color.objects.select_related("product_card").filter(product_card__in=productsGenderTypeFilter)
            filterTypeGender = CatalogFilter(genderPost, typeClothesPost)

            if store_id:
                shop = Shop.objects.get(id=store_id)
                filter_shop_list = [slugify(shop), store_id, shop.comp_name]
                return render(request, "catalog.html", {"products": products, "filter_by_gender": filterTypeGender.genderUrlHtml, "filter_by_type_clothes": filterTypeGender.typeClothesUrlHtml, "gender_index": genderPost, "shop_name_filter": filter_shop_list, "ageC": request.POST.get("type-select-clothes"), "seasonC": request.POST.get("season-clothes")})
            else:
                return render(request, "catalog.html", {"products": products, "filter_by_gender": filterTypeGender.genderUrlHtml, "filter_by_type_clothes": filterTypeGender.typeClothesUrlHtml, "gender_index": genderPost, "ageC": request.POST.get("type-select-clothes"), "seasonC": request.POST.get("season-clothes")})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def ActionFilterBySubtypeClothes(request):
    if request.method == "POST":
        if request.POST.get("gender"):
            genderPost = CatalogFilter.getGenderValue(request.POST.get("gender"))
            subtypeClothesPost = int(request.POST.get("type_clothes"))
            store_id = request.POST.get("store_id")

            if store_id:
                productsGenderTypeFilter = Product.objects.filter(gender=genderPost, type_product=subtypeClothesPost, shop_info_id=store_id)
            else:
                productsGenderTypeFilter = Product.objects.filter(gender=genderPost, type_product=subtypeClothesPost)

            products = Color.objects.select_related("product_card").filter(product_card__in=productsGenderTypeFilter)
            filterTypeGender = CatalogFilter(genderPost, subtypeClothesPost, subtypeClothesPost)

            if store_id:
                shop = Shop.objects.get(id=store_id)
                filter_shop_list = [slugify(shop), store_id, shop.comp_name]
                return render(request, "catalog.html", {"products": products, "filter_by_gender": filterTypeGender.genderUrlHtml, "filter_by_type_clothes": filterTypeGender.typeClothesUrlHtml, "filter_by_subtype_clothes": filterTypeGender.subtypeClothesUrlHtml, "gender_index": genderPost, "shop_name_filter": filter_shop_list})
            else:
                return render(request, "catalog.html", {"products": products, "filter_by_gender": filterTypeGender.genderUrlHtml, "filter_by_type_clothes": filterTypeGender.typeClothesUrlHtml, "filter_by_subtype_clothes": filterTypeGender.subtypeClothesUrlHtml, "gender_index": genderPost})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')