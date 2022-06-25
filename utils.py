import re
import numpy as np
import pandas as pd

import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel


""" TEXT PREPROCESSING """

kamus_alay = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')

# dictionary to map incorrect word with corresponding correct word
nor_dict = {}
for index, row in kamus_alay.iterrows():
    if row[0] not in nor_dict:
        nor_dict[row[0]] = row[1]


# text cleaning
def clean_text(tweet):
    # Mengubah semua huruf menjadi huruf kecil
    tweet = tweet.lower()
    # Menghapus www.* atau https?://*
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    # Menghapus @username
    tweet = re.sub('@[^\s]+','',tweet)
    # Menghapus tanda #
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # Menghapus tanda baca
    tweet = re.sub(r'[^\w\s]',' ', tweet)
    # Menghapus angka
    tweet = re.sub(r'[\d-]', '', tweet)
    # Menghapus spasi berlebih
    tweet = re.sub('[\s]+', ' ', tweet)
    # Menghapus tanda \, ', dan "
    tweet = tweet.strip('\'"')
    
    # Pembersihan kata
    words = tweet.split()
    tokens=[]
    for ww in words:
        # Memisahkan kata berulang
        for w in re.split(r'[-/\s]\s*', ww):
            # Menghapus huruf berulang yang lebih dari dua kali
            pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
            w = pattern.sub(r"\1\1", w)
            w = w.strip('\'"?,.')
            # Memeriksa apakah suatu kata terbentuk dari minimal dua huruf
            val = re.search(r"^[a-zA-Z][a-zA-Z][a-zA-Z]*$", w)
            if w in nor_dict:
                w = nor_dict[w]

            if w == "rt" or val is None:
                continue
            else:
                tokens.append(w.lower())
    
    tweet = " ".join(tokens)  
    return tweet


# tokenization
bert_tokenizer = AutoTokenizer.from_pretrained("model/tokenizer")

def tokenisasi(teks):
      encode_dict = bert_tokenizer(teks,
                                   add_special_tokens = True,
                                   max_length = 128, #maximum token per kalimat = 125
                                   padding = 'max_length',
                                   truncation = True,
                                   return_attention_mask = True,
                                   return_tensors = 'tf',)

      tokenID = encode_dict['input_ids']
      attention_mask = encode_dict['attention_mask']

      return tokenID, attention_mask
  

# Pendefinisian fungsi untuk mengambil hasil tokenisasi pada semua data
def create_input(text):
    tokenID, input_mask = [], []
    
    token, mask = tokenisasi(text)
    tokenID.append(token)
    input_mask.append(mask)
    
    return [np.asarray(tokenID, dtype=np.int32).reshape(-1, 128), 
            np.asarray(input_mask, dtype=np.int32).reshape(-1, 128)]
    

    
""" MODEL """

bert_model = TFAutoModel.from_pretrained("indobenchmark/indobert-lite-large-p2", trainable=False)

input_token = tf.keras.layers.Input(shape=(128,), dtype=np.int32, name="input_token")
input_mask = tf.keras.layers.Input(shape=(128,), dtype=np.int32, name="input_mask")
bert_embedding = bert_model([input_token, input_mask])[0]
lstm_cnn_dense_model = tf.keras.models.load_model('model/lstm-cnn.h5', compile=False)(bert_embedding)
model = tf.keras.models.Model(inputs=[input_token, input_mask], outputs=lstm_cnn_dense_model)
    