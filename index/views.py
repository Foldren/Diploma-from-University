from django.shortcuts import render
from index.models import Shop, Advertising
from django.contrib.auth.models import User, Group
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from pytils.translit import slugify

def Index(request):
    users_id = User.objects.filter(is_staff=1)
    shops_id = Shop.objects.filter(auth_user_id__in=users_id)
    advertisings = Advertising.objects.filter(shop_info_id__in=shops_id)
    transliterate_names = []

    for element in shops_id:
        transliterate_names.append(slugify(element.comp_name))

    return render(request, "index.html", {"adversitings": advertisings, "actions": transliterate_names})

def ActionRegistrationShop(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username = request.POST.get('username'),
            email = request.POST.get('email'),
            password = request.POST.get('password'))

        group = Group.objects.get(name='Shops')
        user.groups.add(group)

        shop = Shop.objects.create(
            auth_user_id = user.id,
            comp_name = request.POST.get('comp_name'),
            number = request.POST.get('number'),
            address = request.POST.get('address'),
            image = "noimage_detail.png")

        Advertising.objects.create(
            shop_info_id = shop.id,
            title = request.POST.get('comp_name'),
            text = "Новый магазин, описание появится скоро :)",
            image = "noimage_detail.png")
        return HttpResponse("Isaac, you did it!")