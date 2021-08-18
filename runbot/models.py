from django.db import models


class Profile(models.Model):
    telegram_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    current_room = models.IntegerField(null=True)

    def __str__(self):
        return self.first_name


class Furniture_category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.category_name


class Furniture_bycat(models.Model):
    category = models.ForeignKey(Furniture_category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Furnitures(models.Model):
    category = models.ForeignKey(Furniture_bycat, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=45)
    image = models.ImageField(null=True)
    price = models.FloatField(default=0)
    eni = models.FloatField(default=0)
    buyi = models.FloatField(default=0)
    balandligi = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=100, null=True)
    eni = models.FloatField(default=0)
    buyi = models.FloatField(default=0)
    balandligi = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    furniture = models.ForeignKey(Furnitures, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=23, default='zakaz berildi')
    order_date = models.DateField(null=True, auto_now_add=True)
    def __str__(self):
        return f"{self.profile.first_name} {self.furniture.name}"


class Savatcha(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furnitures, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
