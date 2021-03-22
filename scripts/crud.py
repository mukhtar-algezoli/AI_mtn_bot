from google.cloud import firestore
from typing import Optional, List, Tuple
from datetime import datetime

from schemas import Option
Database = firestore.AsyncClient



def get_option(db: Database, option_id: str):
    option = db.document('options', option_id).get()
    if option.exists:
        data = option.to_dict()
        categories = db.collection('options', option_id, 'items')
        data['items'] = {
            category.get('name'): [
                {
                    **item.to_dict(),
                    'id': item.id
                }
                for item in category.reference.collection('items').stream()
            ]
            for category in categories.stream()
        }
        return Option.parse_obj(data)


def get_root_option(db: Database):
    options = db.collection('options').where('parent_id', '==', None).get()
    return Option.parse_obj(options[0].to_dict())


def get_suboptions(db: Database, parent: Option):
    suboptions = db.collection('options').where('parent_id', '==', parent.id).get()
    return [Option.parse_obj(suboption.to_dict())
            for suboption in suboptions]


