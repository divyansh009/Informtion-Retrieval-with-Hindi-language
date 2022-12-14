# -*- coding: utf-8 -*-
"""Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xHULc4z0OrRmadtTf3ktdB9F9hs0bC2b
"""

#We need to install a package named gensim that will help us to download pretrained vectors from GloVe, Word2vec and fastText
#!pip install gensim

#Importing neccesary libraries:
import numpy as np #To handle words in vector form
import gensim.downloader as api #Helps to download the word2Vec, glove pretrained models in notebook
from gensim.test.utils import datapath

#Now, we'll download the pretrained word vectors.
#In the hindi zip file, we're given 4 subfolders: 50, 100, 200, 300. They represent the dimensions of word vectors.
#We'll try all of them one by one.
#Let's try first 50 dimension one:
from gensim.models.word2vec import Word2Vec
model=Word2Vec.load('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/50/cbow/hi-d50-m2-cbow.model')

from multiprocessing import cpu_count 
#The multiprocessing package offers both local and remote concurrency, by using subprocesses instead of threads.
model

from gensim.models import KeyedVectors
# Store just the words + their trained embeddings.
word_vectors = model.wv 
word_vectors.save("word2vec.wordvectors")
# Load back with memory-mapping = read-only, shared across processes.
wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')

vector1 = wv['फल']  # Get numpy vector of a word
#Note: It might not detect if we type hindi words in english font. So, we must type words in hindi font only mandatorily

vector1

vector2 = wv['केला']

vector2

#Now, we'll try to build a cosine similarity function from scratch.
#It will help us to find wheather the given pair of words are similar or not.
#We'll try to manually experiment around with few similar and dissimilar words.
#Based on the results, we will set a specific threshold value.
#If the score is above threshold, then words are similar. If score is below threshold, then words are not similar.
num=np.dot(vector1,vector2)

from numpy.linalg import norm
den=norm(vector1)*norm(vector2)

den

num

cos=num/den

cos

#Since, the above words are very similar, we can keep a threshold value of 0.4.

#We tested it for a random value decided by us.
#But, we must apply it on the dataset given to us also.
#So, we'll define a function for cosine similarity.
#We'll call it directly then instead of performing so many steps for every entry.
import pandas as pd #To store the text file
df=pd.read_csv('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',lineterminator='\n',header=None)

df

df= df.rename(columns={0:'Word1',1:'Word2',2:'Ground Truth'}) #Renaming column names as per naming conventions

df

df['Ground Truth']=df['Ground Truth'].apply(lambda x:x*.1) #Making ground truth values b/w 0 to 1

df

wordsim=[item for item in df['Ground Truth']]

wordsim

#Defining function for cosine similarity:
def cos_sim(a,b):
    #Converting vectors to a numpy array:
    a=np.array(a)
    b=np.array(b)
    num=a.dot(b) #Numerator
    den=norm(a)*norm(b) #Denominator
    cos=num/den #Cosine similarity value
    return cos

"""# WORD2VEC-CBOW"""

#Now, we're given 5 threshold values(0.4, 0.5, 0.6, 0.7 and 0.8). If score is above threshold, then the words are similar.
#If the score is below threshold, then the words are dissimilar.
#So, we'll define a function for threshold that will help us to know the same.
def threshold(a,thresh):
    arr=[]
    for i in a: #Here a is the score
        if(i>=thresh):
            arr.append(1) #Words are similar
        else:
            arr.append(0) #Words are not similar
    return arr

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity\Word similarity\hindi.txt',encoding='utf-8')

wordsimilarity

Cbow=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        wordvec1=model.wv[word1] #As we used originally Word2vec CBOW only and saved it as model
        wordvec2=model.wv[word2]
        Cbow.append(cos_sim(wordvec1,wordvec2))

Cbow

df['Similarity Score']=Cbow #We'll save the CBOW similarity score in new column

df

df1=df.copy()

df1

#Now, we'll consider all 5 thresholds one by one and store their output as arrays
#Threshold is 0.4 and CBOW MODEL 50
cbow_sim =threshold(Cbow,0.4)

#To find accuracy, we must define the functions as follows:
def negate_vec(vect1):                                     # negation of binay array
    inverse_s = [2 if i==1 else i for i in vect1]
    inverse_s = [1 if i==0 else i for i in inverse_s]
    inverse_s = [0 if i==2 else i for i in inverse_s]
    return(inverse_s)
def accuracy(vec1,vec2):
    sim=[]
    vect1=negate_vec(vec1)
    sim = [a ^ b for a,b in zip(vect1,vec2)]
    num_ones = sim.count(1)
    return((num_ones/len(vect1))*100,sim)

wordsim_4=threshold(wordsim,0.4)
wordsim_5=threshold(wordsim,0.5)
wordsim_6=threshold(wordsim,0.6)
wordsim_7=threshold(wordsim,0.7)
wordsim_8=threshold(wordsim,0.8)

accuracy_4,sim_4 = accuracy(cbow_sim,wordsim_4)
df1['Label']=sim_4

#Reindexing according to convention asked
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"] 
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy:",accuracy_4," "," "," "] #Adding at last index

df1

df1.to_csv("Q1_50_Cbow_similarity_4.csv") #Save file as csv

df1=df.copy() #To get initial values of dataframe again

df1

#Now, we'll crepeat the same process for all models and thresholds to obtain 2*4*5=40 csv files
#Threshold is 0.5 and CBOW MODEL 50
cbow_sim =threshold(Cbow,0.5)
accuracy_5,sim_5 = accuracy(cbow_sim,wordsim_5)
df1['Label']=sim_5

column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)

df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]

df1

df1.to_csv("Q1_50_Cbow_similarity_5.csv")

df1=df.copy()

#Threshold is 0.6 and CBOW MODEL 50
cbow_sim =threshold(Cbow,0.6)
accuracy_6,sim_6 = accuracy(cbow_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]

df1

df1.to_csv("Q1_50_Cbow_similarity_6.csv")

#Threshold is 0.7 and CBOW MODEL 50
df1=df.copy()
cbow_sim =threshold(Cbow,0.7)
accuracy_7,sim_7 = accuracy(cbow_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]

df1

df1.to_csv("Q1_50_Cbow_similarity_7.csv")

#Threshold is 0.8 and CBOW MODEL 50
df1=df.copy()
cbow_sim =threshold(Cbow,0.8)
accuracy_8,sim_8 = accuracy(cbow_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]

df1

df1.to_csv("Q1_50_Cbow_similarity_8.csv")

#Now we'll deal with CBOW MODEL 100

cbow_model=Word2Vec.load('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/100/cbow/hi-d100-m2-cbow.model')

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity\Word similarity\hindi.txt',encoding='utf-8')

Cbow=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        wordvec1=cbow_model.wv[word1]
        wordvec2=cbow_model.wv[word2]
        Cbow.append(cos_sim(wordvec1,wordvec2))

df1=df.copy()

df1['Similarity Score']=Cbow

df=df1.copy()

df1

#Threshold is 0.4 and CBOW MODEL 100
cbow_sim =threshold(Cbow,0.4)
accuracy_4,sim_4 = accuracy(cbow_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_100_Cbow_similarity_4.csv")

df1

#Threshold is 0.5 and CBOW MODEL 100
df1=df.copy()
cbow_sim =threshold(Cbow,0.5)
accuracy_5,sim_5 = accuracy(cbow_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_100_Cbow_similarity_5.csv")

df1

#Threshold is 0.6, CBOW MODEL 100
df1=df.copy()
cbow_sim =threshold(Cbow,0.6)
accuracy_6,sim_6 = accuracy(cbow_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_100_Cbow_similarity_6.csv")

df1

#Threshold is 0.7 and CBOW MODEL 100
df1=df.copy()
cbow_sim =threshold(Cbow,0.7)
accuracy_7,sim_7 = accuracy(cbow_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_100_Cbow_similarity_7.csv")

df1

#Threshold is 0.8 and CBOW MODEL 100
df1=df.copy()
cbow_sim =threshold(Cbow,0.8)
accuracy_8,sim_8 = accuracy(cbow_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_100_Cbow_similarity_8.csv")

df1

"""# WORD2VEC-FAST TEXT"""

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

from gensim.models import FastText
Ft=FastText.load('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/50/fasttext/hi-d50-m2-fasttext.model')

Ft_sim=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=Ft.wv[word1]
        vec2=Ft.wv[word2]
        Ft_sim.append(cos_sim(vec1,vec2))

df1=df.copy()

df1

df1['Similarity Score']=Ft_sim
df1

df=df1.copy()

#Threshold is 0.4 and FAST TEXT 50
df1=df.copy()
ft_sim =threshold(Ft_sim,0.4)
accuracy_4,sim_4 = accuracy(ft_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_50_FastText_similarity_4.csv")

df1

#Threshold is 0.5 and FAST TEXT 50
df1=df.copy()
ft_sim =threshold(Ft_sim,0.5)
accuracy_5,sim_5 = accuracy(ft_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_50_FastText_similarity_5.csv")

df1

#Threshold is 0.6 and FAST TEXT 50
df1=df.copy()
ft_sim =threshold(Ft_sim,0.6)
accuracy_6,sim_6 = accuracy(ft_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_50_FastText_similarity_6.csv")

df1

#Threshold is 0.7 and FAST TEXT 50
df1=df.copy()
ft_sim =threshold(Ft_sim,0.7)
accuracy_7,sim_7 = accuracy(ft_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_50_FastText_similarity_7.csv")

df1

#Threshold is 0.8 and FAST TEXT 50
df1=df.copy()
ft_sim =threshold(Ft_sim,0.8)
accuracy_8,sim_8 = accuracy(ft_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_50_FastText_similarity_8.csv")

df1

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

Ft=FastText.load('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/100/fasttext/hi-d100-m2-fasttext.model')

Ft_sim=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=Ft.wv[word1]
        vec2=Ft.wv[word2]
        Ft_sim.append(cos_sim(vec1,vec2))

df1=df.copy()

df1['Similarity Score']=Ft_sim
df1

df=df1.copy()

#Threshold is 0.4 and FAST TEXT 100
df1=df.copy()
ft_sim =threshold(Ft_sim,0.4)
accuracy_4,sim_4 = accuracy(ft_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_100_FastText_similarity_4.csv")

df1

#Threshold is 0.5 and FAST TEXT 100
df1=df.copy()
ft_sim =threshold(Ft_sim,0.5)
accuracy_5,sim_5 = accuracy(ft_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_100_FastText_similarity_5.csv")

df1

#Threshold is 0.6 and FAST TEXT 100
df1=df.copy()
ft_sim =threshold(Ft_sim,0.6)
accuracy_6,sim_6 = accuracy(ft_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_100_FastText_similarity_6.csv")

df1

#Threshold is 0.7 and FAST TEXT 100
df1=df.copy()
ft_sim =threshold(Ft_sim,0.7)
accuracy_7,sim_7 = accuracy(ft_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_100_FastText_similarity_7.csv")

df1

#Threshold is 0.8 and FAST TEXT 100
df1=df.copy()
ft_sim =threshold(Ft_sim,0.8)
accuracy_8,sim_8 = accuracy(ft_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_100_FastText_similarity_8.csv")

df1

"""# Glove"""

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

file = open("D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/50/glove/hi-d50-glove.txt",encoding='utf-8',errors='ignore')
cntrl=1
vocab=[]
glove={}
for line in file:
    line=line.strip('\n')
    line=line.split(" ") # separating the data wiht the \n
    wv=line.pop(0)
    line= [float(i) for i in line]
    glove[wv]=line
    cntrl=cntrl+1

glove_sim=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=glove[word1]
        vec2=glove[word2]
        glove_sim.append(cos_sim(vec1,vec2))

df1=df.copy()

df1['Similarity Score']=glove_sim
df1

df=df1.copy()

#Threshold is 0.4 and FAST TEXT 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.4)
accuracy_4,sim_4 = accuracy(glove_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_4.csv")

df1

#Threshold is 0.5 and GLOVE 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.5)
accuracy_5,sim_5 = accuracy(glove_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_5.csv")

df1

#Threshold is 0.6 and GLOVE 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.6)
accuracy_6,sim_6 = accuracy(glove_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_6.csv")

df1

#Threshold is 0.7 and GLOVE 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.7)
accuracy_7,sim_7 = accuracy(glove_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_7.csv")

df1

#Threshold is 0.8 and GLOVE 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.8)
accuracy_8,sim_8 = accuracy(glove_sim,wordsim_7)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_8.csv")

df1

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

file = open("D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/100/glove/hi-d100-glove.txt",encoding='utf-8',errors='ignore')
cntrl=1
vocab=[]
glove={}
for line in file:
    line=line.strip('\n')
    line=line.split(" ") # separating the data wiht the \n
    wv=line.pop(0)
    line= [float(i) for i in line]
    glove[wv]=line
    cntrl=cntrl+1

glove_sim=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=glove[word1]
        vec2=glove[word2]
        glove_sim.append(cos_sim(vec1,vec2))

df1=df.copy()

df1['Similarity Score']=glove_sim
df1

df=df1.copy()

#Threshold is 0.4 and FAST TEXT 50
df1=df.copy()
glove_sim =threshold(glove_sim,0.4)
accuracy_4,sim_4 = accuracy(glove_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_50_Glove_similarity_4.csv")

df1

#Threshold is 0.5 and GLOVE 100
df1=df.copy()
glove_sim =threshold(glove_sim,0.5)
accuracy_5,sim_5 = accuracy(glove_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_100_Glove_similarity_5.csv")

df1

#Threshold is 0.6 and GLOVE 100
df1=df.copy()
glove_sim =threshold(glove_sim,0.6)
accuracy_6,sim_6 = accuracy(glove_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_100_Glove_similarity_6.csv")

df1

#Threshold is 0.7 and GLOVE 100
df1=df.copy()
glove_sim =threshold(glove_sim,0.7)
accuracy_7,sim_7 = accuracy(glove_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_100_Glove_similarity_7.csv")

df1

#Threshold is 0.8 and GLOVE 100
df1=df.copy()
glove_sim =threshold(glove_sim,0.8)
accuracy_8,sim_8 = accuracy(glove_sim,wordsim_7)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_100_Glove_similarity_8.csv")

df1

"""# SKIPGRAM"""

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

sg = Word2Vec.load("D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/50/sg/hi-d50-m2-sg.model")

Sg=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=sg.wv[word1]
        vec2=sg.wv[word2]
        Sg.append(cos_sim(vec1,vec2))

df1=df.copy()

df1['Similarity Score']=Sg
df1

df=df1.copy()

#Threshold is 0.4 and SKIPGRAM 50
df1=df.copy()
Sg_sim =threshold(Sg,0.4)
accuracy_4,sim_4 = accuracy(Sg_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_50_SkipGram_similarity_4.csv")

#Threshold is 0.5 and SKIPGRAM 50
df1=df.copy()
Sg_sim =threshold(Sg,0.5)
accuracy_5,sim_5 = accuracy(Sg_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_50_SkipGram_similarity_5.csv")

#Threshold is 0.6 and SKIPGRAM 50
df1=df.copy()
Sg_sim =threshold(Sg,0.6)
accuracy_6,sim_6 = accuracy(Sg_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_50_SkipGram_similarity_5.csv")

#Threshold is 0.7 and SKIPGRAM 50
df1=df.copy()
Sg_sim =threshold(Sg,0.7)
accuracy_7,sim_7 = accuracy(Sg_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_50_SkipGram_similarity_7.csv")

#Threshold is 0.8 and SKIPGRAM 50
df1=df.copy()
Sg_sim =threshold(Sg,0.8)
accuracy_8,sim_8 = accuracy(Sg_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_50_SkipGram_similarity_8.csv")

wordsimilarity=open('D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/Word similarity/Word similarity/hindi.txt',encoding='utf-8')

sg = Word2Vec.load("D:/001M-Tech IIT-Kanpur/1Subjects/INFO RETRIEVAL/A-2/hi/hi/100/sg/hi-d100-m2-sg.model")

Sg=[]
for line in wordsimilarity:
    line=line.strip("\n").split(",")
    if len(line)>1:
        word1=line[0].strip(" ")
        word2=line[1].strip(" ")
        vec1=sg.wv[word1]
        vec2=sg.wv[word2]
        Sg.append(cos_sim(vec1,vec2))

df1=df.copy()

df1['Similarity Score']=Sg
df1

df=df1.copy()

#Threshold is 0.4 and SKIPGRAM 100
df1=df.copy()
Sg_sim =threshold(Sg,0.4)
accuracy_4,sim_4 = accuracy(Sg_sim,wordsim_4)
df1['Label']=sim_4
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_4," "," "," "]
df1.to_csv("Q1_100_SkipGram_similarity_4.csv")

#Threshold is 0.5 and SKIPGRAM 100
df1=df.copy()
Sg_sim =threshold(Sg,0.5)
accuracy_5,sim_5 = accuracy(Sg_sim,wordsim_5)
df1['Label']=sim_5
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_5," "," "," "]
df1.to_csv("Q1_100_SkipGram_similarity_5.csv")

#Threshold is 0.6 and SKIPGRAM 100
df1=df.copy()
Sg_sim =threshold(Sg,0.6)
accuracy_6,sim_6 = accuracy(Sg_sim,wordsim_6)
df1['Label']=sim_6
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_6," "," "," "]
df1.to_csv("Q1_100_SkipGram_similarity_6.csv")

#Threshold is 0.7 and SKIPGRAM 100
df1=df.copy()
Sg_sim =threshold(Sg,0.7)
accuracy_7,sim_7 = accuracy(Sg_sim,wordsim_7)
df1['Label']=sim_7
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_7," "," "," "]
df1.to_csv("Q1_100_SkipGram_similarity_7.csv")

#Threshold is 0.8 and SKIPGRAM 100
df1=df.copy()
Sg_sim =threshold(Sg,0.8)
accuracy_8,sim_8 = accuracy(Sg_sim,wordsim_8)
df1['Label']=sim_8
column_title=["Word1","Word2", "Similarity Score","Ground Truth","Label"]
df1=df1.reindex(columns=column_title)
df1.loc[65]=["Accuracy is:",accuracy_8," "," "," "]
df1.to_csv("Q1_100_SkipGram_similarity_8.csv")





