from __future__ import annotations

from enum import Enum
from typing import Any, List, Tuple, Type

from django.forms.utils import pretty_name


def enum_choices(enum_type: Type[Enum]) -> List[Tuple[Any, str]]:
    """
    Return an `Enum` in a form usable by Django model / form `choices`.
    """
    return [(member.value, pretty_name(member.name)) for member in enum_type]
