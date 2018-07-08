from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls) -> tuple:
        return tuple((x.name, x.value) for x in cls)
