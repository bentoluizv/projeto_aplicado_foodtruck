from enum import Enum


class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
