from pydantic import BaseModel, Field, validator


class BookCreateModel(BaseModel):
    """BookCreateModel represents a write model to create a book."""

    isbn: str = Field(example="978-0321125217")
    title: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
    )
    page: int = Field(ge=0, example=320)


class BookUpdateModel(BaseModel):
    """BookUpdateModel represents a write model to update a book."""

    title: str = Field(
        example="Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
    )
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)

    @validator("read_page")
    def _validate_read_page(cls, v, values, **kwargs):
        if "page" in values and v > values["page"]:
            raise ValueError(
                "read_page must be between 0 and {}".format(values["page"])
            )
        return v
