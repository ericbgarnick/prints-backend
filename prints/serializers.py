from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from photos.models import Photo
from prints.models import PrintSizeInfo, PrintSize, Print


class PrintSizeInfoSerializer(serializers.ModelSerializer):
    size = serializers.ChoiceField(
        choices=[ps[1] for ps in PrintSize.choices()]
    )

    class Meta:
        model = PrintSizeInfo
        fields = ['base_price_cents', 'ship_price_cents', 'size']


class PrintSerializer(serializers.ModelSerializer):
    """Write-only"""
    class Meta:
        model = Print
        fields = ['size', 'image_id']

    def is_valid(self, raise_exception=False):
        size = self.initial_data.get('size')
        image_id = self.initial_data.get('image_id')
        # These instance vars must be created here
        self._errors = []
        self._validated_data = self.initial_data

        try:
            print_size = PrintSize[size.upper()]
        except KeyError:
            print_size = None
            self._errors.append(f"No PrintSize found for size {size}")

        if not PrintSizeInfo.objects.filter(size=print_size).exists():
            self._errors.append(f"No PrintSizeInfo found for size {size}")
        if not Photo.objects.filter(image_id=image_id).exists():
            self._errors.append(f"No photo found with image_id {image_id}")

        if self._errors and raise_exception:
            raise ValidationError(self._errors)

        return not bool(self._errors)

    def create(self, validated_data):
        size = validated_data['size']
        size_info = PrintSizeInfo.objects.get(size=PrintSize[size.upper()])
        image_id = validated_data['image_id']
        # TODO: Validate that this image_id is valid
        photo = Photo.objects.get(image_id=image_id)
        num_prints = Print.objects.filter(photo=photo).count()
        # TODO: Validate that the max number of prints is not exceeded
        return Print.objects.create(size_info=size_info, photo=photo,
                                    print_number=num_prints + 1)

    # TODO: This is a hack because the inherited errors property was failing - find proper solution
    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors
