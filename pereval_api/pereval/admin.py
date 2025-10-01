from django.contrib import admin
from .models import User, Coords, Level, Pereval, Image


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'fam', 'name', 'otc')
    search_fields = ('email', 'phone', 'fam', 'name')


@admin.register(Coords)
class CoordsAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'height')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('winter', 'summer', 'autumn', 'spring')


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Pereval)
class PerevalAdmin(admin.ModelAdmin):
    list_display = ('title', 'beauty_title', 'status', 'add_time')
    list_filter = ('status', 'level')
    search_fields = ('title', 'beauty_title')
    inlines = [ImageInline]
# Register your models here.
