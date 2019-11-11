from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image_id', 'title', 'image_location', 'max_prints', 'shot_date']

    shot_date = serializers.DateField()
