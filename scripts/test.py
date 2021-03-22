import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from db_handler import *
from csv import reader

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "serious-cabinet-282523",
})

db = firestore.client()
#get_doc_sim_txt_list(db,'complaints')
#print(get_doc_sim_txt_list(db,'complaints'))
#print(get_doc_with_sim_txt(db,"complaints",' شبكه النت كعبه شديد    '))
#print(get_doc_goto_with_sim_txt(db,"complaints",' شبكه النت كعبه شديد    '))


data = {
    u'sim_txt': u'Los Angeles',
    u'go_to': u'CA'
    }


def add_data(sim, res, cat):
    
    new_city_ref = db.collection('options').document()
    data = {
                u'id': str(new_city_ref.id),
                    u'text': res,
                    u'type': "info"
                        }
    new_city_ref.set(data)
    data = {
                              u'sim_txt':sim ,
                              u'go_to': new_city_ref.id
                                                }
    add_document_to_collection(db,cat,data)



def add_data_from_csv():
  with open('./Top25.csv', 'r',encoding='utf-8') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        print(row)
        data = {
          u'sim_txt': row[3],
          u'go_to': u'CA'
        }
        add_document_to_collection(db,'complaints',data)
        data = {
          u'sim_txt': row[2],
          u'go_to': u'CA'
        }
        add_document_to_collection(db,'voice_offers',data)
        data = {
          u'sim_txt': row[1],
          u'go_to': u'CA'
        }
        add_document_to_collection(db,'data_offer',data)
        data = {
          u'sim_txt': row[4],
          u'go_to': u'CA'
        }
        add_document_to_collection(db,'service_centers',data)
        data = {
          u'sim_txt': row[5],
          u'go_to': u'CA'
        }
        add_document_to_collection(db,'my_sim',data)
        
#add_document_to_collection(db,'complaints',data)
