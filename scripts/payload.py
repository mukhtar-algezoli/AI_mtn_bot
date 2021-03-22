import json
from dataclasses import field
from enum import Enum

from pydantic import BaseModel
from pydantic.json import pydantic_encoder



class Actions(str, Enum):
    main_menu = "MAIN_MENU"
    go_to_option = "GO_TO_OPTION"
    order_menu = "ORDER_MENU"
    show_product_list = "SHOW_PRODUCT_LIST"
    modify_cart = "MODIFY_CART"
    show_cart = "SHOW_CART"
    start_ordering = "START_ORDERING"
    orderer_name = "ORDER_NAME"
    orderer_phone = "ORDER_PHONE"
    order_delivery_time = "ORDER_DELIVERY_TIME"
    order_payment = "ORDER_PAYMENT"
    confirm_order = "CONFIRM_ORDER"
    cancel_order = "CANCEL_ORDER"


class CartOperations(str, Enum):
    Add = 'ADD'
    Subtract = 'SUBTRACT'


class BasePayload(BaseModel):
    action: Actions

    def to_json(self) -> str:
        return json.dumps(self, default=pydantic_encoder)


class MainMenu(BasePayload):
    action: Actions = Actions.main_menu


class GoToOption(BasePayload):
    action: Actions = Actions.go_to_option
    option_id: str
