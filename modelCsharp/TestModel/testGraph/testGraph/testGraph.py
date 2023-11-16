import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import aspose.words as aw
import shutil
import pdb

path = os.getcwd()

#run it on machine
#observed_path = os.path.join(path, "../../../../TestModel/Observed/observed.csv")

#run this code for an action
observed_path = "TestModel/Observed/observed.csv"

# fertiliser input
#observed_path = os.path.join(path, "../../../../TestModel/TestModel/FertiliserData.csv")

observed_data = pd.read_csv(observed_path,index_col=0)

# fertiliser input
#observed_data = pd.read_csv(observed_path,index_col=[0,1])

observed_data.sort_index(axis=0,inplace=True)

tests = []
test_name = []

# run it on machine
#for file in os.listdir(path+"\\OutputFiles"):
    
    #if file.endswith('.csv'):
        #tests.append(file)       
        #test_name.append(os.path.splitext(file)[0])

#uncomment it for an Action
for file in os.listdir(path):
    
    if file.endswith('.csv'):
        tests.append(file)       
        test_name.append(os.path.splitext(file)[0])

Alltests =[]
for t in tests[:]:  
    
    #uncomment it for an Action
    testframe = pd.read_csv(t,index_col=0,dayfirst=True,date_format='%d/%m/%Y %H:%M:%S %p')
    
    #testframe = pd.read_csv(path + "\\OutputFiles\\"+t,index_col=0,dayfirst=True,date_format='%d/%m/%Y %H:%M:%S %p') 
    
    Alltests.append(testframe)   

AllData = pd.concat(Alltests,axis=1,keys=test_name)

#uncomment it for a observed.csv
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

# uncomment it for observed,csv    
def make_observed(observed):
    plt.plot(observed.index,observed.loc[:,'Nitrogen'],'*',color='g')

# fertiliser input    
#def make_observed(observed):
    #plt.plot(observed.index,observed.loc[:,'0-30cm'],'*',color='g')
        
Graph = plt.figure(figsize=(10,10))
pos = 1
row_num=len(tests)

for t in tests:
    start = dt.datetime.date(AllData[t].dropna().index.min())
    end = dt.datetime.date(AllData[t].dropna().index.max())
    
    datefilter = []
    # fertiliser input 
    #observed_data_currentTest = observed_data.loc[int(t[0]),:]
    #for d in observed_data_currentTest.index:
        #datata=dt.datetime.strptime(d,'%Y-%m-%d')
        #ret = False        
        #if ((datata>= pd.Timestamp(start)) and (datata<=pd.Timestamp(end))):
            #ret = True
        #datefilter.append(ret)

    #uncomment it for observed.csv
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
    Graph.suptitle('DRAFT VERSION',fontsize = 32, color = "b")
    
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


