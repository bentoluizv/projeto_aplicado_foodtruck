from sqlmodel import Field, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Product(SQLModel, table=True):
    """
    Product model representing a product in the system.
    """

    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=80, index=True, nullable=False)
    description: str | None = Field(
        default=None, max_length=255, nullable=True
    )
    price: float = Field(nullable=False, gt=0.0)
    image_url: str = Field(nullable=False, max_length=255)
    category_id: str = Field(foreign_key='category.id', nullable=False)

    @classmethod
    def create(cls, dto: 'CreateProductDTO'):  # type: ignore  # noqa: F821
        """
        Create a Product instance from a DTO.
        """
        return cls(**dto.model_dump())
