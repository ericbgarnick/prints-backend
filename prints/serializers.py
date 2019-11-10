from rest_framework import serializers

from prints.models import PrintSizeInfo, PrintSize


class PrintSizeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintSizeInfo
        fields = ['base_price_cents', 'ship_price_cents', 'size']

    size = serializers.ChoiceField(
        choices=[ps[1] for ps in PrintSize.choices()]
    )
