from typing import Type, Optional, List

from django.db import models
from enumfields import Enum


def enum_from_str(str_name: str, enumeration: Type[Enum],
                  errors_list: List[str], ) -> Optional[Enum]:
    """
    Return the enum value named by str_name for enumeration, if str_name is
    valid.  Otherwise add error message to errors_list and return None

    SIDE-EFFECT: possibly update errors_list
    """
    result = None
    try:
        result = enumeration[str_name.upper()]
    except KeyError:
        errors_list.append(f"No {enumeration.__name__} found for {str_name}")
    return result


def check_numeric_string(to_check: str, model: Type[models.Model],
                         field_name: str, errors_list: List[str]) -> Optional[str]:
    """
    Return to_check if it contains only digits and its length does not
    exceed the max_length defined for model.field_name. Otherwise add error
    message to errors_list and return None

    SIDE-EFFECT: possibly update errors_list
    """
    good_length = check_str_length(to_check, model, field_name, errors_list)
    if to_check.isdigit() and good_length:
        return to_check
    else:
        errors_list.append(f"{field_name} {to_check} must be numeric")
        return None


def check_str_length(to_check: str, model: Type[models.Model],
                     field_name: str, errors_list: List[str], ) -> Optional[str]:
    """
    Return to_check if it does not exceed the max_length defined for
    model.field_name. Otherwise add error message to errors_list
    and return None

    SIDE-EFFECT: possibly update errors_list
    """
    max_len = model._meta.get_field(field_name).max_length
    if to_check and len(to_check) <= max_len:
        return to_check
    elif not to_check:
        errors_list.append(f"{field_name} cannot be empty")
    else:
        errors_list.append(f"{field_name} \"{to_check}\" may have at most "
                           f"{max_len} characters")
