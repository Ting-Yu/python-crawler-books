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
from .cart import Cart
from .next import Next
from .stock_history import StockHistory
from .stock_item import StockItem
from .stock import Stock
from .sales_return import SalesReturn
from .sales_return_item import SalesReturnItem
from .sales_return_shipping import SalesReturnShipping
from .sales_return_defective import SalesReturnDefective
from sqlalchemy.orm import configure_mappers

configure_mappers()
