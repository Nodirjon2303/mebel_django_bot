# Generated by Django 3.2.6 on 2021-08-17 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture_bycat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Furniture_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(null=True)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('current_room', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=100)),
                ('eni', models.FloatField(default=0)),
                ('buyi', models.FloatField(default=0)),
                ('balandligi', models.FloatField(default=0)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='runbot.profile')),
            ],
        ),
        migrations.CreateModel(
            name='furnitures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('price', models.FloatField(default=0)),
                ('eni', models.FloatField(default=0)),
                ('buyi', models.FloatField(default=0)),
                ('balandligi', models.FloatField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='runbot.furniture_bycat')),
            ],
        ),
        migrations.AddField(
            model_name='furniture_bycat',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='runbot.furniture_category'),
        ),
    ]
