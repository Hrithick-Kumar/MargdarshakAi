import requests
import streamlit as st
from pymongo import MongoClient
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import base64
import os
import time

================= PAGE CONFIG =================

st.set_page_config(
page_title="Margdarshak AI Dashboard",
page_icon="🎓",
layout="wide"
)

================= DATABASE =================

conn = MongoClient(st.secrets["MONGO_URI"])

db = conn["User"]
coll = db["Info"]

================= LOGIN CHECK =================

if "User" not in st.session_state:
st.warning("Please Sign In First")
time.sleep(1)
st.switch_page("MargdarshakAi.py")

username = st.session_state["User"]

================= BACKGROUND =================

def add_bg(image_file):

if not os.path.exists(image_file):  
    return  

with open(image_file, "rb") as image:  
    encoded = base64.b64encode(image.read()).decode()  

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

add_bg("background_img/bg.png")

================= LOAD USER =================

user = coll.find_one({"Name": username})

================= HEADER =================

if "recommended_stream" not in st.session_state:
st.session_state["recommended_stream"] = "Not Predicted Yet"
st.title("🎓 Margdarshak AI Dashboard")

st.markdown(
"""
<div style='background:rgba(25,25,25,0.8);padding:20px;border-radius:15px;'>
<h3>Discover Your Ideal Career Path</h3>
<p>
Enter your goals, interests and academic performance.
Margdarshak AI will recommend the most suitable stream.
</p>
</div>
""",
unsafe_allow_html=True
)

================= TEXT MODEL =================

stream_data = pd.read_csv("Stream1.csv")

text_X = stream_data["word"]
text_y = stream_data["stream"]

vectorizer = CountVectorizer()

text_matrix = vectorizer.fit_transform(text_X)

text_model = MultinomialNB()

text_model.fit(text_matrix, text_y)

================= PREFERENCE MODEL =================

pref_data = pd.read_csv("Preference.csv")

pref_X = pref_data[
[
"Maths_Interest",
"Science_Interest",
"Business_Interest",
"Creativity",
"Stress_Handling_Level"
]
]

pref_y = pref_data["Stream"]

pref_model = RandomForestClassifier(
n_estimators=100,
random_state=42
)

pref_model.fit(pref_X, pref_y)

================= MARKS MODEL =================

marks_data = pd.read_csv("StudentMark.csv")

marks_X = marks_data[
[
"Maths",
"Science",
"Social Science",
"English"
]
]

marks_y = marks_data["Stream"]

marks_model = RandomForestClassifier(
n_estimators=100,
random_state=42
)

marks_model.fit(marks_X, marks_y)

#========goal after stream==========
career_map = {

"Science":[  
    "Software Engineer",  
    "Doctor",  
    "Data Scientist",  
    "Research Scientist",  
    "AI Engineer",  
    "NDA"  
],  

"Commerce":[  
    "CA",  
    "CS",  
    "Investment Banker",  
    "MBA",  
    "Business Analyst"  
],  

"Arts":[  
    "Lawyer",  
    "Journalist",  
    "UPSC",  
    "Psychologist",  
    "Designer"  
]

}

================= GOAL SECTION =================

st.header("Career Goal Analysis")

goal_input = st.text_area(
"Describe your interests, dreams and future goals",
height=150
)

================= PREFERENCE SECTION =================

st.header("Interest Assessment")

col1, col2 = st.columns(2)

with col1:

maths_interest = st.slider(  
    "Maths Interest",  
    0,  
    10,  
    5  
)  

science_interest = st.slider(  
    "Science Interest",  
    0,  
    10,  
    5  
)  

business_interest = st.slider(  
    "Business Interest",  
    0,  
    10,  
    5  
)

with col2:

creativity = st.slider(  
    "Creativity",  
    0,  
    10,  
    5  
)  

stress_level = st.slider(  
    "Stress Handling Level",  
    0,  
    10,  
    5  
)

================= MARKS SECTION =================

st.header("Academic Performance")

m1, m2 = st.columns(2)

with m1:

maths = st.number_input(  
    "Maths Marks",  
    min_value=0,  
    max_value=100,  
    value=0  
)  

science = st.number_input(  
    "Science Marks",  
    min_value=0,  
    max_value=100,  
    value=0  
)

with m2:

social = st.number_input(  
    "Social Science Marks",  
    min_value=0,  
    max_value=100,  
    value=0  
)  

english = st.number_input(  
    "English Marks",  
    min_value=0,  
    max_value=100,  
    value=0  
)

================= PREDICTION =================

if st.button(
"Predict My Stream",
use_container_width=True
):

results = []  

# Goal Prediction  

if goal_input.strip() != "":  

    goal_vector = vectorizer.transform(  
        [goal_input]  
    )  

    goal_prediction = text_model.predict(  
        goal_vector  
    )[0]  

    results.append(goal_prediction)  

# Preference Prediction  

pref_input = pd.DataFrame(  
    [[  
        maths_interest,  
        science_interest,  
        business_interest,  
        creativity,  
        stress_level  
    ]],  
    columns=[  
        "Maths_Interest",  
        "Science_Interest",  
        "Business_Interest",  
        "Creativity",  
        "Stress_Handling_Level"  
    ]  
)  

pref_prediction = pref_model.predict(  
    pref_input  
)[0]  

results.append(pref_prediction)  

# Marks Prediction  

marks_prediction = marks_model.predict(  
    [[  
        maths,  
        science,  
        social,  
        english  
    ]]  
)[0]  

results.append(marks_prediction)  

# Final Result  
if maths==0 or science==0 or english==0 or social==0:  
       st.toast("Please fill details")  
else:  
  
   final_stream = Counter(results).most_common(1)[0][0]  
   st.session_state["recommended_stream"] = final_stream  
   st.success(f"🎯 Recommended Stream: {final_stream}" )  

   st.balloons()  

   st.subheader("Prediction Breakdown")  

   if goal_input.strip() != "":  
       st.info(f"Goal Analysis → {goal_prediction}")  

       st.info(f"Interest Analysis → {pref_prediction}")  

       st.info( f"Marks Analysis → {marks_prediction}" )  


   if final_stream in career_map:  
       st.subheader("Career Options")  
       for career in career_map[final_stream]:  
           st.write("•",career)

#ai counsellor
def ask_ai(question,stream):

api_key = st.secrets["OPENROUTER_API_KEY"]  

headers = {  
    "Authorization": f"Bearer {api_key}",  
    "Content-Type": "application/json"  
}  

payload = {  
    "model": "openrouter/free",  
    "messages": [  
        {  
            "role": "system",  
            "content":f"""  
            You are Margdarshak AI.  
            Student Recommended Stream:{stream}You are a career counselor.  
            Give:  
            1. Personalized guidance  
            2. Career roadmap  
            3. Required skills  
            4. Future opportunities  
            5. Suggested exams  
            Keep answers simple and practical.

"""
},
{
"role": "user",
"content": question
}
]
}

response = requests.post(  
    "https://openrouter.ai/api/v1/chat/completions",  
    headers=headers,  
    json=payload,  
    timeout=30  
)  

result = response.json()  

return result["choices"][0]["message"]["content"]

================= UPDATE PHOTO =================

@st.dialog("Update Photo")
def update_photo():

uploaded = st.file_uploader(  
    "Upload Image",  
    type=["png", "jpg", "jpeg"]  
)  

if uploaded:  

    st.image(uploaded, width=250)  

    if st.button("Save"):  

        os.makedirs(  
            "images/updateImg",  
            exist_ok=True  
        )  

        filepath = os.path.join(  
            "images/updateImg",  
            uploaded.name  
        )  

        with open(filepath, "wb") as f:  
            f.write(uploaded.getbuffer())  

        coll.update_one(  
            {"Name": username},  
            {  
                "$set": {  
                    "Photo":  
                    f"updateImg/{uploaded.name}"  
                }  
            }  
        )  

        st.success(  
            "Photo Updated Successfully"  
        )  

        time.sleep(1)  

        st.rerun()

================= CHANGE PASSWORD =================

@st.dialog("Change Password")
def change_password():

old_pass = st.text_input(  
    "Old Password",  
    type="password"  
)  

new_pass = st.text_input(  
    "New Password",  
    type="password"  
)  

if st.button("Update Password"):  

    user_data = coll.find_one(  
        {"Name": username}  
    )  

    if user_data["Pass"] == old_pass:  

        coll.update_one(  
            {"Name": username},  
            {  
                "$set": {  
                    "Pass": new_pass  
                }  
            }  
        )  

        st.success(  
            "Password Updated"  
        )  

    else:  

        st.error(  
            "Incorrect Old Password"  
        )

================= SIDEBAR =================

with st.sidebar:

st.subheader(f"Welcome {username}")  

if user:  

    photo = user.get("Photo", "")  

    image_path = f"images/{photo}"  

    if os.path.exists(image_path):  

        st.image(  
            image_path,  
            width=250  
        )  

    else:  

        st.warning(  
            "Profile Image Missing"  
        )  

st.divider()  

if st.button(  
    "Update Photo",  
    use_container_width=True  
):  
    update_photo()  

if st.button(  
    "Change Password",  
    use_container_width=True  
):  
    change_password()  

st.divider()  

if st.button(  
    "Sign Out",  
    use_container_width=True  
):  

    st.session_state.clear()  

    st.switch_page(  
        "MargdarshakAi.py"  
    )

st.divider()
st.info(
f"Current Recommended Stream: {st.session_state['recommended_stream']}"
)
st.header("🤖 Margdarshak AI Chat")

if "messages" not in st.session_state:
st.session_state.messages = []

for msg in st.session_state.messages:

with st.chat_message(  
    msg["role"]  
):  

    st.markdown(  
        msg["content"]  
    )

prompt = st.chat_input(
"Ask Margdarshak AI..."
)

if prompt:

st.session_state.messages.append(  
    {  
        "role":"user",  
        "content":prompt  
    }  
)  

with st.chat_message("user"):  
    st.markdown(prompt)  

with st.spinner("Thinking..."):  
    answer = ask_ai(prompt,st.session_state["recommended_stream"])  

st.session_state.messages.append(  
    {  
        "role":"assistant",  
        "content":answer  
    }  
)  

with st.chat_message("assistant"):  
    st.markdown(answer)  
if st.button("Clear Chat",use_container_width=True):  
    st.session_state.messages = []  
    st.rerun()
