# -*- coding: utf-8 -*-
"""Untitled (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ChUs1BYHJbC5jNweBYhA9Pw1CGe0WjZy
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
# %matplotlib inline

dataset=pd.read_csv('/content/drive/MyDrive/data.csv')

from google.colab import drive
drive.mount('/content/drive')

dataset.shape

dataset.head()

dataset.drop(['Unnamed: 32','id'], axis = 1 , inplace=True)
dataset.columns

dataset.diagnosis.replace({"M":1,"B":0},inplace=True)
dataset.diagnosis.unique()

dataset.info()

dataset.isnull().sum()

dataset.head()

dataset.describe()

desc = dataset.describe().T
df1 = pd.DataFrame(index=['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean',
       'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'perimeter_worst', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst'], 
                   columns= ["count","mean","std","min",
                             "25%","50%","75%","max"], data= desc )

f,ax = plt.subplots(figsize=(12,12))

sns.heatmap(df1, annot=True,cmap = "Blues", fmt= '.0f',
            ax=ax,linewidths = 5, cbar = False,
            annot_kws={"size": 16})

plt.xticks(size = 18)
plt.yticks(size = 12, rotation = 0)
plt.ylabel("Variables")
plt.title("Descriptive Statistics", size = 16)
plt.show()

plt.title('Count of cancer type')
sns.countplot(dataset['diagnosis'])
plt.xlabel('Cancer lethality')
plt.ylabel('Count')
plt.show()

#histogram (verinin her ??zellikte da????l??m??)
dataset.hist(figsize = (30,30), color = 'orange')
plt.show()

# radius mean da????l??m??
sns.stripplot(x="diagnosis", y="radius_mean", data=dataset, jitter=True, edgecolor="gray")
plt.show()

# corelasyon matris
corr = dataset.corr()
plt.figure(figsize=(20,20))
sns.heatmap(corr, cbar=True, square= True, fmt='.1f', annot=True, annot_kws={'size':15}, cmap='coolwarm')
plt.show()

#corelasyon matris 0.6 ??st??ndeki de??erler
corr_matrix = dataset.corr()

threshold = 0.60
filter = np.abs(corr_matrix["diagnosis"])>threshold
corr_features = corr_matrix.columns[filter].tolist()

f,ax=plt.subplots(figsize = (16,16))
sns.heatmap(dataset[corr_features].corr(),annot= True,fmt = ".2f",
            vmin = -1,vmax = 1,ax=ax,annot_kws={"size": 16},cmap = "coolwarm")
plt.xticks(rotation=45, size = 14)
plt.yticks(rotation=0, size = 14)
plt.title('Correlation btw Features', size = 14)
plt.show()

#verinin labela g??re d??zenlenmesi
dataset_temp = dataset.drop(['diagnosis'],axis=1)
X = np.array(dataset_temp).T 
Y = np.array(dataset['diagnosis']).T
Y = Y.reshape(1,569)

X.shape

Y.shape

#normalizasyon
X_mean = np.mean(X,axis=1,keepdims=True) 
X_max = np.max(X,axis=1,keepdims=True)
X_normalized = (X-X_mean)/(X_max)

X_normalized

#train test split

X_train = X_normalized[:,:380]
Y_train = Y[:,:380]

X_cv = X_normalized[:,381:]
Y_cv = Y[:,381:]

"""Modelin Olusturulmasi

"""

#L3 aktivasyon
def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s

#l1 l2 aktivasyon (gizli katman)
def tanh(z):
    s = (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))
    return s

def forward_prop(X,W1,W2,W3,b1,b2,b3):
    
    #Katman 1 forward propogation
    Z1 = np.dot(W1,X)
    A1 = tanh(Z1 + b1)
    #Katman 2 forward propogation
    Z2 = np.dot(W2,A1)
    A2 = tanh(Z2 + b2)
    #Katman 3 forward propogation
    Z3 = np.dot(W3,A2)
    A3 = sigmoid(Z3 + b3) #A3 olas??l??k matrisi
    
    cache = {    
                  "Z1": Z1,
                  "A1": A1,
                  "Z2": Z2,
                  "A2": A2,
                  "Z3": Z3,
                  "A3": A3
            }
    return cache

def gradient_descent(iterations,X,Y,alpha):
    
    #ilk fp i??in random veriler
    W1 = np.random.randn(3,30)*0.01
    b1 = np.random.rand(3,1)
    W2 = np.random.randn(2,3)*0.01
    b2 = np.random.rand(2,1)
    W3 = np.random.rand(1,2)*0.01
    b3 = np.random.rand(1,1)
    dummy,m = X.shape
    
    caches = [] #her iterasyon i??in maliyetler
    count_vector = [] #iterasyon sayac??
    count = 0
    
    for i in range (1,iterations):
        
            count = count + 1
            
            count_vector.append(count)
        
            params = forward_prop(X,W1,W2,W3,b1,b2,b3) #fp
            
            #fp den d??nen verileri ata
            Z1 = params['Z1']
            Z2 = params['Z2']
            Z3 = params['Z3']
            A1 = params['A1']
            A2 = params['A2']
            A3 = params['A3']
            
            #????k???? i??in maliyet hesapla
            cost = -(1 / m)*np.sum(np.multiply(Y,np.log(A3)) + np.multiply((1-Y),np.log(1-A3)))
            caches.append(cost)
            
            #Katman 3 geri besleme
            dA3 = -Y/A3 + (1-Y)/(1-A3)
            dZ3 = dA3 * sigmoid(Z3)*(1-sigmoid(Z3))
            dW3 = (1 / m)*np.dot(dZ3,A2.T)
            db3 = (1 / m)*np.sum(dZ3,axis=1,keepdims=True)
            
            #Katman 2 geri besleme
            dA2 = np.dot(W3.T,dZ3)
            dZ2 = dA2*(1-np.power(tanh(Z2),2))
            dW2 = (1 / m)*np.dot(dZ2,A1.T)
            db2 = (1 / m)*np.sum(dZ2,axis=1,keepdims=True)
            
            #Katman 1 geri besleme
            dA1 = np.dot(W2.T,dZ2)
            dZ1 = dA1*(1-np.power(tanh(Z1),2))
            dW1 = (1 / m)*np.dot(dZ1,X.T)
            db1 = (1 / m)*np.sum(dZ1,axis=1,keepdims=True)
            
            #Geri beslemede hesaplanan t??revleri kullanarak a????rl??k parametreleri g??ncellenir
            W1 = W1 - alpha*dW1
            W2 = W2 - alpha*dW2
            W3 = W3 - alpha*dW3
            
            #Geri beslemede hesaplanan t??revleri kullanarak bias parametreleri g??ncellenir
            b1 = b1 - alpha*db1
            b2 = b2 - alpha*db2
            b3 = b3 - alpha*db3
        
    return W1,W2,W3,b1,b2,b3,count_vector,caches

W1,W2,W3,b1,b2,b3,count,caches = gradient_descent(1000,X_cv,Y_cv,0.5)

plt.plot(count,caches,label='Cost')

plt.xlabel('Iteration')
plt.ylabel('Cost')

plt.title("Cost vs. Iteration")

plt.legend()

plt.show()

def predict(X,Y,iterations,alpha,X_train,Y_train):

    W1,W2,W3,b1,b2,b3,count,caches = gradient_descent(iterations,X_train,Y_train,alpha)
    
    Z1 = np.dot(W1,X)
    A1 = tanh(Z1 + b1)
    Z2 = np.dot(W2,A1)
    A2 = tanh(Z2 + b2)
    Z3 = np.dot(W3,A2)
    A3 = sigmoid(Z3 + b3)
    
    dummy,m = A3.shape
    Y_prediction = np.zeros((1, m))
    
    for i in range(m):
        
        Y_prediction[0, i] = 1 if A3[0, i] > 0.5 else 0
        
    return Y_prediction

#acc
print("Train accuracy: {} %".format(100 - np.mean(np.abs(predict(X_train,Y_train,1000,0.5,X_train,Y_train) - Y_train)) * 100))
print("Test accuracy: {} %".format(100 - np.mean(np.abs(predict(X_cv,Y_cv,1000,0.5,X_train,Y_train) - Y_cv)) * 100))

"""Confusion Matrix"""

dummy,m1 = X_train.shape
dummy,m2 = X_cv.shape

train_predict = predict(X_train,Y_train,1000,0.5,X_train,Y_train)
CV_predict = predict(X_cv,Y_cv,1000,0.5,X_train,Y_train)
count_true_pos = 0
count_train_pos = 0

count_true_pos_cv = 0
count_cv_pos = 0

for i in range (1,m1):
    if train_predict[0,i] == 1 and Y_train[0,i] == 1:
        count_true_pos = count_true_pos + 1
    if Y_train[0,i] == 1:
        count_train_pos = count_train_pos + 1
        
for i in range (1,m2):
    if CV_predict[0,i] == 1 and Y_cv[0,i] == 1:
        count_true_pos_cv = count_true_pos_cv + 1
    if Y_cv[0,i] == 1:
        count_cv_pos = count_cv_pos + 1
        
print(str(count_true_pos) + " positives predicted on the training set")
print(str(count_train_pos) + " true positives are in the training set")
print("The accuracy of true positives on the training set is: {} %".format(100-np.abs(100*((count_true_pos - count_train_pos)/count_train_pos))))
print("----------------------------------------------------------------")
print(str(count_true_pos_cv) + " positives predicted on test set")
print(str(count_cv_pos) + " true positives are in test set")
print("The accuracy of true positives on test set is: {} %".format(100-np.abs(100*((count_true_pos_cv - count_cv_pos)/count_true_pos_cv))))


count_true_neg = 0
count_train_neg = 0

count_true_neg_cv = 0
count_cv_neg = 0

for i in range (1,m1):
    if train_predict[0,i] == 0 and Y_train[0,i] == 0:
        count_true_neg = count_true_neg + 1
    if Y_train[0,i] == 0:
        count_train_neg = count_train_neg + 1
        
for i in range (1,m2):
    if CV_predict[0,i] == 0 and Y_cv[0,i] == 0:
        count_true_neg_cv = count_true_neg_cv + 1
    if Y_cv[0,i] == 0:
        count_cv_neg = count_cv_neg + 1
        
print(str(count_true_neg) + " negatives predicted on the training set")
print(str(count_train_neg) + " true negatives are in the training set")
train_acc=100-np.abs(100*((count_true_neg - count_train_neg)/count_train_neg))
print(train_acc)
print("The accuracy of true negatives on the training set is: {} %".format(100-np.abs(100*((count_true_neg - count_train_neg)/count_train_neg))))
print("----------------------------------------------------------------")
print(str(count_true_neg_cv) + " negatives predicted on test set")
print(str(count_cv_neg) + " true negatives are in test set")
test_acc=100-np.abs(100*((count_true_neg_cv - count_cv_neg)/count_true_neg_cv))
print("The accuracy of true negatives on test set is: {} %".format(100-np.abs(100*((count_true_neg_cv - count_cv_neg)/count_true_neg_cv))))

grafik = np.array([train_acc,100-train_acc])
grafik_label = ["Dogruluk" , "Hata"]
plt.pie(grafik , labels = grafik_label , autopct='%1.2f%%')
plt.title("Train Acc")
plt.show()

grafik = np.array([test_acc,100-test_acc])
grafik_label = ["Dogruluk" , "Hata"]
plt.pie(grafik , labels = grafik_label , autopct='%1.2f%%')
plt.title("Test Acc")
plt.show()