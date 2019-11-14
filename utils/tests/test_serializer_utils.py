from unittest import mock

from django.test import TestCase
from enumfields import Enum

from utils.models import TestModel
from utils.serializer_utils import (enum_from_str, check_str_length,
                                    check_numeric_string)


class TestSerializerUtils(TestCase):
    class TestEnum(Enum):
        FIRST = "FIRST"
        SECOND = "SECOND"

    def test_enum_from_str_good_value(self):
        errors_list = []
        enum_val = self.TestEnum.FIRST.value

        result = enum_from_str(enum_val, self.TestEnum, errors_list)

        self.assertIsInstance(result, self.TestEnum)
        self.assertEqual(result.value, enum_val)
        self.assertEqual(len(errors_list), 0)

    def test_enum_from_str_bad_value(self):
        errors_list = []
        enum_val = "BAD_VALUE"

        result = enum_from_str(enum_val, self.TestEnum, errors_list)

        self.assertIsNone(result)
        self.assertEqual(len(errors_list), 1)

    def good_str_length_check(self, test_str: str):
        model = TestModel
        field = "numeric_str"
        errors_list = []

        result = check_str_length(test_str, model, field, errors_list)

        self.assertEqual(test_str, result)
        self.assertEqual(len(errors_list), 0)

    def test_check_str_length_good_values(self):
        exact_str = "abcde"
        short_str = "abc"
        self.good_str_length_check(exact_str)
        self.good_str_length_check(short_str)

    def bad_str_length_check(self, test_str):
        model = TestModel
        field = "numeric_str"
        errors_list = []

        result = check_str_length(test_str, model, field, errors_list)

        self.assertIsNone(result)
        self.assertEqual(len(errors_list), 1)

    def test_check_str_length_bad_values(self):
        long_str = "abcdef"
        empty_str = ""
        self.bad_str_length_check(long_str)
        self.bad_str_length_check(empty_str)

    def test_check_numeric_str_good_value(self):
        good_value = "12345"
        model = TestModel
        field = "numeric_str"
        errors_list = []

        mock_len_check = "utils.serializer_utils.check_str_length"
        with mock.patch(mock_len_check) as mocked:
            mocked.return_value = good_value

            result = check_numeric_string(good_value, model,
                                          field, errors_list)

            mocked.assert_called_with(good_value, model, field, errors_list)
            self.assertEqual(result, good_value)
            self.assertEqual(len(errors_list), 0)

    def test_check_numeric_str_bad_value(self):
        bad_value = "abcdef"
        model = TestModel
        field = "numeric_str"
        errors_list = []

        mock_len_check = "utils.serializer_utils.check_str_length"
        with mock.patch(mock_len_check) as mocked:
            mocked.return_value = bad_value
            mocked.side_effect = lambda *x: x[3].append("error msg")

            result = check_numeric_string(bad_value, model,
                                          field, errors_list)

            mocked.assert_called_with(bad_value, model, field, errors_list)
            self.assertIsNone(result)
            self.assertEqual(len(errors_list), 2)
