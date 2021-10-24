# Generated by Django 3.2.7 on 2021-10-21 19:28

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название продукта')),
                ('measurement_unit', models.CharField(max_length=10, verbose_name='Еденица измерения')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(help_text='Фотография готового блюда', upload_to='recipe/', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Как готовится это блюдо?', max_length=10000, verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveIntegerField(help_text='Сколько минут будет готовиться?', verbose_name='Время приготовления в минутах')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя тега')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', max_length=18, unique=True, verbose_name='Цвет тега')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingLists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buying', to='food.recipes')),
            ],
            options={
                'verbose_name': 'Список покупок для рецепта',
                'verbose_name_plural': 'Список покупок для рецептов',
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='tag', to='food.Tags'),
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(max_length=20, verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.products', verbose_name='Ингридиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='food.recipes')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admirer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admirer', to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='food.recipes')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'ordering': ('pk',),
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglists',
            constraint=models.UniqueConstraint(fields=('buyer', 'products'), name='uniq_shopping_list'),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='uniq_ingredients'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('admirer', 'recipe'), name='uniq_favorite'),
        ),
    ]
