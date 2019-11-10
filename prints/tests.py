from django.test import TestCase

from prints.models import PrintSizeInfo, PrintSize


class TestPrintsModels(TestCase):
    def test_print_size_abbr_small(self):
        size = PrintSize.SMALL
        psi = PrintSizeInfo(size=size)
        self.assertEqual(psi.size_abbr, size.value[0])
