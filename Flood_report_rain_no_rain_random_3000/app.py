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

df = pd.read_csv('Flood_report_rain_no_rain_random_3000.csv')

column = ['YEAR', 'MONTH', 'DAY', 'RAINFALL', 'TMAX', 'TMIN', 'TMEAN', 'WIND_SPEED', 'WIND_DIRECTION', 'ELEVATION', 'SLOPE']

X = df.drop(['FLOOD_HEIGHT'], axis=1)
y= df['FLOOD_HEIGHT']

st.write("""
# Metro Manila River Flood Prediction App
""")

st.sidebar.header('User Input Features')


def user_input_features():
    YEAR = st.sidebar.number_input('Year', X.YEAR.min(),X.YEAR.max(),2013)
    MONTH = st.sidebar.number_input('Month', X.MONTH.min(),X.MONTH.max(),6)
    DAY = st.sidebar.number_input('Day', X.DAY.min(),X.DAY.max(),15)
    RAINFALL = st.sidebar.number_input('Rainfall', min_value=float(X.RAINFALL.min()),value=float(X.RAINFALL.mean()))
    TMAX = st.sidebar.number_input('Tmax', min_value=float(X.TMAX.min()),value=float(X.TMAX.mean()))
    TMIN = st.sidebar.number_input('Tmin', min_value=float(X.TMIN.min()),value=float(X.TMIN.mean()))
    TMEAN = st.sidebar.number_input('Tmean', min_value=float(X.TMEAN.min()),value=float(X.TMEAN.mean()))
    WIND_SPEED = st.sidebar.number_input('Wind speed', min_value=float(X.WIND_SPEED.min()),value=2.0)
    WIND_DIRECTION = st.sidebar.number_input('Wind direction', min_value=float(X.WIND_DIRECTION.min()),value=180.0)
    ELEVATION = st.sidebar.number_input('Flood Height Lowest', min_value=float(X.ELEVATION.min()),value=float(X.ELEVATION.mean()))
    SLOPE = st.sidebar.number_input('Flood Height Average',min_value=float(X.SLOPE.min()),value=float(X.SLOPE.mean()))

    data = {
            'YEAR': YEAR,
            'MONTH': MONTH,
            'DAY': DAY,
            'RAINFALL': RAINFALL,
            'TMAX': TMAX,
            'TMIN': TMIN,
            'TMEAN': TMEAN,
            'WIND_SPEED': WIND_SPEED,
            'WIND_DIRECTION': WIND_DIRECTION,
            'ELEVATION': ELEVATION,
            'SLOPE': SLOPE,
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
