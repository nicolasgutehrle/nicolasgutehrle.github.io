import streamlit as st
from joblib import load
import pandas as pd
import time
# ouvrez le terminal Anaconda


@st.cache(suppress_st_warning=True)
def load_file(filepath):
    """Charge le fichier csv et enregistre le DataFrame dans le cache"""
    # st.write("Cache miss: expensive_computation(", filepath, ") ran")

    data = pd.read_csv(filepath)
    return data

def load_model(modelpath):
    """Charge le modele et l'enregistre dans le cache"""
    model = load(modelpath)
    return model

# Définition des paramètres
data_folder = 'data'
model_folder = 'models'
file_list = ['as_train.csv', 'as_dev.csv', 'as_test.csv']
model_list = ['pipe_model.joblib']

### AFFICHAGE SLIDEBAR
st.sidebar.write('# Options')
# Boites de sélection, pour choisir les fichiers et modèles à ouvrir
file_selection = st.sidebar.selectbox('Select file:', file_list)
filepath = "{}/{}".format(data_folder, file_selection)

model_selection = st.sidebar.selectbox('Select a model:', model_list)
modelpath = "{}/{}".format(model_folder, model_selection)


# Chargement des modèles
model = load_model(modelpath)
data = load_file(filepath)


# slider qui permet de séléctionner plus ou moins de données du DataFrame
# dans l'ordre: nombre minimal, nombre maximal, valeur par défaut
slider = st.sidebar.slider('Data size', 0, len(data), len(data))
if slider:
    data = data.iloc[:slider]


### DEBUT AFFICHAGE
st.write('# Amazon Reviews exploration app')

# Affiche le Dataframe
st.write('## Data')
st.dataframe(data, 10000, 500)
# Affiche un diagramme a barres
st.write('## Class distribution')
st.bar_chart(data['targets'].value_counts())

st.write('## Model testing')
# text_input affiche un champ texte
input = st.text_input('Write here:')
if st.button('Classify'):
    if not input:
        st.warning('Please write a sentence here')
        st.stop()
    result = model.predict(['test sentence'])
    st.success('Prediction successful')
    st.write('This sentence is :', result[0])