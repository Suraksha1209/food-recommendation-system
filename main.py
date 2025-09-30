import streamlit as st 
import tensorflow as tf
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier 
import pandas as pd 
# import fnmatch
# import os


# Load JSON data containing vitamin values
with open("vitamin_data.json", "r") as f:
    vitamin_data = json.load(f)

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("VGG16_model95.h5")
    model = tf.keras.models.load_model("VGG16_model83.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of max element


# def data():
#     return pd.read_csv('newfood.csv')
# data=pd.read_csv(os.path.join(BASE_DIR ,"./food.csv"))

data = pd.read_csv("C:\\Users\\HP\\Desktop\\Food Recommender\\food\\food.csv")

Breakfastdata=data['Breakfast']
BreakfastdataNumpy=Breakfastdata.to_numpy()
                                   
Lunchdata=data['Lunch']
LunchdataNumpy=Lunchdata.to_numpy()
                                            
Dinnerdata=data['Dinner']
DinnerdataNumpy=Dinnerdata.to_numpy()
Food_itemsdata=data['Food_items']

def calculate_calories(age, weight, height, bodyfat, goal, activity, gender):
    leanfactor = 0.0
    if gender == "m":
        if 10 <= bodyfat <= 14:
            leanfactor = 1
        elif 15 <= bodyfat <= 20:
            leanfactor = 0.95
        elif 21 <= bodyfat <= 28:
            leanfactor = 0.90
        else:
            leanfactor = 0.85
    else:
        if 14 <= bodyfat <= 18:
            leanfactor = 1
        elif 19 <= bodyfat <= 28:
            leanfactor = 0.95
        elif 29 <= bodyfat <= 38:
            leanfactor = 0.90
        else:
            leanfactor = 0.85

    maintaincalories = int(weight * 24 * leanfactor * activity)

    caloriesreq = 0
    finaldata = []
    bmi = 0
    bmiinfo = ""
    if goal == "weight gain":
        finaldata = Weight_Gain(age, weight, height)
        bmi = int(finaldata[len(finaldata) - 2])
        bmiinfo = finaldata[len(finaldata) - 1]
        caloriesreq = maintaincalories + 300
    if goal == "weight loss":
        finaldata = Weight_Loss(age, weight, height)
        bmi = int(finaldata[len(finaldata) - 2])
        bmiinfo = finaldata[len(finaldata) - 1]
        caloriesreq = maintaincalories - 300

    if goal == "healthy":
        finaldata = Healthy(age, weight, height)
        bmi = int(finaldata[len(finaldata) - 2])
        bmiinfo = finaldata[len(finaldata) - 1]
        caloriesreq = maintaincalories

    return finaldata, bmi, bmiinfo, caloriesreq



def Weight_Loss(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving Lunch data rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    #print(LunchfoodseparatedIDdata)
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    #print(LunchfoodseparatedIDdata)

    # retrieving Breafast data rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving Dinner Data rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    #calculating BMI
    bmi = weight/((height/100)**2) 
    agewiseinp=0
        
    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)    

        
    #conditions
    bmiinfo=""    
    if ( bmi < 16):
        bmiinfo="According to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="According to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="According to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="According to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="According to your BMI, you are Severely Overweight"
        clbmi=0

    #converting into numpy array
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2
    
    ## K-Means Based  Dinner Food
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]

    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    XValu=np.arange(0,len(kmeans.labels_))
    
    # retrieving the labels for dinner food
    dnrlbl=kmeans.labels_

    ## K-Means Based  lunch Food
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    
    # retrieving the labels for lunch food
    lnchlbl=kmeans.labels_
    
    ## K-Means Based  lunch Food
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    
    # retrieving the labels for breakfast food
    brklbl=kmeans.labels_
    
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv("C:\\Users\\HP\\Desktop\\Food Recommender\\food\\nutrition_distriution.csv")

    ## train set
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc=list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t]=np.array(valloc)
            yt.append(brklbl[jj])
            t+=1
        # for jj in range(len(weightgaincat)):
        #     valloc=list(weightgaincat[jj])
        #     valloc.append(bmicls[zz])
        #     valloc.append(agecls[zz])
        #     weightgainfin[r]=np.array(valloc)
        #     yr.append(lnchlbl[jj])
        #     r+=1
        # for jj in range(len(healthycat)):
        #     valloc=list(healthycat[jj])
        #     valloc.append(bmicls[zz])
        #     valloc.append(agecls[zz])
        #     healthycatfin[s]=np.array(valloc)
        #     ys.append(dnrlbl[jj])
        #     s+=1

    
    X_test=np.zeros((len(weightlosscat),6),dtype=np.float32)

    print('####################')
    
    #randomforest
    for jj in range(len(weightlosscat)):
        valloc=list(weightlosscat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    
    X_train=weightlossfin# Features
    y_train=yt # Labels

    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
    #print (X_test[1])
    X_test2=X_test
    y_pred=clf.predict(X_test)
    
    returndata=[]
    print ('SUGGESTED FOOD ITEMS ::')
    for ii in range(len(y_pred)):
        print(y_pred)
        if y_pred[ii]==2:     #weightloss
            findata=Food_itemsdata[ii]
            returndata.append(Food_itemsdata[ii])
            # if int(veg)==1:
            #     datanv=['Chicken Burger']
        # for it in range(len(datanv)):
        #     if findata==datanv[it]:
        #         pass

    returndata.append(bmi)
    returndata.append(bmiinfo)
    return returndata


def Weight_Gain(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    
        
    # retrieving rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    #claculating BMI
    bmi = weight/((height/100)**2)        

    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)

    bmiinfo=""    
    #conditions

    if ( bmi < 16):
        bmiinfo="according to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="according to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="according to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="according to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="according to your BMI, you are Severely Overweight"
        clbmi=0


    
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2 
    
    
    ## K-Means Based  Dinner Food
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    # plt.bar(XValu,kmeans.labels_)
    dnrlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    
    ## K-Means Based  lunch Food
    # Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    # lnchlbl=kmeans.labels_
    dnrlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    
    ## K-Means Based  lunch Food
    # Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    # brklbl=kmeans.labels_
    lnchlbl=kmeans.labels_

    # K-Means Based  lunch Food
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    
    # retrieving the labels for breakfast food
    brklbl=kmeans.labels_
    
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv("C:\\Users\\HP\\Desktop\\Food Recommender\\food\\nutrition_distriution.csv")
    # datafin.head(5)
    
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    # in wg
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        # for jj in range(len(weightlosscat)):
        #     valloc=list(weightlosscat[jj])
        #     valloc.append(bmicls[zz])
        #     valloc.append(agecls[zz])
        #     weightlossfin[t]=np.array(valloc)
        #     yt.append(brklbl[jj])
        #     t+=1
        for jj in range(len(weightgaincat)):
            valloc=list(weightgaincat[jj])
            #print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r]=np.array(valloc)
            yr.append(lnchlbl[jj])
            r+=1
        # for jj in range(len(healthycat)):
        #     valloc=list(healthycat[jj])
        #     valloc.append(bmicls[zz])
        #     valloc.append(agecls[zz])
        #     healthycatfin[s]=np.array(valloc)
        #     ys.append(dnrlbl[jj])
        #     s+=1

    
    X_test=np.zeros((len(weightgaincat),10),dtype=np.float32)

  
    # In[287]:
    for jj in range(len(weightgaincat)):
        valloc=list(weightgaincat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    X_train=weightgainfin# Features
    y_train=yr # Labels
    
   
    
    
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
   
    X_test2=X_test
    y_pred=clf.predict(X_test)
    
    
    returndata=[]
    print("Suggested Food Item :: ")
    for ii in range(len(y_pred)):
        if y_pred[ii]==1: 
            print("now here")     #weightgain
            findata=Food_itemsdata[ii]
            print("i am hereeeeee")
            returndata.append(Food_itemsdata[ii])
            # if int(veg)==1:
            #     datanv=['Chicken Burger']
        # for it in range(len(datanv)):
        #     if findata==datanv[it]:
        #         pass

    returndata.append(bmi)
    returndata.append(bmiinfo)
    return returndata                    




def Healthy(age,weight,height):
    breakfastfoodseparated=[]
    Lunchfoodseparated=[]
    Dinnerfoodseparated=[]
        
    breakfastfoodseparatedID=[]
    LunchfoodseparatedID=[]
    DinnerfoodseparatedID=[]
        
    for i in range(len(Breakfastdata)):
        if BreakfastdataNumpy[i]==1:
            breakfastfoodseparated.append( Food_itemsdata[i] )
            breakfastfoodseparatedID.append(i)
        if LunchdataNumpy[i]==1:
            Lunchfoodseparated.append(Food_itemsdata[i])
            LunchfoodseparatedID.append(i)
        if DinnerdataNumpy[i]==1:
            Dinnerfoodseparated.append(Food_itemsdata[i])
            DinnerfoodseparatedID.append(i)
        
    # retrieving rows by loc method |
    LunchfoodseparatedIDdata = data.iloc[LunchfoodseparatedID]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.iloc[Valapnd]
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.T
        
    # retrieving rows by loc method 
    breakfastfoodseparatedIDdata = data.iloc[breakfastfoodseparatedID]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.iloc[Valapnd]
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.T
        
        
    # retrieving rows by loc method 
    DinnerfoodseparatedIDdata = data.iloc[DinnerfoodseparatedID]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
    val=list(np.arange(5,15))
    Valapnd=[0]+val
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.iloc[Valapnd]
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.T
        
    
    bmi = weight/((height/100)**2) 
    agewiseinp=0
        
    for lp in range (0,80,20):
        test_list=np.arange(lp,lp+20)
        for i in test_list: 
            if(i == age):
                tr=round(lp/20)  
                agecl=round(lp/20)    

    bmiinfo=""    
    #conditions
    print("Your body mass index is: ", bmi)
    if ( bmi < 16):
        bmiinfo="according to your BMI, you are Severely Underweight"
        clbmi=4
    elif ( bmi >= 16 and bmi < 18.5):
        bmiinfo="according to your BMI, you are Underweight"
        clbmi=3
    elif ( bmi >= 18.5 and bmi < 25):
        bmiinfo="according to your BMI, you are Healthy"
        clbmi=2
    elif ( bmi >= 25 and bmi < 30):
        bmiinfo="according to your BMI, you are Overweight"
        clbmi=1
    elif ( bmi >=30):
        bmiinfo="according to your BMI, you are Severely Overweight"
        clbmi=0

    
    DinnerfoodseparatedIDdata=DinnerfoodseparatedIDdata.to_numpy()
    LunchfoodseparatedIDdata=LunchfoodseparatedIDdata.to_numpy()
    breakfastfoodseparatedIDdata=breakfastfoodseparatedIDdata.to_numpy()
    ti=(clbmi+agecl)/2
    
    

    Datacalorie=DinnerfoodseparatedIDdata[1:,1:len(DinnerfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    dnrlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    
    Datacalorie=LunchfoodseparatedIDdata[1:,1:len(LunchfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    #print ('## Prediction Result ##')
    #print(kmeans.labels_)
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    lnchlbl=kmeans.labels_
    # plt.title("Predicted Low-High Weigted Calorie Foods")
   
    Datacalorie=breakfastfoodseparatedIDdata[1:,1:len(breakfastfoodseparatedIDdata)]
    
    X = np.array(Datacalorie)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    
    XValu=np.arange(0,len(kmeans.labels_))
    # fig,axs=plt.subplots(1,1,figsize=(15,5))
    # plt.bar(XValu,kmeans.labels_)
    brklbl=kmeans.labels_
    # print (len(brklbl))
    # plt.title("Predicted Low-High Weigted Calorie Foods")
    inp=[]
    ## Reading of the Dataet
    datafin=pd.read_csv("C:\\Users\\HP\\Desktop\\Food Recommender\\food\\nutrition_distriution.csv")
    datafin.head(5)
   
    dataTog=datafin.T
    bmicls=[0,1,2,3,4]
    agecls=[0,1,2,3,4]
    weightlosscat = dataTog.iloc[[1,2,7,8]]
    weightlosscat=weightlosscat.T
    weightgaincat= dataTog.iloc[[0,1,2,3,4,7,9,10]]
    weightgaincat=weightgaincat.T
    healthycat = dataTog.iloc[[1,2,3,4,6,7,9]]
    healthycat=healthycat.T
    weightlosscatDdata=weightlosscat.to_numpy()
    weightgaincatDdata=weightgaincat.to_numpy()
    healthycatDdata=healthycat.to_numpy()
    weightlosscat=weightlosscatDdata[1:,0:len(weightlosscatDdata)]
    weightgaincat=weightgaincatDdata[1:,0:len(weightgaincatDdata)]
    healthycat=healthycatDdata[1:,0:len(healthycatDdata)]
    
    
    weightlossfin=np.zeros((len(weightlosscat)*5,6),dtype=np.float32)
    weightgainfin=np.zeros((len(weightgaincat)*5,10),dtype=np.float32)
    healthycatfin=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    t=0
    r=0
    s=0
    yt=[]
    yr=[]
    ys=[]
    for zz in range(5):
        for jj in range(len(weightlosscat)):
            valloc=list(weightlosscat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightlossfin[t]=np.array(valloc)
            yt.append(brklbl[jj])
            t+=1
        for jj in range(len(weightgaincat)):
            valloc=list(weightgaincat[jj])
            #print (valloc)
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            weightgainfin[r]=np.array(valloc)
            yr.append(lnchlbl[jj])
            r+=1
        for jj in range(len(healthycat)):
            valloc=list(healthycat[jj])
            valloc.append(bmicls[zz])
            valloc.append(agecls[zz])
            healthycatfin[s]=np.array(valloc)
            ys.append(dnrlbl[jj])
            s+=1

    X_test=np.zeros((len(healthycat)*5,9),dtype=np.float32)
    
    for jj in range(len(healthycat)):
        valloc=list(healthycat[jj])
        valloc.append(agecl)
        valloc.append(clbmi)
        X_test[jj]=np.array(valloc)*ti
    
    
    X_train=healthycatfin# Features
    y_train=ys # Labels
    
    
    
    
    #Create a Gaussian Classifier
    clf=RandomForestClassifier(n_estimators=100)
    
    #Train the model using the training sets y_pred=clf.predict(X_test)
    clf.fit(X_train,y_train)
    
    
    X_test2=X_test
    y_pred=clf.predict(X_test)
   
    
    returndata=[]
    for ii in range(len(y_pred)):
        print(y_pred)
        if y_pred[ii]==1:
            returndata.append(Food_itemsdata[ii])
            findata=Food_itemsdata[ii]
            # if int(veg)==1:
                # datanv=['Chicken Burger']

    returndata.append(bmi)
    returndata.append(bmiinfo)

    return returndata






# Initialize session state variables
if 'predicted_label' not in st.session_state:
    st.session_state.predicted_label = ""
if 'vitamin1' not in st.session_state:
    st.session_state.vitamin1 = 0

# Sidebar
st.sidebar.title("Dashboard")
# app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Prediction", "Recommender"])
# Main Page
if app_mode == "Home":
    st.header("Food Recommender System")
    image_path = "home_img.jpg"
    st.image(image_path)

# About Project
# elif app_mode == "About Project":
#     st.header("About Project")
#     st.subheader("About Dataset")
#     st.text("This dataset contains images of the following food items:")
#     st.code("fruits- banana, apple, pear, grapes, orange, kiwi, watermelon, pomegranate, pineapple, mango.")
#     st.code("vegetables- cucumber, carrot, capsicum, onion, potato, lemon, tomato, raddish, beetroot, cabbage, lettuce, spinach, soy bean, cauliflower, bell pepper, chilli pepper, turnip, corn, sweetcorn, sweet potato, paprika, jalepeño, ginger, garlic, peas, eggplant.")
#     st.subheader("Content")
#     st.text("This dataset contains three folders:")
#     st.text("1. train (100 images each)")
#     st.text("2. test (10 images each)")
#     st.text("3. validation (10 images each)")

# Prediction Page
elif app_mode == "Prediction":
    st.header("Food Recommender")
    test_image = st.file_uploader("Choose an Image:")
    if st.button("Show Image"):
        st.image(test_image, width=4, use_column_width=True)

    # Create an empty element to display the predicted label
    predicted_label_display = st.empty()

    # Predict button
    if st.button("Predict"):
        st.write("Nutritional Facts")
        result_index = model_prediction(test_image)
        with open("labels.txt") as f:
            content = f.readlines()
        label = [i.strip() for i in content]
        predicted_label = label[result_index]
        predicted_label_display.success("It's  {}".format(predicted_label))
        # Set the session state to store the predicted label
        st.session_state.predicted_label = predicted_label
        
        # Find the vitamin value for the predicted label from the vitamin data
        for item in vitamin_data:
            if item['name'] == predicted_label:
                # st.session_state.vitamin1 = item['vitamin_value']
                # calcium = item.get('calcium', 'N/A')
                # iron = item.get('iron', 'N/A')
                # carbohydrates = item.get('carbohydrates', 'N/A')
                # vitamin_value = item.get('vitamin_value', 'N/A')
            
            # Display nutrient values
                # st.write("Calcium:", calcium)
                # st.write("Iron:", iron)
                # st.write("Carbohydrates:", carbohydrates)
                # st.write("Vitamin Value:", vitamin_value)
                st.image(item['nutiimage'], caption='Food Image', use_column_width=True)

            
            # Set the session state to store nutrient values
                # st.session_state.calcium = calcium
                # st.session_state.iron = iron
                # st.session_state.carbohydrates = carbohydrates
                # st.session_state.vitamin_value = vitamin_value


                # # if 'food_data' in st.session_state:
                # if predicted_label in st.session_state.food_data:
                #     food_info = st.session_state.food_data[predicted_label]
                #     image_url = food_info.get('image', None)
                #     nutriimage_url = food_info.get('nutiimage', None)
                #     if image_url:
                #         st.image(image_url, caption=predicted_label, use_column_width=True)
                #     else:
                #         st.write("Image not available for this food item.")
                    
                #     # Display nutritional image
                #     if nutriimage_url:
                #         st.image(nutriimage_url, caption="Nutritional Information", use_column_width=True)
                #     else:
                #         st.write("Nutritional image not available for this food item.")
                # else:
                #     st.write("Image not available for this predicted food item.")
                # # else:
                #     # st.write("Food data not found.")
                
                break


    # Input fields for vitamins
    # if "predicted_label" in st.session_state:
    #     vitamin2 = st.number_input("Enter Total nutrition value you needed:")  # system image vitamin value
    #     st.session_state.vitamin1 = st.number_input(f"Nutrition value of {st.session_state.predicted_label} :", st.session_state.vitamin1)

    #     difference = vitamin2 - st.session_state.vitamin1

    #     # Predict button
    #     if st.button("Calculate") and test_image is not None:
    #         # Filter items with vitamin values less than difference
    #         filtered_items = [item for item in vitamin_data if item["vitamin_value"] < difference]
    #         st.write("Recommended food are:")
            
    #         # Define the number of items to display per row
    #         items_per_row = 4
    #         num_items = len(filtered_items)

    #         # Calculate the number of rows needed
    #         num_rows = (num_items + items_per_row - 1) // items_per_row

    #         # Loop through each row
    #         for i in range(num_rows):
                # Define the start and end indices for the items in the current row
                # start_idx = i * items_per_row
                # end_idx = min((i + 1) * items_per_row, num_items)

                # # Create a Streamlit column for the current row
                # cols = st.columns(end_idx - start_idx)

                # # Loop through each item in the current row
                # for j, item_idx in enumerate(range(start_idx, end_idx)):
                #     item = filtered_items[item_idx]
                #     # Display the image and information in the current column
                #     with cols[j]:
                #         st.image(item['image'], caption=item['name'], width=100)
                #         st.write(f"Vitamin Value: {item['vitamin_value']} mg")



#recommnding food items
elif app_mode == "Recommender":
    st.title("BMI Calculator")

    age = st.number_input("Age", min_value=1, max_value=150, value=30)
    weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)
    height = st.number_input("Height (cm)", min_value=1, max_value=300, value=170)
    bodyfat = st.slider("Body Fat (%)", min_value=1, max_value=100, value=20)
    goal = st.selectbox("Goal", ["weight gain", "weight loss", "healthy"])
    activity = st.slider("Activity", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    gender = st.radio("Gender", ["male", "female"])

    if st.button("Calculate"):
        finaldata, bmi, bmiinfo, caloriesreq = calculate_calories(age, weight, height, bodyfat, goal, activity, gender)

        st.subheader("Recommended Meals")
        st.write("Breakfast:")
        st.write(finaldata[0])

        st.write("Lunch:")
        st.write(finaldata[1])
        
        st.write("Dinner:")
        st.write(finaldata[2])

        st.subheader("BMI")
        st.write(f"BMI: {bmi}")
        st.write(f"BMI Info: {bmiinfo}")

        st.subheader("Calories Required")
        st.write(f"Calories Required: {caloriesreq}")


