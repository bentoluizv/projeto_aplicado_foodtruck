from sqlmodel import SQLModel

from .order.model import Order, OrderItem
from .product.model import Product
from .shared.model import BaseModel
from .users.model import User

__all__ = [
    'Product',
    'Order',
    'OrderItem',
    'User',
    'BaseModel',
    'get_metadata',
]


def get_metadata():
    """
    Returns SQLModel metadata with all models registered.
    This function ensures all models are imported and registered with SQLModel's metadata.
    """  # noqa: E501
    # Import all models to ensure they are registered
    from .order.model import Order, OrderItem  # noqa: F401, PLC0415
    from .product.model import Product  # noqa: F401, PLC0415
    from .shared.model import BaseModel  # noqa: F401, PLC0415
    from .users.model import User  # noqa: F401, PLC0415

    return SQLModel.metadata
