import numpy as np 
from pdf2image import convert_from_path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from PIL import Image
import glob
import os, sys, os.path, time
from tensorflow.keras import Input
from tensorflow.keras import Model


def getnames(path,):
    with open(path, 'r') as f:
        names = f.readlines()

    return names


def learning (x_train, y_train, names):
    inp = Input(shape=(810*570*3,))
    out = Dense(len(names),  activation = 'softmax')(inp)
    model=Model(inputs = inp, outputs = out)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs = 50)
    
    return model



def usenet(path,model):
    os.chdir(path)
    rename0(path)
    i = sum([len(files) for r, d, files in os.walk(path)])
    pdf_to_png(path)
    resizeZ(path)
    data = png_to_list(path)
    data1 = np.array(data)
    data1.flatten()
    
    data1 = np.array(data1).reshape(i, 810*570*3)
   
    for file in os.listdir(path):
        if file.endswith(".png"):
           os.remove(file)
    pred= model.predict(data1)
    #*print (pred)
    
    return pred


def resize(path):
    os.chdir(path)
    dirs = os.listdir( path )
    for item in dirs:
        if item.endswith(".png"):
            im = Image.open(item)
            f = os.path.splitext(item)
            imResize = im.resize((570,810), Image.ANTIALIAS)
            imResize.save(str(f) + ' resized.png', 'png', quality=90)




def resizeZ(path):
    os.chdir(path)
    dirs = os.listdir( path )
    for item in dirs:
        if item.endswith(".png"):
            im = Image.open(item)
            f = os.path.splitext(item)
            im = im.resize((570,810), Image.ANTIALIAS)
            im.save(item, quality=90)




def png_to_list(path):
    os.chdir(path)
    img = []
    for file in os.listdir(path):

        if file.endswith(".png"):
            
            im = np.array(Image.open(file))
               
            img.append(im)
             
    return img


def pdf_to_png(path):
    os.chdir(path)
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            images = convert_from_path(file, 70, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
            fname = file +'.png'
            images[0].save(fname, "PNG")
        
        
    for file in os.listdir(path):
        if file.endswith(".PDF"):
            images = convert_from_path(file, 70,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
            fname = file +'.png'
            images[0].save(fname, "PNG")



def rename0(path):
    os.chdir(path)
    i = 0
    for file in os.listdir(path):
        os.rename(file, str(i) + '.pdf')
        i+=1


def rename(path, path_model, pred):
    os.chdir(path)
    txt_path = '.'.join(path_model.split('.')[:-1]) + '.txt'
    name=getnames(txt_path)
    #for i in range(len(pred)):
    pred = np.flip(pred, 1)
    #pred = np.array(pred)
    pred.flatten()
    
    #print(pred)
    i = 0
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    #print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', name, name[1], name[0])
    for file in os.listdir(path):
        #if pred[i][0] == 1 and pred[i][1] == 0: 
        #    os.rename(file, name[0][:-1] + str(j) + '.pdf')
        #    j+=1
            
        #if pred[i][0] == 0 and pred[i][1] == 1:
         #   os.rename(file, name[1][:-1] + str(k) + '.pdf')
         #   k+=1

        p = np.array([])
        for j in range(5 - len(pred[i])):
            p = np.append(p, 0)
        p = np.append(p, pred[i])
        #print(p)

        if np.array_equal(p, [0, 0, 0, 0, 1]):
            os.rename(file, name[0][:-1] + str(a) + '.pdf')
            a+=1

        if np.array_equal(p, [0, 0, 0, 1, 0]):
            os.rename(file, name[1][:-1] + str(b) + '.pdf')
            b+=1

        if np.array_equal(p, [0, 0, 1, 0, 0]):
            os.rename(file, name[2][:-1] + str(c) + '.pdf')
            c+=1

        if np.array_equal(p, [0, 1, 0, 0, 0]):
            os.rename(file, name[3][:-1] + str(d) + '.pdf')
            d+=1

        if np.array_equal(p, [1, 0, 0, 0, 0]):
            os.rename(file, name[4][:-1] + str(e) + '.pdf')
            e+=1
        
        i+=1