import re
from numpy import asarray, int32
from pandas import read_csv

from tensorflow.keras.layers import Input
from tensorflow.keras.models import load_model, Model
from transformers import AutoTokenizer, TFAutoModel

import matplotlib.pyplot as plt
import io, base64

import gc



""" TEXT PREPROCESSING """

kamus_alay = read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')

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
def create_input(text_list):
    tokenID, input_mask = [], []
    
    for teks in text_list:
        token, mask = tokenisasi(teks)
        tokenID.append(token)
        input_mask.append(mask)
    
    return [asarray(tokenID, dtype=int32).reshape(-1, 128), 
            asarray(input_mask, dtype=int32).reshape(-1, 128)]
    

    
""" MODEL """

# load pretrained indobert that have been saved locally
def get_model():
    bert_model = TFAutoModel.from_pretrained("model/indobert-lite-large-p2", trainable=False)
    # build model
    input_token = Input(shape=(128,), dtype=int32, name="input_token")
    input_mask = Input(shape=(128,), dtype=int32, name="input_mask")
    bert_embedding = bert_model([input_token, input_mask])[0]
    ## lstm-cnn.h5 contains trained layers that have been extracted right after the bert_embedding layer
    lstm_cnn_dense_model = load_model('model/lstm-cnn.h5', compile=False)(bert_embedding)
    model = Model(inputs=[input_token, input_mask], outputs=lstm_cnn_dense_model)

    return model

# more straightforward code for loading the pretrained model, but more costly in memory
# bert_model = TFAutoModel.from_pretrained("model/indobert-lite-large-p2", trainable=False)
# model = tf.keras.models.load_model(
#     'model/indobert-lite-large-p2/bert-lite-large-lstm-cnn.h5', 
#     compile=False, 
#     custom_objects={'TFAlbertModel': bert_model}
# )



""" PLOTTING """

def plot_sentiment(sentiment_results):
    # initialize figure
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    
    # draw the results
    plt.bar(
        x = ["Senang", "Neutral", "Kecewa", "Saran", "Penasaran", "Komplain"],
        height = sentiment_results,
        color = ["green", "gray", "red", "lightgreen", "gold", "darkred"]
    )
    
    # configure plot label
    plt.xlabel("Sentimen")
    plt.ylabel("Skor Sentimen")
  
    # adjusts the size of the chart to the size of the figure
    plt.tight_layout()
    
    # get the stream data
    chart = get_graph()
    
    return chart


def get_graph():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph