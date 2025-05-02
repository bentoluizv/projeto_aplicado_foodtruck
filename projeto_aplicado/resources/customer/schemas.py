from sqlmodel import SQLModel


class CreateCustomerDTO(SQLModel):
    name: str
    email: str
