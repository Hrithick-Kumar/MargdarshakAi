import streamlit as st
from pymongo import MongoClient
from datetime import date
import base64
import os
import random
import time

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Margdarshak AI",
    page_icon="🎓",
    layout="wide"
)

# =========================
# DATABASE
# =========================

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
db = client["User"]
coll = db["Info"]

# =========================
# BACKGROUND
# =========================

def add_bg(image_file):

    if not os.path.exists(image_file):
        return

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:url("data:image/png;base64,{encoded}");
            background-size:cover;
            background-position:center;
            background-repeat:no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("background_img/bg.png")

# =========================
# HOME PAGE
# =========================

st.title("🎓 Margdarshak AI")
st.subheader("Your Smart Career & Stream Guidance Partner")

st.markdown("""
### Welcome

Margdarshak AI helps students choose the most suitable stream
and career path based on:

- Academic Performance
- Subject-wise Marks
- Interests & Preferences
- Skills & Strengths
- Career Goals

Our AI system provides personalized recommendations to help
students make better career decisions.
""")

# =========================
# PROFILE
# =========================

@st.dialog("Profile")
def profile():

    if "User" not in st.session_state:
        st.warning("Please sign in first")
        return

    username = st.session_state["User"]

    user = coll.find_one({"Name": username})

    if not user:
        st.error("User not found")
        return

    st.write(f"Username : {user['Name']}")
    st.write(f"DOB : {user['DOB']}")

    photo = user.get("Photo", "")

    img_path = f"images/{photo}"

    if os.path.exists(img_path):
        st.image(img_path, width=250)
    else:
        st.warning("Profile image not found")

# =========================
# ABOUT
# =========================

@st.dialog("About Margdarshak AI")
def about():

    st.header("About")

    st.markdown("""
    Margdarshak AI is an AI-powered career guidance platform.

    ### Technologies Used

    - Python
    - Streamlit
    - MongoDB
    - Scikit-Learn
    - Pandas

    ### Features

    - Stream Prediction
    - Career Guidance
    - Interest Analysis
    - Student Profile Management
    - AI Recommendations

    ### Goal

    Help students choose the right academic stream using
    data-driven decisions instead of confusion and pressure.
    """)

# =========================
# CONTACT
# =========================

@st.dialog("Contact")
def contact():

    st.write("📞 Phone: 9431774516")
    st.write("📧 Email: kumarhrithick369@gmail.com")
    st.write("💻 GitHub: Hrithick-kumar")

# =========================
# SIGN IN
# =========================

@st.dialog("Sign In")
def sign_in():

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        user = coll.find_one({
            "Name": username,
            "Pass": password
        })

        if user:

            st.session_state["User"] = username

            st.success("Login Successful")

            time.sleep(1)

            st.switch_page("pages/Dashboard.py")

        else:
            st.error("Invalid Username or Password")

# =========================
# SIGN UP
# =========================

@st.dialog("Sign Up")
def sign_up():

    st.subheader("Create Account")

    col1, col2 = st.columns(2)

    with col1:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        dob = st.date_input(
            "Date of Birth",
            min_value=date(1980, 1, 1),
            max_value=date.today()
        )

    with col2:

        photo = st.camera_input("Take Photo")

    if st.button("Register", use_container_width=True):

        if not username or not password:

            st.warning("Fill all required fields")
            return

        existing = coll.find_one({"Name": username})

        if existing:

            st.error("Username already exists")
            return

        photo_name = ""

        if photo:

            os.makedirs("images", exist_ok=True)

            photo_name = f"img_{random.randint(1000,9999)}.png"

            filepath = os.path.join(
                "images",
                photo_name
            )

            with open(filepath, "wb") as f:
                f.write(photo.getbuffer())

        coll.insert_one({
            "Name": username,
            "Pass": password,
            "DOB": str(dob),
            "Photo": photo_name
        })

        st.success("Registration Successful")

        time.sleep(1)

        st.rerun()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("Menu")

    if st.button(
        "👤 Profile",
        use_container_width=True
    ):
        profile()

    if st.button(
        "ℹ️ About",
        use_container_width=True
    ):
        about()

    if st.button(
        "📞 Contact",
        use_container_width=True
    ):
        contact()

    st.divider()

    if st.button(
        "📝 Sign Up",
        use_container_width=True
    ):
        sign_up()

    if st.button(
        "🔑 Sign In",
        use_container_width=True
    ):
        sign_in()<p style="font-size:23px;box-shadow:grey 10px 10px 46px;box-shadow:black 10px 15px 26px;border-radius:30px;padding:50px;">Choosing the right stream after 10th or 12th can shape your future — but making that decision is often confusing.
<br>
Margdarshak AI helps students discover the most suitable stream and career path using the power of Artificial Intelligence.</p>
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
              st.write(f"DOB : {x["DOB"]}")
              st.session_state["img"]=f"{x['Photo']}"
              c1.image(f"images/{x['Photo']}",width=300)

@st.dialog("About Margdarshak AI")
def About():
    c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
    st.markdown(f"""
    <p>Margdarshak AI is an AI-powered career and stream recommendation platform developed using Python and Streamlit.<br>
    <br>The project is designed to help students choose the most suitable stream after 10th and 12th based on their academic performance, interests, and career preferences.
    <br><br>
    This application combines Machine Learning, Data Processing, and Interactive Web Technologies to provide smart and personalized guidance for students.</p>
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >Technologies Used</h2>
    <h4 >Frontend & Interface</h4>
    <li>Streamlit — for creating the interactive web application interface.</li>
    """,unsafe_allow_html=True)
    st.code("""import streamlit as st\nst.title("Margdarshak AI")\nst.write("Your Smart Career & Stream Guidance Partner")""")

    st.markdown(f"""
    <br>
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >Data Handling</h2>
    <li>Pandas — for managing and analyzing student datasets.</li>""",unsafe_allow_html=True)
    st.code("""import pandas as pd\ndata = pd.read_csv("students.csv")\nst.dataframe(data.head())""")

    st.markdown(f"""
    <br>
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >Machine Learning</h2>
    <li>Scikit-learn — used for training AI models and predicting suitable streams.</li>""",unsafe_allow_html=True)
    st.code("""from sklearn.feature_extraction.text import CountVectorizer\ncv = CountVectorizer()\nX=df['Interest']\ny=df['Stream']\nx_matrix = cv.fit_transform(X)""")

    st.markdown(f"""
    <br>
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >Prediction Model</h2><br><br>
    """,unsafe_allow_html=True)
    st.code("""from sklearn.naive_bayes import MultinomialNB\nmodel = MultinomialNB()\nmodel.fit(x,y)""")

    st.markdown(f"""
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >MongoDB Database</h2>
    <br><br>
    <li>Used for storing user profiles, login details, and student information.</li>""",unsafe_allow_html=True)
    st.code("""from pymongo import MongoClient\nconn = MongoClient("mongodb string...")\ndb = conn["MargdarshakAI"]""")

    st.markdown(f"""
    <br>
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;" >Features of Margdarshak AI</h2>
    <br><br>
    <ul>
    <li>AI-based Stream Prediction</li>
    <li>Career Guidance System</li>
    <li>Student Interest Analysis</li>
    <li>10th & 12th Marks Evaluation</li>
    <li>Secure Login & User Profiles</li>
    <li>Profile Photo Upload</li>
    <li>Fast & Lightweight Interface</li>
    </ul><br>
    """,unsafe_allow_html=True)

    st.markdown(f"""
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;">Project Objective</h2>
    <br><br>
    <p>The main goal of Margdarshak AI is to reduce confusion among students while selecting streams and careers.
    <br>The system uses Artificial Intelligence to provide guidance based on data rather than assumptions or peer pressure.</p>
    <br>
    """,unsafe_allow_html=True)

    st.markdown(f"""
    <h2 style="font-size:20px;box-shadow:grey 3px 3px 2px;border-radius:10px;padding:30px;">Future Enhancements</h2>
    <br><br>
    <ul>
    <li>Advanced Deep Learning Models</li>
    <li>Career Roadmaps</li>
    <li>College Recommendations</li>
    <li>Skill Assessment Tests</li>
    <li>AI Chat Assistant for Students</li>
    </ul>
    <br>
    """,unsafe_allow_html=True)
    st.markdown(f"""<h1>Developer Motive</h1><br><p style="font-size:20px;margin-top:0px;box-shadow:white 0px 5px 6px;border-radius:30px;padding:10px;"> "Guiding Students Towards the Right Future with Artificial Intelligence."</p> """,unsafe_allow_html=True)


@st.dialog("Contact us")
def contact():
   st.markdown("Phone Number:9431774516")
   st.markdown("Email:kumarhrithick369@gmail.com")
   st.markdown("Github:Hrithick-kumar")
@st.dialog("Sign In")
def SignIn():
    c1,c2=st.columns([6,1])
    t1=st.text_input("Username",width=400)
    t2=st.text_input("Password",type="password",width=400)
    if st.button("SIGNIN"):
        user_fetch=coll.find_one({"Name":t1,"Pass":t2})
        if user_fetch:
                st.session_state['User']=t1
                st.session_state['Passwd']=t2
                st.success("Signed In Successfully")
                st.switch_page("pages/Dashboard.py")
        else:
                st.warning("Invalid Credentials")
                st.toast("Check password or username")
@st.dialog("Sign Up")
def SignUp():
    c1,c2,c3,c4,c5,c6=st.columns(6)
    st.header("SignUp")
    c1,c2=st.columns(2)
    min_date=date(1980,1,1)
    max_date=date(2040,12,31)
    name=c1.text_input("User Name",width=350)
    Password=c1.text_input("Password",type="password",width=350)
    dob=c1.date_input("DOB",value=date.today(),min_value=min_date,max_value=max_date,width=350)
    photo=c2.camera_input("Live Photo",width=350)
    count=random.randint(1,100)
    str1=""
    if photo:
            str1="img"+str(count)+".png"
            filepath=os.path.join("images",str1)
            bytes_data=photo.getbuffer()
            with open(filepath,"wb") as f:
                    f.write(bytes_data)
            if st.button("SAVE") and name!="" and Password!="" and dob!="" and str1!="":
                if coll.find_one({"Name":name}) and coll.find_one({"Pass":Password}):
                    st.warning("Already Exist")
                else:
                    coll.insert_one({"Name":name,"Pass":Password,"DOB":str(dob),"Photo":str1})
                    st.toast("Successfully Registered")
                    time.sleep(2)
                    st.switch_page("MargdarshakAi.py")
            else:
                if name=="" or Password=="" or dob=="" or str1=="":
                    st.toast("Required field details")
with st.sidebar:
    if st.button("Profile",use_container_width=True):
        profile()
    if st.button("About",use_container_width=True):
        About()
    if st.button("Contact",use_container_width=True):
        contact()
    if st.button("Sign Up",use_container_width=True):
        SignUp()
    if st.button("Sign In",use_container_width=True):
        SignIn()

