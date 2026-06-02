from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    # Связь с категорией: у одной категории может быть много товаров
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    # Связь с товаром: у одного товара может быть много отзывов
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")

    def __str__(self):
        return f"Отзыв для {self.product.title}"