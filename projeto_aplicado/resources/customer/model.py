from sqlmodel import Field, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Customer(SQLModel, table=True):
    """
    Customer model representing a customer in the system.
    """

    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(max_length=80, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True)
    phone: str = Field(max_length=20, nullable=False)
    address: str = Field(max_length=255, nullable=False)

    @classmethod
    def create(cls, dto: 'CreateCustomerDTO'):  # type: ignore  # noqa: F821
        """
        Create a Customer instance from a DTO.
        """
        return cls(**dto.model_dump())
