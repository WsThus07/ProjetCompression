import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
import pickle
import os
def W_fichier(donn,nom,ext):
    f = open('{}.{}'.format(nom,ext), "w")
    f.write(str(donn))
    f.close()
    
def r_fichier(path):
    f = open(path, "r")
    data=f.read()
    return data

def W_fichierOrg(donn,nom,ext):
    f = open('{}.{}'.format(nom,ext), "wb")
    f.write(bytearray(donn))
    f.close()
    

def lect_img_H(path):
    img=Image.open(path)
    img_array=np.array(img)
    dim=np.shape(img_array)
    liste=[0,dim[0],dim[1],dim[2],np.reshape(img,(dim[0]*dim[1]*dim[2]))]
    return liste
def cons_img_H(liste):
    img_array=np.reshape(liste[4],(liste[1],liste[2],liste[3]))
    return img_array
def lect_img_V(path):
    img=Image.open(path)
    img_array=np.array(img.rotate(-90))
    dim=np.shape(img_array)

    liste=[1,dim[0],dim[1],dim[2],np.reshape(img_array,(dim[0]*dim[1]*dim[2]))]
    return liste
def cons_img_V(liste):
    img_array=np.reshape(liste[4],(liste[1],liste[2],liste[3]))
    if liste[3]==4:
        PIL_image = Image.fromarray(img_array.astype('uint8'), 'RGBA')
    else:
        if liste[3]==3:
            PIL_image = Image.fromarray(img_array.astype('uint8'), 'RGB')
        else :
            PIL_image = Image.fromarray(img_array.astype('uint8'), 'L')
    return PIL_image.rotate(90)


def LZ78(phrase):
    s={}
    I={}
    dec=[]
    pos=0
    test=''
    count=0
    for k in range(len(phrase)):
        test+=phrase[k]
        if test not in s.keys():
            if len(test)>1:
                s[test]=(I[test[:-1]]+1,phrase[k])
                I[test]=(count)
                dec.append([I[test[:-1]]+1,phrase[k]])
                test=''
                count+=1

            else:
                s[test]=(0,test)
                I[test]=(count)
                dec.append([0,test]) 
                test=''
                count+=1
        if test  in s.keys() and k==len(phrase)-1:
                s[test]=(I[test[:-1]]+1,phrase[k])
                I[test]=(count)
                dec.append([I[test[:-1]]+1,phrase[k]])
                test=''
                count+=1
            
    return dec 

def deco_LZ78(suite):
    k={}
    p=''
    for i in range(len(suite)):
        g=suite[i][0]
        if g==0:
            k[i+1]=suite[i][1]
        else:
            k[i+1]=k[g]+suite[i][1]
    return "".join(k.values())
def to_binary(a):
    maxi=a[4][0][0]
    p=''
    for i in a[4] :
        if i[0]>maxi:
            maxi=i[0]

    taille=len(format(maxi,'b'))
    print(taille)

    p+=format(a[0],'b').zfill(2)
    p+=format(a[1],'b').zfill(16)
    p+=format(a[2],'b').zfill(16)
    p+=format(a[3],'b').zfill(2)
    p+=format(taille,'b').zfill(8)
    for i in a[4]:
        p+=format(i[0],'b').zfill(taille)+format(ord(i[1]),'b').zfill(8)
    return p

            
def compression(path):
    nom,ext=path.split('.')
    T=lect_img_H(path)
    W_fichierOrg(T[4],nom+'Org',ext)
    t=[chr(i) for i in T[4]]
    env_msg=[T[0],T[1],T[2],T[3],LZ78(t)]
    data=to_binary(env_msg)
    W_fichier(data,nom,'IRM')
    return  data,env_msg

def ORG_file(path):
    nom,ext=path.split('.')
    T=lect_img_H(path)
    W_fichierOrg(T[4],nom+'Org',ext)
    return  os.path.getsize(nom+'Org'+'.'+ext)

def compression_file_irm(path):
    nom,ext=path.split('.')
    T=lect_img_H(path)
    W_fichierOrg(T[4],nom+'Org',ext)
    t=[chr(i) for i in T[4]]
    env_msg=[T[0],T[1],T[2],T[3],LZ78(t)]
    data=to_binary(env_msg)
    W_fichier(data,nom,'IRM')
    pat=nom+'.IRM'
    return  os.path.getsize(pat)//8

def taux_compression(initiale,finale):
        return (1-(finale/initiale))*100
       
def reverse_binary(path):
    B=r_fichier(path)
    print(len(B))
    p=''
    k=[]
    y=44
    mode=B[:2]
    longeur=B[2:18]
    largeur=B[18:34]
    p=B[34:36]
    taille=int(str(B[36:44]),2)
    print(taille)
    k=[int(mode,2),int(longeur,2),int(largeur,2),int(p,2)]
    x=int(len(B[44:])/(8+taille))
    pas=8+taille
    for i in range(x):
        k.append([int(B[y:y+taille],2),chr(int(B[y+taille:y+taille+8],2))])
        print(y)
        y+=pas
    return k
def décompression(path):
    suite=reverse_binary(path)
    mat=deco_LZ78(suite[4:])
    G=[ord(i) for i in mat]
    suit_i=[suite[0],suite[1],suite[2],suite[3],G]
    photo=cons_img_H(suit_i)
    return  photo
