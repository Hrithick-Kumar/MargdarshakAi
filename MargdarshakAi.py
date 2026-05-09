import streamlit as st
from datetime import date
import time
import base64
import os
from pymongo import MongoClient
import random
conn=MongoClient("mongodb+srv://StreamDecider:stream123@cluster0.fgaudsd.mongodb.net/?appName=Cluster0")
db=conn["User"]
coll=db["Info"]

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
    h1, h2, h3, p {{
        color:white;
    }}

    </style>
    """, unsafe_allow_html=True)
c1,c2,c3,c4,c5,c6,c7=st.columns([10,3,6,6,6,6,6])
@st.dialog("Profile")
def profile():
       c1,c2=st.columns(2)
       if "User" not in st.session_state:
            st.warning("Please Sign in first")
            st.switch_page("MargdarshakAi.py")
       pro=st.session_state["User"]
       url=""
       pasd=""
       for x in coll.find({"Name":pro}):
              st.write(f"Username : {x["Name"]}")
              st.write(f"Password :XXX{x["Pass"][3:]}")
              st.write(f"Course : {x["course"]}")
              st.write(f"Address: {x['Address']}")
              st.write(f"DOB : {x["DOB"]}")
              st.session_state["img"]=f"{x['Photo']}"
              c1.image(f"images/{x['Photo']}",width=300)
if c3.button("Profile",type="primary"):
       profile()

@st.dialog("About")
def About():
    c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
    st.markdown(f"""
    <h1 style="color:Wheat;box-shadow:black 10px 15px 26px;padding:10px 60px;border-radius:30px;">About Margdarshak AI</h1>
    <p style="font-size:20px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Margdarshak AI is an AI-powered career and stream recommendation platform developed using Python and Streamlit.<br>
    The project is designed to help students choose the most suitable stream after 10th and 12th based on their academic performance, interests, and career preferences.
    <br>
    This application combines Machine Learning, Data Processing, and Interactive Web Technologies to provide smart and personalized guidance for students.</p>
    <h2 >Technologies Used</h2>
    <h4 >Frontend & Interface</h4>
    <li style="color:white;font-size:20px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Streamlit — for creating the interactive web application interface.</li>
    """,unsafe_allow_html=True)
    st.code("""import streamlit as st\nst.title("Margdarshak AI")\nst.write("Your Smart Career & Stream Guidance Partner")""")

    st.markdown(f"""
    <h2 >Data Handling</h2>
    <li style="color:white;font-size:20px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Pandas — for managing and analyzing student datasets.</li>""",unsafe_allow_html=True)
    st.code("""import pandas as pd\ndata = pd.read_csv("students.csv")\nst.dataframe(data.head())""")

    st.markdown(f"""
    <h2 >Machine Learning</h2>
    <li style="color:white;font-size:20px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Scikit-learn — used for training AI models and predicting suitable streams.</li>""",unsafe_allow_html=True)
    st.code("""from sklearn.feature_extraction.text import CountVectorizer\ncv = CountVectorizer()\nX=df['Interest']\ny=df['Stream']\nx_matrix = cv.fit_transform(X)""")

    st.markdown(f"""
    <h2 >Prediction Model</h2>
    """,unsafe_allow_html=True)
    st.code("""from sklearn.naive_bayes import MultinomialNB\nmodel = MultinomialNB()\nmodel.fit(x,y)""")

    st.markdown(f"""
    <h2 >MongoDB Database</h2>
    <li style="color:white;font-size:20px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Used for storing user profiles, login details, and student information.</li>""",unsafe_allow_html=True)
    st.code("""from pymongo import MongoClient\nconn = MongoClient("mongodb string...")\ndb = conn["MargdarshakAI"]""")

    st.markdown(f"""
    <h2 >Features of Margdarshak AI</h2>
    <ul style="box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">
    <li style="color:white;">AI-based Stream Prediction</li>
    <li style="color:white;">Career Guidance System</li>
    <li style="color:white;">Student Interest Analysis</li>
    <li style="color:white;">10th & 12th Marks Evaluation</li>
    <li style="color:white;">Secure Login & User Profiles</li>
    <li style="color:white;">Profile Photo Upload</li>
    <li style="color:white;">Fast & Lightweight Interface</li>
    </ul>
    """,unsafe_allow_html=True)

    st.markdown(f"""
    <h2 ">Project Objective</h2>
    <p style="box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">The main goal of Margdarshak AI is to reduce confusion among students while selecting streams and careers.
    <br>The system uses Artificial Intelligence to provide guidance based on data rather than assumptions or peer pressure.</p>
    """,unsafe_allow_html=True)

    st.markdown(f"""
    <h2 >Future Enhancements</h2>
    <ul style="box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">
    <li style="color:white;">Advanced Deep Learning Models</li>
    <li style="color:white;">Career Roadmaps</li>
    <li style="color:white;">College Recommendations</li>
    <li style="color:white;">Skill Assessment Tests</li>
    <li style="color:white;">AI Chat Assistant for Students</li>
    </ul>
    """,unsafe_allow_html=True)
    st.markdown(f"""<h3 style="font-size:30px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:10px 60px;">Developer Motive</h3><p style="font-size:23px;color:wheat;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;"> "Guiding Students Towards the Right Future with Artificial Intelligence."</p> """,unsafe_allow_html=True)

if c4.button("About",type="primary"):
       About()

@st.dialog("Contact us")
def contact():
   st.markdown("Phone Number:9431774516")
   st.markdown("Email:kumarhrithick369@gmail.com")
   st.markdown("Github:hfhdfkjk")
if c5.button("Contact",type="primary"):
       contact()
@st.dialog("Sign In")
def SignIn():
    c1,c2=st.columns([6,1])
    t1=st.text_input("Username",width=400)
    t2=st.text_input("Password",type="password",width=400)
    if st.button("SIGNIN",type="primary"):
        conn=MongoClient("mongodb+srv://StreamDecider:stream123@cluster0.fgaudsd.mongodb.net/?appName=Cluster0")
        db=conn["User"]
        coll=db["Info"]
        user_fetch=coll.find_one({"Name":t1,"Pass":t2})
        if user_fetch:
                st.session_state['User']=t1
                st.session_state['Passwd']=t2
                st.switch_page("pages/Dashboard.py")
        else:
                st.warning("Invalid Credentials")
                st.toast("Check password or username")
if c7.button("Sign In",type="primary"):
    SignIn()
@st.dialog("Sign Up")
def SignUp():
    c1,c2,c3,c4,c5,c6=st.columns(6)
    st.header("SignUp")
    c1,c2=st.columns(2)
    min_date=date(1980,1,1)
    max_date=date(2040,12,31)
    name=c1.text_input("User Name",width=350)
    Password=c1.text_input("Password",type="password",width=350)
    c=c1.selectbox("Course",['BCA','IT','CS','AI & ML'],width=350)
    g=c1.radio("Gender",['M','F'],width=350)
    address=c2.text_area("Address",width=350)
    dob=c2.date_input("DOB",value=date.today(),min_value=min_date,max_value=max_date,width=350)
    photo=c2.camera_input("Live Photo",width=350)
    count=random.randint(1,100)
    str1="img"+str(count)+".png"
    if st.button("SAVE",type="primary") and name!="" and Password!="" and dob!="" and address!="":
        if photo:
                filepath=os.path.join("images",str1)
                bytes_data=photo.getbuffer()
                with open(filepath,"wb") as f:
                        f.write(bytes_data)
        conn=MongoClient("mongodb+srv://StreamDecider:stream123@cluster0.fgaudsd.mongodb.net/?appName=Cluster0")
        db=conn["User"]
        coll=db["Info"]
        if coll.find_one({"Name":name}) and coll.find_one({"Pass":Password}):
                st.warning("Already Exist")
        else:
                if name=="" or Password=="" or address=="" or dob=="" or photo=="":
                        st.toast("Required field details")
                else:

                        coll.insert_one({"Name":name,"Pass":Password,"course":c,"Gender":g,"Address":address,"DOB":str(dob),"Photo":str1})
                        st.toast("Successfully Registered")
                        st.switch_page("MargdarshakAi.py")
if c6.button("Sign Up",type="primary"):
    SignUp()

add_bg("background_img/bg.png")
st.markdown(f"""
<h1 style="color:black;">Welcome to 'Margdarshak Ai'</h1>
<h4 style="color:black;">Your Smart Career & Stream Guidance Partner</h4>
<h6 style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Explore your potential, discover your strengths, and make smarter academic decisions with Margdarshak AI.</h6>
<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Choosing the right stream after 10th or 12th can shape your future — but making that decision is often confusing.
<br>
Margdarshak AI helps students discover the most suitable stream and career path using the power of Artificial Intelligence.</p>
<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">
Choosing the right stream after 10th or 12th can shape your future — but making that decision is often confusing.
Margdarshak AI helps students discover the most suitable stream and career path using the power of Artificial Intelligence.
</p>
<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Whether you're interested in Science, Commerce, Arts, Technology, Design, Medical, Government Jobs, Business, or Creative Fields, our AI analyzes your:
</p>
<ul style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">
   <li>Academic performance</li>
   <li>Subject-wise marks</li>
   <li>Interests & preferences</li>
   <li>Skills and strengths</li>
   <li>Career goals</li>
</ul>
<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">…and provides personalized stream recommendations designed especially for you</p>
<h2 style="color:#1A2421;">What Margdarshak AI Does</h2>
<p>
<ul style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">
<li>Analyzes 10th & 12th marks</li>
<li>Understands student interests and choices</li>
<li>Suggests the best stream and career direction</li>
<li>Provides AI-based smart recommendations</li>
<li>Helps students make confident career decisions</li>
<li>Simple, fast, and student-friendly interface</li></ul>
</p>
<h2 style="color:#1A2421;">Why Choose Margdarshak AI?</h2>
<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Many students choose streams based on pressure, confusion, or trends.
Margdarshak AI focuses on your abilities, interests, and future goals to guide you toward the right path.
</p>
<h5 style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">"Right Guidance Today Creates a Better Tomorrow."</h5>
<h5 style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">"So choose right today,lest regret forever"</h5>

""",unsafe_allow_html=True)

