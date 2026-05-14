import streamlit as st
from pymongo import MongoClient
import os
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import base64
import pandas as pd
import matplotlib.pyplot as plt

data1=""
data2=""
conn=MongoClient("mongodb+srv://StreamDecider:stream123@cluster0.fgaudsd.mongodb.net/?appName=Cluster0")
db=conn["User"]
coll=db["Info"]
c1,c2,c3,c4,c5,c6,c7=st.columns([10,8,8,25,25,15,15])
if "User" not in st.session_state:
       st.toast("Please Sign in ..")
       time.sleep(2)
       st.switch_page("MargdarshakAi.py")
str1=st.session_state["User"]

st.header("MargdarshakAi")
def add_bg(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size:cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity:1;
    }}

    </style>
    """, unsafe_allow_html=True)
add_bg("background_img/bg.png")
pasd=""

st.markdown(f"""
<h6 style="color:#1A2421;font-size:23px;box-shadow:#1A2421 10px 10px 46px;box-shadow:#1A2421 10px 15px 26px;border-radius:30px;padding:10px 50px;">Explore your potential, discover your strengths, and make smarter academic decisions with Margdarshak AI.</h6><br><br>
<h2 style="color:#1A2421;">What your goals write here</h2><br<br>
<h5 style="color:rgb(6, 126, 116);padding-bottom:0px;padding-left:10px;">What's in your mind write here</h5>
""",unsafe_allow_html=True)
data=pd.read_csv("Stream1.csv",encoding="latin-1")
df=pd.DataFrame(data)
X=df['word']
y=df['stream']
vc=CountVectorizer()
X_input=vc.fit_transform(X)
model=MultinomialNB()
model.fit(X_input,y)
userInput=st.text_area("")
user_mess=vc.transform([userInput])
prediction=model.predict(user_mess)
data1=prediction[0]
@st.dialog("MargdarshakAi Suggestion")
def suggestion():
       st.write(f"According to your goal we suggest you to choose----> {prediction[0]}")

if st.button("Get Suggestion",use_container_width=True,type="primary"):
       if userInput=="":
              st.toast("Please tell us about your goals")
       else:
              suggestion()
# subject=['English','Maths','Science']
# marks=[34,56,78]
# p1,a1=plt.subplots()
# a1.pie(marks,labels=subject,colors=['red','green'],autopct="%1.0f%%",explode=[0.1,0.1,0],shadow=True)
# st.pyplot(p1)
user_mark_data=pd.read_csv('StudentMark.csv',encoding="latin-1")
df1=pd.DataFrame(user_mark_data)
inp=df1[['Average']]
out=df1['Stream']
model=DecisionTreeClassifier()
model.fit(inp,out)

sub1=[]
@st.dialog("User Input")
def Userdetail():
       sum=0
       mean=0
       sub1=st.multiselect("Choose subjects of class 10th",['Maths','Science','Social Science','English','Hindi','Sanskrit','Computer'])
       for x in range(len(sub1)):
              marks=st.number_input(f"Enter marks in {sub1[x]}",value=0)
              sum=sum+marks
              mean=len(sub1)
       if st.button("Submit"):
              mean=int(sum / len(sub1))
              predi=model.predict([[mean]])
              data2=predi[0]
              st.write(f"According to marks you can choose \n{predi[0]}")
if st.button("User Input"):
       Userdetail()
@st.dialog("Update photo")
def updatePhoto():
       c1,c2=st.columns(2)
       url=st.file_uploader(label="Upload Photo")
       c1.markdown("Preview image")
       if "img" not in st.session_state:
              st.warning("Please upload image first")
              time.sleep(2)
              st.switch_page("pages/SignUp.py")
       oldurl=st.session_state["img"]
       if url is not None:
              filepath=os.path.join("images/updateImg",url.name)
              with open(filepath,"wb") as f:
                     f.write(url.getbuffer())
                     url1=f"updateImg/{url.name}"
       if url:
              c1.image(url,width=300)
       if st.button("Update"):
              coll.update_one({"Photo":oldurl},{"$set":{"Photo":url1}})
              st.toast("Updated successfully")
              time.sleep(2)
              st.switch_page("pages/Dashboard.py")


@st.dialog("Change Password")
def updatePass():
       oldpass=st.text_input("Old Password",type="password")
       newpass=st.text_input("New Password",type="password")
       if st.button("Update"):
              if oldpass==pasd:
                     coll.update_one({"Pass":oldpass},{"$set":{"Pass":newpass}})
                     st.success("password updated successfully")
                     time.sleep(2)
                     st.switch_page("pages/Dashboard.py")
              else:
                     st.error("Password not found")

with st.sidebar:
       st.subheader(f"Welcome,{str1}")
       for x in coll.find({'Name':str1}):
              st.session_state["img"]=f"{x['Photo']}"
              st.image(f"images/{x['Photo']}",width=300)
              pasd=x['Pass']
       if st.button("Update Photo",use_container_width=True):
              updatePhoto()
       if st.button("Change Password",use_container_width=True):
              updatePass()
       if st.button("SignOut",use_container_width=True):
              st.session_state.clear()
              st.switch_page("MargdarshakAi.py")
dataGroup={
       'Result':[[data1],[data2]]
}
st.write(dataGroup['Result'])
