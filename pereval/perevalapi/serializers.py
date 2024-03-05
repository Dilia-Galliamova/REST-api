from django.core.exceptions import ValidationError

from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class ImagesSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Images
        fields = ['title', 'image',]

    def create(self, validated_data):
        title = validated_data.pop('title')
        record = validated_data.pop('record')
        image = validated_data.pop('image')
        return Images.objects.create(title=title, record=record, image=image)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
       model = Users
       fields = ['email', 'first_name', 'last_name', 'father_name', 'phone']

    def create(self, validated_data):
        return Users.objects.create(**validated_data)


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']

    def create(self, validated_data):
        return Coordinates.objects.create(**validated_data)


class RecordSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordinatesSerializer()
    image = ImagesSerializer(many=True)

    class Meta:
        model = Record
        exclude = ['status', 'id']
        include = ['image']

    def create(self, validated_data, **kwargs):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        image_data = validated_data.pop('image')

        user = Users.objects.create(**user_data)
        coords = Coordinates.objects.create(**coords_data)
        record = Record.objects.create(**validated_data, user=user, coords=coords, status="new")

        for image in image_data:
            title = image.pop('title')
            picture = image.pop('image')
            Images.objects.create(title=title, record=record, image=picture)

        return record

    def validate(self, data):
        image = data['image']
        for row in image:
            if row['image'] == None:
                raise ValidationError("Вы не прикрепили фото")

        return data


class RecordDetailSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordinatesSerializer()
    image = ImagesSerializer(many=True)

    class Meta:
        model = Record
        fields = '__all__'


class RecordSerializerUpdate(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    coords = CoordinatesSerializer()
    image = ImagesSerializer(many=True)

    class Meta:
        model = Record
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_title = validated_data.get('other_title', instance.other_title)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.level_summer = validated_data.get('level_summer', instance.level_summer)
        instance.level_autumn = validated_data.get('level_autumn', instance.level_autumn)
        instance.level_winter = validated_data.get('level_winter', instance.level_winter)
        instance.level_spring = validated_data.get('level_spring', instance.level_spring)
        instance.save()

        if 'coords' in validated_data.keys():
            c = instance.coords
            coords_data = validated_data.pop('coords')
            if "latitude" in coords_data.keys():
                c.latitude = coords_data['latitude']
            if "longitude" in coords_data.keys():
                c.longitude = coords_data['longitude']
            if "height" in coords_data.keys():
                c.height = coords_data['height']
            c.save()

        if 'image' in validated_data.keys():
            image_data = validated_data.pop('image')
            i_list = Images.objects.filter(record=instance)
            for image_old in i_list:
                for image_new in image_data:
                    if "image" == image_new.title:
                        picture = image_new.pop('image')
                        image_old.image = picture
                    elif image_old.image == image_new.image:
                        title = image_new.pop('title')
                        image_old.title = title
                image_old.save()


        return instance
