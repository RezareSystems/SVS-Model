import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import aspose.words as aw
import shutil

path = os.getcwd()

#run it on machine
#observed_path = os.path.join(path, "../../../../TestModel/Observed/observed.csv")

#run this code for an action
observed_path = "TestModel/Observed/observed.csv"

observed_data = pd.read_csv(observed_path,index_col=0)

observed_data.sort_index(axis=0,inplace=True)

tests = []
test_name = []

# run it on machine
#for file in os.listdir(path+"\\OutputFiles"):
    
    #if file.endswith('.csv'):
        #tests.append(file)       
        #test_name.append(os.path.splitext(file)[0])

for file in ("OutputFiles"):
    
    if file.endswith('.csv'):
        tests.append(file)       
        test_name.append(os.path.splitext(file)[0])


Alltests =[]
for t in tests[:]:  
   
    testframe = pd.read_csv(path + "\\OutputFiles\\"+t,index_col=0,dayfirst=True,date_format='%d/%m/%Y %H:%M:%S %p')  
    
    Alltests.append(testframe)   

AllData = pd.concat(Alltests,axis=1,keys=test_name)

observed_data.index=pd.to_datetime(observed_data.index,format="%d/%m/%Y %H:%M")

observed_test = observed_data.columns.get_level_values(0).drop_duplicates()
AllData.sort_index(axis=0,inplace=True)

AllData.index = pd.to_datetime(AllData.index)

tests = AllData.columns.get_level_values(0).drop_duplicates()
colors = pd.Series(['r','b','g'])

start = dt.datetime.date(AllData['8Wheat'].dropna().index.min())
end = dt.datetime.date(AllData['8Wheat'].dropna().index.max())

def makeplot(Data,color):
    plt.plot(Data,color=color)
    
def make_observed(observed):
    plt.plot(observed.index,observed.loc[:,'Nitrogen'],'*',color='g')     
        
Graph = plt.figure(figsize=(10,10))
pos = 1
row_num=len(tests)

for t in tests:
    start = dt.datetime.date(AllData[t].dropna().index.min())
    end = dt.datetime.date(AllData[t].dropna().index.max())
    datefilter = []
    for d in observed_data.index:
        ret = False
        if ((d >= pd.Timestamp(start)) and (d<=pd.Timestamp(end))):
            ret = True
            # if site id matching the observed id make it true only then 
        datefilter.append(ret)
        
    color = 'b'
    Graph.add_subplot(row_num,2,pos)
    Data = AllData.loc[:,(t,'SoilMineralN')].sort_index()
    plt.xticks(rotation = 45)    
    plt.title("SoilMineralN")
    makeplot(Data,color)
    make_observed(observed_data[datefilter])
    Graph.tight_layout(pad=1.5)
    pos+=1
    
    Graph.add_subplot(row_num,2,pos)
    plt.xticks(rotation = 45)  
    plt.title("CropN")
    Data = AllData.loc[:,(t,'CropN')].sort_index()
    makeplot(Data,color)
    make_observed(observed_data[datefilter])
    pos+=1

plt.savefig('testplot.png')

doc = aw.Document()
builder = aw.DocumentBuilder(doc)
builder.insert_image("testplot.png")
doc.save("index.html")

plt.show()

#shutil.rmtree(path+"\\OutputFiles")
#shutil.rmtree(path+"\\NitrogenApplied")


