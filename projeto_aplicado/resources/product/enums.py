from enum import Enum


class ProductCategory(str, Enum):
    FOOD = 'FOOD'
    DRINK = 'DRINK'
    DESSERT = 'DESSERT'
    SNACK = 'SNACK'
