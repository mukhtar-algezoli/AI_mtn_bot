import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample, losses, util, SentencesDataset
from torch.utils.data import DataLoader
from db_handler import *

sim_model = None
df_AJGT = None
class1= None 
class2= None
class3= None
class4= None
class5= None
v = None
embeddings2 = None
class6= None
class7= None
class8= None
class9= None
class10= None
v2 = None
embeddings3 = None

def load_model(t):
  global sim_model
  sim_model = SentenceTransformer(t)

def load_data(t):
  global df_AJGT
  df_AJGT = pd.read_csv(t,header=0)
  df_AJGT = df_AJGT.iloc[1:]

  DATA_COLUMN = 'text'
  LABEL_COLUMN = 'label'

  df_AJGT = df_AJGT[['text', 'label']]
  df_AJGT.columns = [DATA_COLUMN, LABEL_COLUMN]

  label_map = {
      'data_offer' : 0,
      'voice_offers' : 1,
      'complaint' : 2,
      'service_center' : 3,
      'service_centers' : 3,
      'my_sim' : 4
  }

  df_AJGT = df_AJGT.dropna()
  df_AJGT[LABEL_COLUMN] = df_AJGT[LABEL_COLUMN].apply(lambda x: label_map[x])
###############################################
def cal_embeddings_classify():
        global class1, class2, class3, class4, class5, classes,embeddings2, v
        class1 = list(df_AJGT.loc[df_AJGT['label'] == 0]['text'])
        class2 = list(df_AJGT.loc[df_AJGT['label'] == 1]['text'])
        class3 = list(df_AJGT.loc[df_AJGT['label'] == 2]['text'])
        class4 = list(df_AJGT.loc[df_AJGT['label'] == 3]['text'])      
        class5 = list(df_AJGT.loc[df_AJGT['label'] == 4]['text'])
                          
        v = {}          
        v[0] = class1             
        v[1] = class2               
        v[2] = class3                 
        v[3] = class4                   
        v[4] = class5

        classes = v[0]+v[1]+v[2]+v[3]+v[4]
        embeddings2 = sim_model.encode(classes, convert_to_tensor=True)
##############################################
def cal_embeddings_sim(db):
  global class6, class7, class8, class9, class10, classes2,embeddings3, v2
  class6 = get_doc_sim_txt_list(db,'data_offer')
 # class1 = list(df_AJGT.loc[df_AJGT['label'] == 0]['text'])
  class7 = get_doc_sim_txt_list(db,'voice_offers')
 # class2 = list(df_AJGT.loc[df_AJGT['label'] == 1]['text'])
  class8 = get_doc_sim_txt_list(db,'complaints')
  # class3 = list(df_AJGT.loc[df_AJGT['label'] == 2]['text'])
  class9 = get_doc_sim_txt_list(db,'service_centers')
  #class4 = list(df_AJGT.loc[df_AJGT['label'] == 3]['text'])
  class10 = get_doc_sim_txt_list(db,'my_sim')
  #class5 = list(df_AJGT.loc[df_AJGT['label'] == 4]['text'])

  v2 = {}
  v2[0] = class6
  v2[1] = class7
  v2[2] = class8
  v2[3] = class9
  v2[4] = class10

  classes2 = v2[0]+v2[1]+v2[2]+v2[3]+v2[4]

  #Compute embeddings
  embeddings3 = sim_model.encode(classes2, convert_to_tensor=True)
#################################################################
def compare_classify(t):
  sentences = [t]
  embeddings = sim_model.encode(sentences, convert_to_tensor=True)

  cosine_scores = util.pytorch_cos_sim(embeddings, embeddings2)
  euclidena_dist = len(embeddings)*[len(embeddings2)*[0]]
  for i in range(len(embeddings)):
    for j in range(len(embeddings2)):
      euclidena_dist[i][j] = sum(((embeddings[i] - embeddings2[j])**2).reshape(768))


  #Find the pairs with the highest cosine similarity scores
  pairs = []
  for i in range(len(cosine_scores)):
      for j in range(len(cosine_scores[0])):
          pairs.append({'index': [i, j], 'score': cosine_scores[i][j], 'score2': euclidena_dist[i][j]})

  #Sort scores in decreasing order
  pairs = sorted(pairs, key=lambda x: x['score2'])

  for pair in pairs[:1]:
     i, j = pair['index']
     for k in range(len(v)):
        if classes[j] in v[k]:
          break
    # print(k)
     return "{}\t \t{}\t Score: {:.4f}\t Score2: {:.4f}".format(sentences[i], classes[j], pair['score'], pair['score2']),k, sentences[i]
######################################################################
def compare_sim(t):
  sentences2 = [t]
  embeddings5 = sim_model.encode(sentences2, convert_to_tensor=True)

  cosine_scores = util.pytorch_cos_sim(embeddings5, embeddings3)
  euclidena_dist = len(embeddings5)*[len(embeddings3)*[0]]
  for i in range(len(embeddings5)):
    for j in range(len(embeddings3)):
      euclidena_dist[i][j] = sum(((embeddings5[i] - embeddings3[j])**2).reshape(768))


  #Find the pairs with the highest cosine similarity scores
  pairs = []
  for i in range(len(cosine_scores)):
      for j in range(len(cosine_scores[0])):
          pairs.append({'index': [i, j], 'score': cosine_scores[i][j], 'score2': euclidena_dist[i][j]})

  #Sort scores in decreasing order
  pairs = sorted(pairs, key=lambda x: x['score2'])

  for pair in pairs[:1]:
     i, j = pair['index']
     for k in range(len(v2)):
        if classes2[j] in v2[k]:
          break
     print(k)
     print(classes2[j])
     print(sentences2[i])
     return "{}\t \t{}\t Score: {:.4f}\t Score2: {:.4f}".format(sentences2[i], classes2[j], pair['score'], pair['score2']),k ,classes2[j]


