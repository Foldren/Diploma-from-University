from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Shop(models.Model):
    auth_user = models.ForeignKey(User, on_delete = models.CASCADE, default=False, verbose_name="Владелец", editable=False) #добавим как внешний ключ auth_user через SQL Server и добавим каскадное удаление другим (эмулятор cascade)
    comp_name = models.CharField(max_length=120, verbose_name="Название")
    number = models.CharField(max_length=11, verbose_name="Телефон")
    address = models.CharField(max_length=150, verbose_name="Адрес")
    image = models.ImageField(upload_to='shops', max_length=300, verbose_name="Фон", unique=True)
    description = models.TextField(max_length=300, default="", verbose_name="Описание")
    yandex_rates_id = models.BigIntegerField(default=0, verbose_name="Индекс яндекс отзывов", help_text="Найдите свою организацию на Яндекс Картах, откройте список отзывов, затем скопируйте цифровой код после названия вашей организации из URL")

    class Meta:
        db_table = 'shop_info'
        verbose_name = 'магазин'
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f"{self.comp_name}"


class Advertising(models.Model):
    shop_info = models.ForeignKey(Shop, on_delete = models.CASCADE, default=False, verbose_name="Магазин") #default=False убирает 0 значение из списка в форме
    title = models.CharField(max_length=59, verbose_name="Заголовок")
    text = models.TextField(max_length=120, verbose_name="Описание")
    image = models.ImageField(upload_to='advertising', max_length=300, verbose_name="Фон", unique=True)

    class Meta:
        db_table = 'advertising'
        verbose_name = 'реклама'
        verbose_name_plural = "Рекламные баннеры"

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    AGE_LIST = [
        (1, 'Взрослый'),
        (2, 'Тинейджер'),
        (3, 'Ребенок'),]

    GENDER_LIST = [
        (1, 'Женщина'),
        (2, 'Мужчина'),]

    BRAND_LIST = [
        ('Corneliani','Corneliani'),
        ('Nike','Nike'),
        ('Adidas','Adidas'),
        ('Puma','Puma'),
        ('Prada','Prada'),
        ('Balenciaga','Balenciaga'),
        ('Gucci','Gucci'),
        ('Off-White','Off-White'),
        ('Saint Laurent','Saint Laurent'),
        ('Tom Ford','Tom Ford'),
        ('Valentino','Valentino'),
        ('Louis Vuitton','Louis Vuitton'),]

    SEASON_LIST = [
        (1, 'Лето'),
        (2, 'Зима'),
        (3, 'Демисезон'),]

    TYPE_LIST = [
        ('Обувь', (
                (101, 'Ботинки'),
                (102, 'Кроссовки и кеды'),
                (103, 'Сандалии'),
                (104, 'Туфли'),
            )
        ),
        ('Одежда', (
                (201, 'Верхняя одежда'),
                (202, 'Брюки'),
                (203, 'Футболки'),
                (204, 'Рубашки'),
                (205, 'Трикотаж'),
                (206, 'Юбки'),
            )
        ),
        ('Аксессуары', (
                (301, 'Галстуки'),
                (302, 'Зонты'),
                (303, 'Часы'),
                (304, 'Ремни и пояса'),
                (305, 'Сумки'),
            )
        ),]

    reg_validator_price = RegexValidator(regex="^[0-9]+$", message="Цена указана неверно, смотрите подсказки")

    shop_info = models.ForeignKey(Shop, on_delete = models.CASCADE, default=False, verbose_name="Магазин") #default=False
    age = models.IntegerField(choices=AGE_LIST, default=False, verbose_name="Возраст")
    gender = models.IntegerField(choices=GENDER_LIST, default=False, verbose_name="Пол")
    name = models.CharField(max_length=35, verbose_name="Название")
    price = models.CharField(max_length=6, verbose_name="Цена", validators=[reg_validator_price], help_text="Введите число до: 999999")
    brand = models.CharField(max_length=40, default=False, choices=BRAND_LIST, verbose_name="Бренд")
    material = models.CharField(max_length=120, default="Выберите материал", verbose_name="Материал")
    season = models.IntegerField(choices=SEASON_LIST, default=False, verbose_name="Сезон")
    description = models.TextField(max_length=320, default="Добавьте описание", verbose_name="Описание")
    type_product = models.IntegerField(choices=TYPE_LIST, default=False, verbose_name="Тип")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'product_card'
        verbose_name = 'товар'
        verbose_name_plural = "Карточки товаров"


class Color(models.Model):
    COLOR_LIST = [
        (1, 'Черный'),
        (2, 'Зеленый'),
        (3, 'Синий'),
        (4, 'Красный'),
        (5, 'Белый')]

    reg_validator_sizes = RegexValidator(regex="^(\d{2} )*(\d{2})$", message="Размеры указаны неверно, смотрите подсказки")

    product_card = models.ForeignKey(Product, on_delete = models.CASCADE, default=False, verbose_name="Товар") #default=False
    color = models.IntegerField(choices=COLOR_LIST, verbose_name="Цвет", default=1)
    article = models.CharField(max_length=12, verbose_name="Артикул")
    sizes = models.CharField(max_length=40, verbose_name="Размеры", validators=[reg_validator_sizes], help_text="Используйте формат: 41 42 43 ..")
    image = models.ImageField(upload_to='products', max_length=300, verbose_name="Фото", unique=True)

    def __str__(self):
        return f"{Product.objects.get(id=self.product_card_id)} {self.COLOR_LIST[self.color-1][1]}"

    class Meta:
        db_table = 'product_color'
        verbose_name = 'цвет товара'
        verbose_name_plural = "Цвета для карточек товаров"
        unique_together = 'product_card', 'color'