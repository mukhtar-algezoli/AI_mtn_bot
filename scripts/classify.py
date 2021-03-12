from transformers import AutoConfig, BertForSequenceClassification, AutoTokenizer, BertTokenizer, PretrainedConfig
from transformers import BertConfig, BertForPreTraining, load_tf_weights_in_bert
from transformers.data.processors import SingleSentenceClassificationProcessor
from transformers import Trainer , TrainingArguments

import numpy as np

from AI_bot.arabert.preprocess_arabert import preprocess, never_split_tokens

trainer = None
tokenizer = None

def load_classification_model():
    global trainer
    global tokenizer
    mod = 'mtn_models/pytorch_model.bin'
    tok = 'mtn_models/vocab.txt'
    conf = 'mtn_models/config.json'
    tokenizer = BertTokenizer.from_pretrained(
        tok,
        do_lower_case=False,
        do_basic_tokenize=True,
        never_split=never_split_tokens, truncation=True)
    config = PretrainedConfig.from_pretrained(conf,num_labels=6)
    model = BertForSequenceClassification.from_pretrained(mod, config=config)

    training_args = TrainingArguments("./train")

    training_args.do_train = True
    training_args.evaluate_during_training = True
    training_args.adam_epsilon = 1e-8
    training_args.learning_rate = 2e-5
    training_args.warmup_steps = 0
    training_args.per_gpu_train_batch_size = 16
    training_args.per_gpu_eval_batch_size = 16
    training_args.num_train_epochs= 3
    #training_args.logging_steps = (len(train_features) - 1) // training_args.per_gpu_train_batch_size + 1
    training_args.save_steps = training_args.logging_steps
    training_args.seed = 42

    trainer = Trainer(model=model,args = training_args)


def fun(sentiment):

    if sentiment == 0 :
        return 'data_offer'

    elif sentiment == 1:
        return 'voice_offers'

    elif sentiment == 2:
        return 'complaint'

    elif sentiment == 3:
        return 'my_sim'

    elif sentiment == 4:
        return 'service_centers'

    else:
        return 'nothing'

def classify_input(text):
  #text = input('enter your text:')
  inf_dataset = SingleSentenceClassificationProcessor(mode='classification')
  inf_dataset.add_examples(texts_or_text_and_labels=[text],overwrite_examples=True)
  #print(inf_dataset.examples)
  max_length = 128
  inf_features = inf_dataset.get_features(tokenizer = tokenizer)
  #with io.capture_output() as captured:
      #preds = trainer.predict(test_dataset=inf_features);
  preds = trainer.predict(test_dataset=inf_features);
  res = fun(np.argmax(preds[0]))
  print(preds[0])
  counter = 0
 # for i in preds[:][0]:
 #   for J in i:
 #      if J > 0:
 #        counter +=1

  print('//////////////////////////////////////')
  if counter > 2 :
    return "others"
  else:
    return res
  print('//////////////////////////////////////')
