import pandas as pd
import numpy as np

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import LSTM, RepeatVector, TimeDistributed, Dense
import keras.backend as K 
def root_mean_squared_error(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true))) 

from pickle import load
import joblib

################# auto encoder 실행

ae_data = pd.read_csv('../pre_res/ae_pre.csv')
ae_model = tf.keras.models.load_model('../ref/ae_model.hdf5', custom_objects={'root_mean_squared_error': root_mean_squared_error})
pred = ae_model.predict(ae_data).reshape(ae_data.shape[0],)

print(pred)



################# classification model 실행
cla_data  = pd.read_csv('../pre_res/rate_df.csv')
cla_model = joblib.load(('../ref/rfmodel.pkl'))

result = cla_model.predict(cla_data)
if result == 0:
    print('정상')
else:
    print('tool 부러짐')