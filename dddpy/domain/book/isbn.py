import re
from dataclasses import dataclass

regex = r"978[-0-9]{10,15}"
pattern = re.compile(regex)


@dataclass(init=False, eq=True, frozen=True)
class Isbn:
    """Isbn represents an ISBN code as a value object"""

    value: str

    def __init__(self, value: str):
        if pattern.match(value) is None:
            raise ValueError("isbn should be a valid format.")

        object.__setattr__(self, "value", value)
