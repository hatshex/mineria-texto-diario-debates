# -*- coding: utf-8 -*-
"""
Created on Thu May 12 23:24:54 2016

@author: stuka

"""

import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
import os
import io
import re
from collections import defaultdict
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math
import pandas as pd
import sys
import gensim
from string import punctuation
#Cleaning the house
os.getcwd()
os.chdir("/home/stuka/itam2/textmining/mineria-texto-diario-debates/data/raw/")
os.listdir(".")

#Debe venir de fuera
"""
Christian - pon tu path local en path_to_raw
Mete manualmente archivos a una carpeta_christian y corre este codigo
file_names = [f for f in os.listdir(path_to_raw+'carpeta_christian/') if f.endswith('.txt')]
documentos =[io.open(f,'rt') for f in file_names]


"""
path_to_raw = "/home/stuka/itam2/textmining/mineria-texto-diario-debates/data/"

file_names = [f for f in os.listdir(path_to_raw+'raw/') if f.endswith('.txt')]

documentos =[io.open(f,'rt',encoding='ISO-8859-1') for f in file_names]


for file_name in file_names:
    sourceEncoding = "iso-8859-1"
    targetEncoding = "utf-8"
    source = io.open(file_name,'rt',encoding='ISO-8859-1')
    target = open(path_to_raw+'encoded/'+file_name, "w")
    target.write(source.read().encode(targetEncoding))
    
documentos =[io.open(path_to_raw+'encoded/'+f,'rt') for f in file_names]

#Pruebas
raw = documentos[0].read()

documentos[1]

dir(data[0])
data[0].name
#Codigo para probar stopterm
for documento in documentos:
    print(len(documento.read().replace("Honorable Asamblea:","Honorable asamblea:").split("Honorable asamblea:")))
    
    
#Este es el buen codigo
"""
documento trae un file abierto
lo consumo a memoria con read() a un solo string
lo parto segun keyterms = Honorable asamblea
"""
for documento in documentos:
    documento_nombre = documento.name.rsplit('/',1)[1].split('.')[0]
    raw = documento.read()
    for i,tematica in enumerate(raw.replace("Honorable Asamblea:","Honorable asamblea:").split("Honorable asamblea:")):
        with io.open(path_to_raw+'tematicas/'+documento_nombre+'_'+str(i+1)+'.txt', mode="w") as newfile:
            tematica_limpia = mataAcentos(strip_punctuation(tematica.replace('\n',' ')))
            newfile.write(tematica_limpia)

def mataAcentos(s):
    charstosub = pd.DataFrame(zip([u'á', u'é', u'í', u'ó', u'ú',u'"',u'“',u'”',u',',u'\.',u'ñ',u'\!',u'\¡'],[u'a', u'e', u'i', u'o', u'u',u'',u'',u'',u'',u'',u'n',u'',u''])) 
    data = s.lower()
    for row in charstosub.iterrows():
        data = re.sub(row[1][0],row[1][1],data)
    return data
##Este no funciona aun
"""
Remover acentos y puntuacion parece no ser lo mejor


def cleanText(corpus):
    #punctuation = """.,?!:;(){}[]"""
    punctuation = punctuation
    corpus = [z.lower().replace('\n','') for z in corpus]
    corpus = [z.replace('<br />', ' ') for z in corpus]

    #treat punctuation as individual words
    for c in punctuation:
        corpus = [z.replace(c, ' %s '%c) for z in corpus]
    corpus = [z.split() for z in corpus]
    return corpus
"""

#Esto si funciona
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)
"""
Christian!!!!!
Crea una carpeta prueba y mete alli documentos de prueba para RAKE
"""
file_names_tematicas = [f for f in os.listdir(path_to_raw+'tematicas/') if f.endswith('.txt')]
sentences = []
i=0
dicto = {}
for doc in file_names_tematicas:
    f = io.open(path_to_raw+'tematicas/'+doc,'rt')
    sentences.append(gensim.models.doc2vec.LabeledSentence(f.read().split(),["SENT_"+str(i+1)]))
    dicto["SENT_"+str(i+1)] = doc 
    i=i+1
    f.close()
    
    
#Pruebas
sentences[0]
sentences[0:5]
print(sentences[0:5])


#Modelo
min_count = 5
size = 50
window = 10
 
model = gensim.models.doc2vec.Doc2Vec(sentences,size = size, window = window, min_count = min_count)





dir(model)
len(model.vocab)
model.similarity('organismos','constar')
checa(u'elecciones')
def checa(word):
    for i in model.most_similar(word):
        print(i)

print model.docvecs.most_similar(["SENT_1"])
model.docvecs["SENT_1"]
dir(model.docvecs)
model.docvecs.doctags
dir(model)

