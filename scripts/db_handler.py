import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_doc_sim_txt_list(db,data_class):
   sim_txt_list = []
   data_class_collection= db.collection(data_class)
   docs = data_class_collection.stream()

   for doc in docs:
     sim_txt_list.append(doc.to_dict()["sim_txt"])
   return sim_txt_list

def get_doc_with_sim_txt(db,data_class,sim_txt):
    data_class_collection= db.collection(data_class)
    query_ref =data_class_collection.where(u'sim_txt', u'==',sim_txt).get()
    
    return query_ref[0].to_dict()

def get_doc_goto_with_sim_txt(db,data_class,sim_txt):
    data_class_collection= db.collection(data_class)
    query_ref =data_class_collection.where(u'sim_txt', u'==',sim_txt).get()
    print(query_ref[0].to_dict())
    return query_ref[0].to_dict()['go_to']

def get_next_option_with_option_id(db,option_id):
    data_class_collection= db.collection('options')
    query_ref =data_class_collection.where(u'id', u'==',option_id).get()
    return query_ref[0].to_dict()['next_option']

def get_option_text_with_option_id(db,option_id):
        data_class_collection= db.collection('options')
        query_ref =data_class_collection.where(u'id', u'==',option_id).get()
        return query_ref[0].to_dict()['text']

def add_document_to_collection(db,data_class,data):

    db.collection(data_class).document().set(data)
    
    
