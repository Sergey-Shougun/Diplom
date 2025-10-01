from rest_framework import serializers
from .models import User, Coords, Level, Pereval, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'fam', 'name', 'otc']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect',
                  'add_time', 'user', 'coords', 'level', 'images', 'status']
        read_only_fields = ['id', 'status']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user, created = User.objects.get_or_create(**user_data)

        coords = Coords.objects.create(**coords_data)

        level = Level.objects.create(**level_data)

        pereval = Pereval.objects.create(
            user=user,
            coords=coords,
            level=level,
            **validated_data
        )

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval

    def update(self, instance, validated_data):
        if 'coords' in validated_data:
            coords_data = validated_data.pop('coords')
            coords_serializer = CoordsSerializer(instance.coords, data=coords_data, partial=True)
            if coords_serializer.is_valid():
                coords_serializer.save()

        if 'level' in validated_data:
            level_data = validated_data.pop('level')
            level_serializer = LevelSerializer(instance.level, data=level_data, partial=True)
            if level_serializer.is_valid():
                level_serializer.save()

        if 'images' in validated_data:
            instance.images.all().delete()

            images_data = validated_data.pop('images')
            for image_data in images_data:
                Image.objects.create(pereval=instance, **image_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
