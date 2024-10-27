#!/usr/bin/env python
# coding: utf-8

# # Exercice 1
# 
# Dans cet exercice, vous allez appliquer les méthodes de Clustering et de Topic Modelling sur la version anglaise du ``amazon_reviews``. Comme dans le cours, vous n'aurez pas besoin de classes, mais seulement des textes. 
# 
# Dans un premier temps, vous vectoriserez vos données textuelles afin qu'elles soient utilisables par l'algorithme. Vous utiliserez ensuite la librairie ``yellowbrick`` pour déterminer le nombre de cluster idéal pour vos données. Vous utiliserez la classe ``MiniBatchKmeans`` comme méthode de clustering. 
# 
# Une fois le nombre de clusters idéal trouvé, vous utiliserez la classe ``Pipeline`` (vue au cours précédent) pour entraîner votre modèle. Votre pipeline contiendra votre vectorizer ainsi que votre modèle de clustering. Vous contrôlerez la qualité de votre modèle, en ayant de classer des données issues du devset ou du testset. Enfin, vous sauvegarderez votre Pipeline sur le disque à l'aide de la libraire ``joblib``.

# In[13]:


#chargement des données avec panda
import pandas as pd 
train = pd.read_json('dataset_en_train.json', lines= True)
dev = pd.read_json('dataset_en_dev.json', lines= True)
test = pd.read_json('dataset_en_test.json', lines= True)


# In[14]:


#Vectorise données textuelles afin qu'elles soient utilisable par algorithme

from sklearn.feature_extraction.text import CountVectorizer 
vectorizer = CountVectorizer()#ici permet de transformer un corpus de texte en vecteurs d'occurrences de mots

#Pour s'assurer que chaque dataset soit traité de la même façon on entraîne le CountVectorizer
data = pd.concat([train['review_body'], dev['review_body'], 
                  test['review_body']])

vectorizer.fit(data) #fonction fit qui permet de s'adapter aux données


# In[15]:


#utilise CountVectorizer pr transformer les données 

X_train= vectorizer.transform(train['review_body'])
y_train =  train['stars']
print("Forme de la matrice :", X_train.shape)

X_dev = vectorizer.transform(dev['review_body'])
y_dev = dev['stars']
print("Forme de la matrice :", X_dev.shape)

X_test = vectorizer.transform(test['review_body'])
y_test = test['stars']
print("Forme de la matrice :", X_test.shape)


# In[16]:


#enlever les mots vides
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS #pas besoin de créer liste de stopWords car présent dans sklearn


data = train['stars']#mon stars correspond à texts
 
tfidf = TfidfVectorizer(stop_words=ENGLISH_STOP_WORDS, max_features=10000)
X = tfidf.fit_transform(data)

X.shape 


# In[5]:


#librairie yellowbrick pour déterminer le nombre de cluster idéal pour mes données 
from yellowbrick.cluster import KElbowVisualizer

model = MiniBatchKMeans() # on initialise le modele que l'on va utiliser


# k est le nombre de cluster
visualizer = KElbowVisualizer(model, k=(3, 20)) #Nombre minimal de cluster qu'on veut qu'il essaye



visualizer.fit(X)
visualizer.show()

"""j'ai eu l'erreur No module named 'sklearn.metrics._classification'
j'ai essayer de télecharger dans l'invite de commande ac "pip3 install -U scikit-learn scipy matplotlib" 
(j'ai trouvé cette commande sur stackoverflow)
mais il a pas réussi à le télecharger il m'a mit erreur"""


# In[ ]:


#Entrainement du modèle avec Pipeline

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from joblib import dump

#Renommer les variables
X_train, y_train = train['review_body'], train['stars'] #je n'ai pas renommer en texts et classes donc c'est review_body & stars
X_dev, y_dev = dev['review_body'], dev['stars']

# Pipeline prend en argument une liste de tuple
# Le 1er element du tuple est le nom de l'objet, le 2nd est l'objet lui-meme
pipe = Pipeline(
    [
     ('vectorizer', KElbowVisualizer(model, k=(3, 20))), # 1ere couche : vectorizer
     ('model_clustering', MiniBatchKMeans()) # Derniere couche : modele
    ]
)

# on entraine le Pipeline comme si l'on entrainait un modele
pipe.fit(X_train, y_train)
score = pipe.score(X_dev, y_dev)
print("Score :", score)


# In[ ]:


#enregistrement de la pipeline sur le disque

from joblib import dump
import os
os.mkdir('pipeline_model')
dump(pipe, 'pipeline_model/model.joblib')


# # Exercice 2
# 
# En utilisant le même dataset, vous utiliserez la librairie ``gensim`` pour entraîner un modèle de Topic Modelling. Vous utiliserez l'algorithme LDA, comme vu en cours. Comme dans le cours, vous écrirez une fonction pour créer une version tokenizée de votre corpus (on gardera les mots vides cette fois). Appuyez vous sur le cours pour appliquer toutes les étapes qui mènent à l'entraînement de LDA.
# 
# Une fois le modèle entraîné, vous afficherez les 10 premiers topics obtenus. Vous utiliserez ensuite votre modèle pour prédire le topic d'un document issu du devset ou du testset.

# In[18]:


# prétraitements de texte avec gensim

def tokenize(data):
    
    new_data = [text.lower() for text in data] # boucle qui remplit une liste
    print(new_data)
    new_data = [text.split() for text in new_data] # tokenize
corpus = tokenize(train['review_body'])

""" j'ai l'erreur suivante qui s'affiche
'IOPub data rate exceeded.
The notebook server will temporarily stop sending output
to the client in order to avoid crashing it.
To change this limit, set the config variable
`--NotebookApp.iopub_data_rate_limit`.

Current values:
NotebookApp.iopub_data_rate_limit=1000000.0 (bytes/sec)
NotebookApp.rate_limit_window=3.0 (secs)'"""


# In[21]:


from gensim.corpora import Dictionary

# Dictionnaire constitue notre vocabulaire, associe un id a chaque token
dictionnaire = Dictionary(corpus)


# In[20]:


# on vectorize notre corpus selon la methode BoW (fréquence d'apparition d'un token)
vec_corpus = [dictionary.doc2bow(doc) for doc in corpus]


# In[22]:


# entraînement de modèle Latent Dirichlet Analysis (LDA)

# prend en entrée le corpus vectorisé + dictionnaire + le nombre de topic à identifier
 
from gensim.models.ldamodel import LdaModel
NUM_TOPICS = 20
lda = LdaModel(corpus=vec_corpus, num_topics=NUM_TOPICS, id2word=dictionary)


# In[ ]:


#affichage des 10 premiers topics obtenus
lda.print_topics(10)


# In[ ]:


#prédiction de topic d'un document issu du devset ou du testset.

# on traite le corpus de dev
dev_texts = tokenize(df_dev['review_body'])
vec_dev = [dictionary.doc2bow(text) for text in dev_texts]

