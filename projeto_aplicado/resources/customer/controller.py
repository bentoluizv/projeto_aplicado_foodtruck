from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from projeto_aplicado.resources.customer.model import Customer
from projeto_aplicado.resources.customer.repository import (
    CustomerRepository,
    get_customer_repository,
)
from projeto_aplicado.resources.customer.schemas import (
    CreateCustomerDTO,
    CustomerList,
    UpdateCustomerDTO,
)
from projeto_aplicado.schemas import BaseResponse
from projeto_aplicado.settings import get_settings

settings = get_settings()
router = APIRouter(
    tags=['Customer'], prefix=f'{settings.API_PREFIX}/customers'
)


@router.get('/', response_model=CustomerList, status_code=HTTPStatus.OK)
def fetch_customers(
    repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
    offset: int = 0,
    limit: int = 100,
):
    return repository.get_all(offset=offset, limit=limit)


@router.get('/{customer_id}', response_model=Customer)
def fetch_customer_by_id(
    customer_id: str,
    repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    customer = repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Customer with {customer_id} not found',
        )
    return customer


@router.post('/', response_model=BaseResponse, status_code=HTTPStatus.CREATED)
def create_customer(
    dto: CreateCustomerDTO,
    repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    existing_customer = repository.get_by_email(dto.email)
    if existing_customer:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Customer already exists'
        )
    new_customer = Customer.create(dto)
    repository.create(new_customer)
    return BaseResponse(id=new_customer.id, action='created')


@router.patch('/{customer_id}', response_model=BaseResponse)
def update_customer(
    customer_id: str,
    dto: UpdateCustomerDTO,
    repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    existing_customer = repository.get_by_id(customer_id)
    if not existing_customer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Customer not found'
        )
    repository.update(existing_customer, dto)
    return BaseResponse(id=existing_customer.id, action='updated')


@router.delete('/{customer_id}', response_model=BaseResponse)
def delete_customer(
    customer_id: str,
    repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    existing_customer = repository.get_by_id(customer_id)
    if not existing_customer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Customer not found'
        )
    repository.delete(existing_customer)
    return BaseResponse(id=existing_customer.id, action='deleted')
