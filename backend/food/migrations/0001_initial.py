# Generated by Django 3.2.7 on 2021-10-12 16:35

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(max_length=20, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('pk',),
            },
        ),
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
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_shop', to='food.ingredients')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
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
                ('cooking_time', models.DurationField(help_text='Какое время будет готовиться?', verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='tag', to='food.Tags')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='ingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.products', verbose_name='Ингридиент'),
        ),
        migrations.AddField(
            model_name='ingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='food.recipes'),
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
            constraint=models.UniqueConstraint(fields=('buyer', 'product'), name='uniq_purchase'),
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
