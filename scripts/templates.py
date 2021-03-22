import itertools
import math
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, Iterable, List, Mapping, Sequence

from pymessenger import Button

from crud import get_suboptions
from crud import Database
from schemas import  Option
from payload import *

show_another_rep = False

class QuickReplies:
    @staticmethod
    def phone_number() -> dict:
        return {
                "content_type": "user_phone_number",
                                                }

def _grouper(options: List[Any], limit: int):
    def check(option):
        return options.index(option) // limit
    return check



def menu(db: Database, option: Option):
    options = get_suboptions(db, option)
    quick_replies = []
    buttons = [Button(
        title=option.title,
        type='postback',
        payload=GoToOption(option_id=option.id,).to_json()
    ) for option in options]
    messages = []
    for _, section in itertools.groupby(buttons, _grouper(buttons, 3)):
        message = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': option.title,
                    'buttons': list(section)
                }
            },
        }
        if quick_replies:
            message['quick_replies'] = quick_replies
        messages.append(message)
    return messages


def info(_db: Database, option: Option):
    messages = []
    #print("i am here")
    message = {
        'text': option.text,
        }
    if option.id == "xjq53kisj4rmRZQECD3S":
        message['quick_replies']= [{
                                         "content_type": "text",
                                                                      "title": "+249922838400",
                                                                                                  "payload": 'id'
                                                                                                                                                                             }]
    messages.append(message)
    return messages





