import os
import sys
import random
import numpy as np
import math

y={}
x1={}
x2={}
for i in range(0,100):
    x1[i]=random.random()
    x2[i]=random.random()
    y[i]=3*x1[i]+6*x2[i]+0.08

#for i in range(0,100):
#    print y[i],x1[i],x2[i]

#use cem to learn param
w1=0
w2=0
w3=0

mu1=1
mu2=1
mu3=1
sigma1=sigma2=sigma3=10

topn=10

#generate pred, suppose w is guass distribution
pred={}
for t in range(0,100):
    loss_total=0
    w_loss={}
    w={}
    for k in range(0,100):
        loss_sum=0
        pass_cnt=0
    
        w1 = random.gauss(mu1,sigma1)
        w2 = random.gauss(mu2,sigma2)
        w3 = random.gauss(mu3,sigma3)
 
        #batch eval, don't change every instance!!
        ####very importance step1
        for i in range(0,100):
            #print w1,w2,w3
            pred[i]=w1*x1[i]+w2*x2[i]+w3
            #print pred[i],y[i]
            #if loss less than 0.1, remember wi value ,later update wi
            loss_sum+=math.fabs(pred[i]-y[i])
            #need to sort according to loss!!! otherwise no imporvement
            if(math.fabs(pred[i]-y[i])<1):
                pass_cnt+=1
        #print "loss = ",loss_sum
        #print "pass_cnt = ",pass_cnt
        w_loss[k]=loss_sum
        w[k]=[w1,w2,w3]
        loss_total+=loss_sum

    print t,loss_total
    #update mu and sigma
    w1s=[]
    w2s=[]
    w3s=[]

    sorted_wv = sorted(w_loss.items(),key=lambda item:float(item[1]))
    cnt = 0
    for ws,v in sorted_wv:
        print ws,v,w[ws][0],w[ws][1],w[ws][2]
        if(cnt<topn):
            ###weighted importance , if not add this, will not reach optimize solution!!!
            ###very importance step2
            for f in range(topn-cnt):
                w1s.append(w[ws][0])
                w2s.append(w[ws][1])
                w3s.append(w[ws][2])
        else:
            break
        cnt+=1

    #update mu and sigma
    ###very important step3
    #print w
    mu1=np.mean(w1s)
    mu2=np.mean(w2s)
    mu3=np.mean(w3s)
    sigma1=np.std(w1s)
    sigma2=np.std(w2s)
    sigma3=np.std(w3s)
    print mu1,mu2,mu3

