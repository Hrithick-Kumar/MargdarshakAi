import streamlit as st
from pymongo import MongoClient
import os
import time
import base64
conn=MongoClient("mongodb+srv://StreamDecider:stream123@cluster0.fgaudsd.mongodb.net/?appName=Cluster0")
db=conn["User"]
coll=db["Info"]
c1,c2,c3,c4,c5,c6,c7=st.columns([10,8,8,25,25,15,15])
if "User" not in st.session_state:
       st.toast("Please Sign in ..")
       time.sleep(2)
       st.switch_page("MargdarshakAi.py")
str1=st.session_state["User"]
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

st.markdown(f"""
<h6 style="color:#1A2421;font-size:23px;box-shadow:#1A2421 10px 10px 46px;box-shadow:#1A2421 10px 15px 26px;border-radius:30px;padding:10px 50px;">Explore your potential, discover your strengths, and make smarter academic decisions with Margdarshak AI.</h6>""",unsafe_allow_html=True)
pasd=""

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

