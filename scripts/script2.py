from lib import *

### loading the data
df=pd.read_csv("/Users/niloofar/Downloads/Hotel_Reviews.csv")

# total number of hotels:

len(set(df.Hotel_Name))
print(df.Hotel_Name.value_counts())


#change the format of time to datetime

df['Review_Date']=pd.to_datetime(df['Review_Date'], format='%m/%d/%Y')
df1=df[df.Hotel_Name=="Britannia International Hotel Canary Wharf"]
df1.index = range(df1.shape[0])