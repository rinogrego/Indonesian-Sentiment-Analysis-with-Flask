from tensorflow.keras.layers import Input
from tensorflow.keras.models import load_model, Model
from transformers import TFAutoModel
from numpy import int32

import gc

# load pretrained indobert that have been saved locally
bert_model = TFAutoModel.from_pretrained("model/indobert-lite-large-p2", trainable=False)
# build model
input_token = Input(shape=(128,), dtype=int32, name="input_token")
input_mask = Input(shape=(128,), dtype=int32, name="input_mask")
bert_embedding = bert_model([input_token, input_mask])[0]
## lstm-cnn.h5 contains trained layers that have been extracted right after the bert_embedding layer
lstm_cnn_dense_model = load_model('model/lstm-cnn.h5', compile=False)(bert_embedding)

model = Model(inputs=[input_token, input_mask], outputs=lstm_cnn_dense_model)

del bert_model, input_token, input_mask, bert_embedding, lstm_cnn_dense_model
gc.collect()

# more straightforward code for loading the pretrained model, but more costly in memory
# bert_model = TFAutoModel.from_pretrained("model/indobert-lite-large-p2", trainable=False)
# model = tf.keras.models.load_model(
#     'model/indobert-lite-large-p2/bert-lite-large-lstm-cnn.h5', 
#     compile=False, 
#     custom_objects={'TFAlbertModel': bert_model}
# )