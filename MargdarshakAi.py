import streamlit as st
from datetime import date
import time
import base64
import os
import random
from pymongo import MongoClient

st.set_page_config(page_title="Margdarshak AI",page_icon="🎓",layout="wide")

# ================= DATABASE =================

conn=MongoClient(st.secrets["MONGO_URI"])
db=conn["User"]
coll=db["Info"]

# ================= BACKGROUND =================

def add_bg(image_file):
    if not os.path.exists(image_file):
        return

    with open(image_file,"rb") as image:
        encoded=base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp{{
            background-image:url("data:image/png;base64,{encoded}");
            background-size:cover;
            background-position:center;
            background-repeat:no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("background_img/Bg1.png")

# ================= HOME =================

st.markdown("""
<h1 style="color:black;">Margdarshak AI</h1>
<h3 style="color:black;">Your Smart Career & Stream Guidance Partner</h3>

<div style="background:rgba(25,25,25,0.8);padding:20px;border-radius:20px;margin-top:20px;">
<h4>Explore your potential, discover your strengths, and make smarter academic decisions with Margdarshak AI.</h4>

<p style="font-size:18px;">
Choosing the right stream after 10th or 12th can shape your future.
Margdarshak AI helps students discover the most suitable stream and career path using Artificial Intelligence.
</p>

<ul>
<li>Academic Performance Analysis</li>
<li>Subject-wise Marks Evaluation</li>
<li>Interest Analysis</li>
<li>Skills & Strength Detection</li>
<li>Career Goal Guidance</li>
</ul>

<p style="font-size:18px;">
Our AI system provides personalized recommendations designed especially for students.
</p>
</div>
""",unsafe_allow_html=True)

# ================= PROFILE =================

@st.dialog("Profile")
def profile():

    if "User" not in st.session_state:
        st.warning("Please Sign In First")
        return

    username=st.session_state["User"]

    user=coll.find_one({"Name":username})

    if not user:
        st.error("User not found")
        return

    st.subheader("User Profile")

    st.write(f"Username : {user['Name']}")
    st.write(f"DOB : {user['DOB']}")
    st.write(f"Password : XXX{user['Pass'][3:]}")

    photo=user.get("Photo","")

    img_path=f"images/{photo}"

    if os.path.exists(img_path):
        st.image(img_path,width=300)
    else:
        st.warning("Profile Image Not Found")

# ================= ABOUT =================

@st.dialog("About Margdarshak AI")
def About():

    st.header("About Margdarshak AI")

    st.markdown("""
### Technologies Used

- Python
- Streamlit
- MongoDB
- Pandas
- Scikit-Learn
- Machine Learning

### Features

- AI-Based Stream Prediction
- Career Guidance System
- Student Interest Analysis
- Marks Evaluation
- Secure Login System
- Profile Management

### Objective

Margdarshak AI helps students choose the right academic stream based on data-driven insights rather than assumptions or peer pressure.

### Future Enhancements

- College Recommendations
- Career Roadmaps
- AI Chat Assistant
- Skill Assessment Tests
- Advanced Deep Learning Models
""")

# ================= CONTACT =================

@st.dialog("Contact Us")
def contact():

    st.subheader("Contact Information")

    st.write("📞 Phone : 9431774516")
    st.write("📧 Email : kumarhrithick369@gmail.com")
    st.write("💻 GitHub : Hrithick-kumar")

# ================= SIGN IN =================

@st.dialog("Sign In")
def SignIn():

    st.subheader("Login")

    username=st.text_input("Username")
    password=st.text_input("Password",type="password")

    if st.button("SIGN IN",use_container_width=True):

        user=coll.find_one({
            "Name":username,
            "Pass":password
        })

        if user:

            st.session_state["User"]=username
            st.session_state["Passwd"]=password

            st.success("Signed In Successfully")

            time.sleep(1)

            st.switch_page("pages/Dashboard.py")

        else:
            st.error("Invalid Credentials")

# ================= SIGN UP =================

@st.dialog("Sign Up")
def SignUp():

    st.subheader("Create Account")

    col1,col2=st.columns(2)

    with col1:

        username=st.text_input("Username")

        password=st.text_input(
            "Password",
            type="password"
        )

        dob=st.date_input(
            "DOB",
            value=date.today(),
            min_value=date(1980,1,1),
            max_value=date.today()
        )

    with col2:

        photo=st.camera_input("Take Photo")

    if st.button("REGISTER",use_container_width=True):

        if username=="" or password=="":

            st.warning("Fill all required fields")
            return

        existing=coll.find_one({"Name":username})

        if existing:

            st.error("Username already exists")
            return

        photo_name=""

        if photo:

            os.makedirs("images",exist_ok=True)

            photo_name=f"img_{random.randint(1000,9999)}.png"

            filepath=os.path.join(
                "images",
                photo_name
            )

            with open(filepath,"wb") as f:
                f.write(photo.getbuffer())

        coll.insert_one({
            "Name":username,
            "Pass":password,
            "DOB":str(dob),
            "Photo":photo_name
        })

        st.success("Registration Successful")

        time.sleep(1)

        st.rerun()

# ================= SIDEBAR =================

with st.sidebar:

    st.title("Margdarshak AI")

    if "User" in st.session_state:
        st.success(f"Welcome {st.session_state['User']}")

    st.divider()

    if st.button("👤 Profile",use_container_width=True):
        profile()

    if st.button("ℹ️ About",use_container_width=True):
        About()

    if st.button("📞 Contact",use_container_width=True):
        contact()

    st.divider()

    if st.button("📝 Sign Up",use_container_width=True):
        SignUp()

    if st.button("🔑 Sign In",use_container_width=True):
        SignIn()

# ================= FOOTER =================

st.markdown("""
<br><br>
<hr>
<center>
<h4>Right Guidance Today Creates a Better Tomorrow</h4>
<h5>Choose Right Today, Lest Regret Forever</h5>
</center>
""",unsafe_allow_html=True)
