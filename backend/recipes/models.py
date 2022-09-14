from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import is_hex_code
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        verbose_name="tag name",
        max_length=200,
        unique=True,
        blank=False
    )
    color = models.CharField(
        verbose_name="HEX color code",
        max_length=7,
        validators=[is_hex_code],
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        verbose_name="tag slug",
        max_length=200,
        unique=True,
        blank=False
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='ingredient name',
        max_length=200,
        blank=False
    )
    measurement_unit = models.CharField(
        verbose_name='measurment unit of ingredient',
        max_length=200,
        blank=False
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='pair ingredient/measure must be unique',
            ),
        ]

    def __str__(self):
        return f'{self.name} / {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='recipe author',
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        verbose_name='ingredients for recipe',
        through='IngredientAmount',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag',
        verbose_name='recipe tags',
        blank=True
    )
    name = models.CharField(
        verbose_name='recipe name',
        max_length=200,
        blank=False
    )
    text = models.TextField(
        verbose_name='recipe description',
        unique=True,
        blank=False
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='recipe image',
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='cooking time',
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='ingredient',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='recipe',
        blank=False
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='amount of an ingredient',
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(9999)
        ]
    )

    class Meta:
        verbose_name_plural = 'ingredients amounts'
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='pair ingredient/recipe must be unique',
            ),
        ]

    def __str__(self):
        return (f'{self.amount} {self.ingredient.measurement_unit}'
                f' of {self.ingredient.name}')


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='fan',
        verbose_name='subscriber',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='recipe to favorites',
        blank=False
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user can favorite recipe just once',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} / {self.user} favorites'


class ShoppingCartItem(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name='client',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_to_cart',
        verbose_name='recipe to cart',
        blank=False
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user can add recipe to shopping cart just once',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} / {self.user} shopping cart'
