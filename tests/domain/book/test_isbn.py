import dataclasses

import pytest

from dddpy.domain.book import Isbn


class TestIsbn:
    @pytest.mark.parametrize(
        "value",
        [
            ("978-0321125217"),
            ("978-4-949999-12-0"),
        ],
    )
    def test_constructor_should_create_instance(self, value):
        isbn = Isbn(value)

        assert isbn.value == value

    @pytest.mark.parametrize(
        "value",
        [
            ("invalid-string"),
            ("123456789"),
            ("000-0141983479"),
        ],
    )
    def test_constructor_should_throw_value_error_when_params_are_invalid(self, value):
        with pytest.raises(ValueError):
            Isbn(value)

    def test_isbn_should_be_frozen(self):
        with pytest.raises(dataclasses.FrozenInstanceError):
            isbn = Isbn("978-0321125217")
            isbn.value = "978-1141983479"  # type: ignore
