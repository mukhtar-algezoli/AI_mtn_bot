from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class OrderStatus(str, Enum):
    shopping = 'SHOPPING'
    name = 'GET_NAME'
    phone = 'GET_PHONE'
    delivery_time = 'GET_DELIVERY_TIME'
    payment_method = 'PAYMENT_METHOD'
    await_confirmation = 'AWAIT_CONFIRMATION'


class User(BaseModel):
    id: int
    order_status: OrderStatus = OrderStatus.shopping
    name: Optional[str]
    phone: Optional[str]


class Category(BaseModel):
    id: int
    name: str


class WeightUnit(BaseModel):
    id: int
    title: str


class DeliveryTime(BaseModel):
    id: int
    title: str


class PaymentMethod(str, Enum):
    CASH = "Cash"
    MBOK = "Mbok"
    WALLET = "Wallet"


class Product(BaseModel):
    id: str
    name: str
    image_full_path: str
    category_id: int
    price: float
    available: bool
    weight_unit: WeightUnit


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Option(BaseModel):
    id: str
    type: str
    parent_id: Optional[str]
    title: Optional[str]
    text: Optional[str]
    image_url: Optional[str]
    products: Optional[Dict[str, List[Product]]]


class Selection(BaseModel):
    id: str
    option_id: str
    time: datetime


class Cart(BaseModel):
    items: List[CartItem]


# Facebook Message Format


class ChoicesResponse(BaseModel):
    choices: List[Selection]


class Sender(BaseModel):
    id: int


class PostbackData(BaseModel):
    payload: str


class Message(BaseModel):
    text: str
    quick_reply: Optional[PostbackData]


class MessagingEvent(BaseModel):
    sender: Sender
    message: Optional[Message]
    postback: Optional[PostbackData]


class Event(BaseModel):
    messaging: Optional[List[MessagingEvent]]


class FacebookHookRequest(BaseModel):
    entry: List[Event]