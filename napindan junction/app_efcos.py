import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
#for filling the missing values
from sklearn.impute import SimpleImputer
# Importing the machine learning models
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR

df = pd.read_csv('NapindanJunctionSide_Consolidated_Data.csv')

column = ['RAINFALL', 'TMAX', 'TMIN', 'TMEAN', 'WIND_SPEED', 'WIND_DIRECTION', 'FLOOD_HEIGHT_LOWEST', 'FLOOD__HEIGHT_AVE']

X = df.drop(['FLOOD_HEIGHT_HIGHEST'], axis=1)
y= df['FLOOD_HEIGHT_HIGHEST']

st.write("""
# Metro Manila River Flood Prediction App for Napindan Junction
""")

st.sidebar.header('User Input Features')


def user_input_features():
    RAINFALL = st.sidebar.number_input('Rainfall (mm)', min_value=float(X.RAINFALL.min()),value=float(X.RAINFALL.mean()))
    TMAX = st.sidebar.number_input('Tmax (Celsius °C)', min_value=float(X.TMAX.min()),value=float(X.TMAX.mean()))
    TMIN = st.sidebar.number_input('Tmin (Celsius °C)', min_value=float(X.TMIN.min()),value=float(X.TMIN.mean()))
    TMEAN = st.sidebar.number_input('Tmean (Celsius °C)', min_value=float(X.TMEAN.min()),value=float(X.TMEAN.mean()))
    WIND_SPEED = st.sidebar.number_input('Wind speed (m/s)', min_value=float(X.WIND_SPEED.min()),value=2.0)
    WIND_DIRECTION = st.sidebar.number_input('Wind direction (degrees)', min_value=float(X.WIND_DIRECTION.min()),value=180.0)
    FLOOD_HEIGHT_LOWEST = st.sidebar.number_input('Flood Height Lowest (EL.m)', min_value=float(X.FLOOD_HEIGHT_LOWEST.min()),value=float(X.FLOOD_HEIGHT_LOWEST.mean()))
    FLOOD__HEIGHT_AVE = st.sidebar.number_input('Flood Height Average (EL.m)',min_value=float(X.FLOOD__HEIGHT_AVE.min()),value=float(X.FLOOD__HEIGHT_AVE.mean()))

    data = {
            'RAINFALL (mm)': RAINFALL,
            'TMAX (Celsius °C)': TMAX,
            'TMIN (Celsius °C)': TMIN,
            'TMEAN (Celsius °C)': TMEAN,
            'WIND_SPEED (m/s)': WIND_SPEED,
            'WIND_DIRECTION (degrees)': WIND_DIRECTION,
            'FLOOD_HEIGHT_LOWEST (EL.m)': FLOOD_HEIGHT_LOWEST,
            'FLOOD__HEIGHT_AVE (EL.m)': FLOOD__HEIGHT_AVE,
            }


    features = pd.DataFrame(data, index=[0])
    return features

# Displays the user input features
user_features = user_input_features()
st.subheader('User Input features')
st.write(user_features)
#
# ## Load StandardScaler
load_sclaer = pickle.load(open('standscaler.pkl', 'rb'))

user_features_scaler = load_sclaer.transform(user_features)
df_features = pd.DataFrame(user_features_scaler, columns=column)

#
# Reads in random forest model
load_clf_rf = pickle.load(open('rf_prediction.pkl', 'rb'))

# Apply model to make predictions
RF_prediction = load_clf_rf.predict(df_features)
st.subheader('Prediction Probability for RF')
st.write(RF_prediction)

# Reads in Support vector machine model
load_clf_SVR = pickle.load(open('SVR_prediction.pkl', 'rb'))

# Apply model to make predictions
SVR_prediction = load_clf_SVR.predict(df_features)
st.subheader('Prediction Probability for SVR')
st.write(SVR_prediction)

# Reads in Artificial Neural Network model
load_clf_ANN = pickle.load(open('ANN_prediction.pkl', 'rb'))

# Apply model to make predictions
ANN_prediction = load_clf_ANN.predict(df_features)
st.subheader('Prediction Probability for ANN')
st.write(ANN_prediction)

st.write("water level basis")
image = Image.open('napindanjunction.png')
st.image(image, '')