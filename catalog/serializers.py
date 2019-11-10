from rest_framework import serializers

from catalog.models import Photo, Catalog


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image_id', 'title', 'image_location', 'max_prints', 'shot_date']

    shot_date = serializers.DateField()


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['title', 'publish_date', 'photos']

    photos = PhotoSerializer(source='photo_set', many=True)
