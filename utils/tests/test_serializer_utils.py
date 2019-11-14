from django.test import TestCase
from enumfields import Enum

from utils.serializer_utils import enum_from_str


class TestSerializerUtils(TestCase):
    class TestEnum(Enum):
        FIRST = "FIRST"
        SECOND = "SECOND"

    def test_enum_from_str_good_data(self):
        errors_list = []
        enum_val = self.TestEnum.FIRST.value

        result = enum_from_str(enum_val, self.TestEnum, errors_list)

        self.assertIsInstance(result, self.TestEnum)
        self.assertEqual(result.value, enum_val)
        self.assertEqual(len(errors_list), 0)

    def test_enum_from_str_bad_data(self):
        errors_list = []
        enum_val = "BAD_VALUE"

        result = enum_from_str(enum_val, self.TestEnum, errors_list)

        self.assertIsNone(result)
        self.assertEqual(len(errors_list), 1)
