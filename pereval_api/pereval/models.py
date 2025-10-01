from django.db import models


class User(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2, blank=True, null=True)
    summer = models.CharField(max_length=2, blank=True, null=True)
    autumn = models.CharField(max_length=2, blank=True, null=True)
    spring = models.CharField(max_length=2, blank=True, null=True)


class Pereval(models.Model):
    STATUS_CHOICES = [
        ('new', 'новый'),
        ('pending', 'модератор взял в работу'),
        ('accepted', 'модерация прошла успешно'),
        ('rejected', 'модерация прошла, информация не принята'),
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')


class Image(models.Model):
    pereval = models.ForeignKey(Pereval, related_name='images', on_delete=models.CASCADE)
    data = models.TextField()
    title = models.CharField(max_length=255)
# Create your models here.
