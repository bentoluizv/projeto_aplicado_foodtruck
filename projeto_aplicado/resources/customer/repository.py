from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.customer.model import Customer
from projeto_aplicado.resources.customer.schemas import (
    CustomerList,
    UpdateCustomerDTO,
)
from projeto_aplicado.schemas import Pagination


class CustomerRepository:
    """
    Repository for Customer entity.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        Args:
            session (Session): The database session to use.
        """
        self.session = session

    def create(self, customer: Customer) -> str:
        """
        Create a new customer.
        Args:
            customer (Customer): The customer to create.
        Returns:
            str: The ID of the created customer.
        """
        try:
            self.session.add(customer)
            self.session.commit()
            return customer.id
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100) -> CustomerList:
        """
        Get all customers with optional pagination.
        Args:
            offset (int): The offset for pagination.
            limit (int): The maximum number of customers to retrieve.
        Returns:
            CustomerList: A list of customers with pagination information.
        """
        try:
            total_count_stmt = select(func.count()).select_from(Customer)
            total_count = self.session.exec(total_count_stmt).first() or 0
            stmt = select(Customer).offset(offset).limit(limit)
            customers = self.session.exec(stmt).all()
            pagination = Pagination(
                offset=offset,
                limit=limit,
                total_count=total_count,
                page=offset // limit + 1,
                total_pages=(total_count // limit) + 1,
            )
            return CustomerList(customers=customers, pagination=pagination)
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, customer_id: str) -> Customer | None:
        """
        Get a customer by ID.
        Args:
            customer_id (str): The ID of the customer to retrieve.
        Returns:
            Customer | None: The customer with the specified ID, or None if not found.
        """
        try:
            return self.session.get(Customer, customer_id)
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_email(self, email: str) -> Customer | None:
        """
        Get a customer by email.
        Args:
            email (str): The email of the customer to retrieve.
        Returns:
            Customer | None: The customer with the specified email, or None if not found.
        """
        try:
            return self.session.exec(
                select(Customer).where(Customer.email == email)
            ).first()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, customer: Customer, dto: UpdateCustomerDTO) -> str:
        """
        Update a customer.
        Args:
            customer (Customer): The customer to update.
            dto (UpdateCustomerDTO): The data to update the customer with.
        Returns:
            str: The ID of the updated customer.
        """
        try:
            update_data = dto.model_dump(exclude_unset=True)
            customer.sqlmodel_update(update_data)
            self.session.commit()
            self.session.refresh(customer)
            return customer.id
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, customer: Customer) -> str:
        """
        Delete a customer.
        Args:
            customer (Customer): The customer to delete.
        Returns:
            str: The ID of the deleted customer.
        """
        try:
            self.session.delete(customer)
            self.session.commit()
            return customer.id
        except Exception as e:
            self.session.rollback()
            raise e


def get_customer_repository(
    session: Annotated[Session, Depends(get_session)],
) -> CustomerRepository:
    """
    Dependency to get the CustomerRepository.
    Args:
        session (Session): The database session to use.
    Returns:
        CustomerRepository: An instance of the CustomerRepository.
    """
    return CustomerRepository(session)
