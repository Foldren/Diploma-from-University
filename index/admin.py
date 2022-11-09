from django.contrib import admin
from index.models import Shop, Product, Color, Advertising
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


admin.site.site_title = 'Stock Clothes Shops - Администрирование магазинов'
admin.site.site_header = 'Stock Clothes Shops'
admin.site.index_title = 'Панель администрирования'
admin.site.unregister(User) #для кастомизации окна с юзерами

# class MyUserInline(admin.TabularInline): #для изменения представления модели юзера
#     model=User
#     verbose_name = "Пользователь"
#     verbose_name_purpal = "Пользователи"

@admin.register(User)
class MyUserAdmin(UserAdmin):
    def view_user_shop_link(self, obj):
        url = reverse("admin:index_shop_changelist") + "?" + urlencode({"auth_user_id": f"{obj.id}"})
        name = Shop.objects.get(auth_user_id=obj.id)
        return format_html('<a href="{}">{}</a>', url, name)


    # inlines = [MyUserInline,]
    list_display = ["username", "first_name", "last_name", "view_user_shop_link", "email", "is_staff", "date_joined"]
    # prepopulated_fields = {"username": ("Имя",)}
    view_user_shop_link.short_description = "Магазин"




@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    def get_queryset(self, request): #возвращает набор экземпляров модели
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(auth_user_id=request.user.id)

    def get_html_shop_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=200>")


    list_display = ["comp_name", "number", "address", "yandex_rates_id", "get_html_shop_photo"]
    get_html_shop_photo.short_description = "Фото"




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            shop_user_id = Shop.objects.get(auth_user_id=request.user.id)
            return qs.filter(shop_info_id=shop_user_id)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs): #ставим ограничение
        if db_field.name == "shop_info" and (not request.user.is_superuser):
            kwargs["queryset"] = Shop.objects.filter(auth_user_id=request.user.id) #на вывод вариантов только для текущего магазина
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def view_product_colors_link(self, obj):
        count = obj.color_set.count()
        url = reverse("admin:index_color_changelist") + "?" + urlencode({"product_card__id": f"{obj.id}"})
        return format_html('<a href="{}">Количество: {}</a>', url, count)

    list_display = ["name", "brand", "price", "view_product_colors_link", "material", "age", "gender", "description", "season"]
    search_fields = ["name", ]
    view_product_colors_link.short_description = "Заданные цвета"




@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            shop_user_id = Shop.objects.get(auth_user_id=request.user.id)
            product_user_ids = Product.objects.filter(shop_info_id=shop_user_id)
            return qs.filter(product_card_id__in=product_user_ids)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product_card" and (not request.user.is_superuser):
            shop_user_id = Shop.objects.filter(auth_user_id=request.user.id)
            kwargs["queryset"] = Product.objects.filter(shop_info_id__in=shop_user_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_html_color_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=150>")

    def view_product_edit_link(self, obj):
        url = reverse("admin:index_product_change", args=[obj.product_card_id,])
        name = Product.objects.get(id=obj.product_card_id)
        return format_html('<a href="{}">{}</a>', url, name)


    list_display = ["article", "color", "sizes", "view_product_edit_link", "get_html_color_photo"]
    search_fields = ["article", ]
    get_html_color_photo.short_description = "Фото"
    view_product_edit_link.short_description = "Карточка товара"




@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            shop_user_id = Shop.objects.get(auth_user_id=request.user.id)
            return qs.filter(shop_info_id=shop_user_id)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop_info" and (not request.user.is_superuser):
            kwargs["queryset"] = Shop.objects.filter(auth_user_id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_html_advers_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=150>")


    list_display = ["title", "text", "get_html_advers_photo"]
    get_html_advers_photo.short_description = "Фото"