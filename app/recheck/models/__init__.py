from .book import Book
from .publisher import Publisher
from .member import Member
from .supplier import Supplier
from .order import Order
from .order_item import OrderItem
from .purchase import Purchase
from .purchase_item import PurchaseItem
from .shipping import Shipping
from .shipping_item import ShippingItem
from sqlalchemy.orm import configure_mappers
configure_mappers()