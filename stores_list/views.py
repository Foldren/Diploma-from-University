from django.shortcuts import render
from index.models import Shop
from django.contrib.auth.models import User

def Index(request):
    users_staff = User.objects.filter(is_staff=1)
    shops = Shop.objects.filter(auth_user_id__in=users_staff)

    return render(request, "stores_list.html", {"stores": shops })

def ActionRenderSelectStore(request):
    filters_flag = 0

    if request.method == "POST":
        shop_id = request.POST.get("store_id")
        shop = Shop.objects.filter(id=shop_id)
        filters_flag = 1

    return render(request, "stores_list.html", {"stores": shop, "remove_filters": filters_flag })