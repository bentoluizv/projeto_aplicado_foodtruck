from sqlmodel import Field

from projeto_aplicado.resources.shared.model import BaseModel


class Product(BaseModel, table=True):
    """
    Product model representing a product in the system.
    """

    name: str = Field(max_length=80, index=True, nullable=False)
    description: str | None = Field(
        default=None, max_length=255, nullable=True
    )
    price: float = Field(nullable=False, gt=0.0)

    @classmethod
    def create(cls, dto: 'CreateProductDTO'):  # type: ignore  # noqa: F821
        """
        Create a Product instance from a DTO.
        """
        return cls(**dto.model_dump())
