from faust.types import TableT

from schemas import Product

from schemas import ProductFieldsForFiltering


async def check_product_is_blocked(blocked_product_table: TableT, product: Product) -> bool:
    for field in ProductFieldsForFiltering:
        if field.value in blocked_product_table:
            if getattr(product, field.value) in blocked_product_table[field.value]:
                return True
    return False
