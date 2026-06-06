import streamlit as st
import pandas as pd
import base64
import os
import time

from pymongo import MongoClient
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Margdarshak AI Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ================= DATABASE =================

conn = MongoClient(
    st.secrets["MONGO_URI"]
)

db = conn["User"]
coll = db["Info"]

# ================= LOGIN CHECK =================

if "User" not in st.session_state:
    st.warning(
        "Please Sign In First"
    )
    time.sleep(1)
    st.switch_page(
        "MargdarshakAi.py"
    )

username = st.session_state["User"]

# ================= SESSION STATE =================

if "recommended_stream" not in st.session_state:
    st.session_state[
        "recommended_stream"
    ] = "Not Predicted Yet"

# ================= BACKGROUND =================

def add_bg(image_file):
    if not os.path.exists(
        image_file
    ):
        return
    with open(
        image_file,
        "rb"
    ) as image:
        encoded = base64.b64encode(
            image.read()
        ).decode()
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

add_bg(
    "background_img/bg.png"
)

# ================= LOAD USER =================

user = coll.find_one(
    {"Name": username}
)

# ================= HEADER =================

st.title(
    "🎓 Margdarshak AI Dashboard"
)

st.markdown(
    """
    <div style="
    background:rgba(25,25,25,0.75);
    padding:20px;
    border-radius:15px;
    ">
    <h3>
    Discover Your Ideal Career Path
    </h3>
    <p>
    Enter your interests, goals,
    academic performance and preferences.
    Margdarshak AI will recommend
    the most suitable stream for you.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ================= TEXT MODEL =================

stream_data = pd.read_csv(
    "Stream1.csv"
)

vectorizer = CountVectorizer()

text_X = vectorizer.fit_transform(
    stream_data["word"]
)

text_model = MultinomialNB()

text_model.fit(
    text_X,
    stream_data["stream"]
)

# ================= PREFERENCE MODEL =================

pref_data = pd.read_csv(
    "Preference.csv"
)

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

pref_model.fit(
    pref_X,
    pref_y
)

# ================= MARKS MODEL =================

marks_data = pd.read_csv(
    "StudentMark.csv"
)

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

marks_model.fit(
    marks_X,
    marks_y
)

# ================= CAREER MAP =================

career_map = {
    "Science":[
        "Software Engineer",
        "Doctor",
        "AI Engineer",
        "Data Scientist",
        "Research Scientist",
        "NDA Officer"
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
        "Psychologist",
        "UPSC Officer",
        "Designer"
    ]
}

# ================= GOAL SECTION =================

st.header(
    "🎯 Career Goal Analysis"
)

goal_input = st.text_area(
    "Describe your interests, dreams and future goals",
    height=150
)

# ================= INTEREST SECTION =================

st.header(
    "📊 Interest Assessment"
)

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

# ================= MARKS SECTION =================

st.header(
    "📚 Academic Performance"
)

m1, m2 = st.columns(2)

with m1:
    maths = st.number_input(
        "Maths Marks",
        0,
        100,
        0
    )
    science = st.number_input(
        "Science Marks",
        0,
        100,
        0
    )

with m2:
    social = st.number_input(
        "Social Science Marks",
        0,
        100,
        0
    )
    english = st.number_input(
        "English Marks",
        0,
        100,
        0
    )

# ================= PREDICTION =================

if st.button(
    "🚀 Predict My Stream",
    use_container_width=True
):
    results = []
    if goal_input.strip():
        goal_vector = vectorizer.transform(
            [goal_input]
        )
        goal_prediction = text_model.predict(
            goal_vector
        )[0]
        results.append(
            goal_prediction
        )
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
    results.append(
        pref_prediction
    )
    marks_prediction = marks_model.predict(
        [[
            maths,
            science,
            social,
            english
        ]]
    )[0]
    results.append(
        marks_prediction
    )
    final_stream = Counter(
        results
    ).most_common(1)[0][0]
    st.session_state[
        "recommended_stream"
    ] = final_stream
    st.success(
        f"🎯 Recommended Stream: {final_stream}"
    )
    st.balloons()
    st.subheader(
        "Prediction Breakdown"
    )
    if goal_input.strip():
        st.info(
            f"Goal Analysis → {goal_prediction}"
        )
    st.info(
        f"Interest Analysis → {pref_prediction}"
    )
    st.info(
        f"Marks Analysis → {marks_prediction}"
    )
    if final_stream in career_map:
        st.subheader(
            "💼 Recommended Careers"
        )
        for career in career_map[
            final_stream
        ]:
            st.write(
                "•",
                career
            )
# ================= UPDATE PHOTO =================

@st.dialog("Update Profile Photo")
def update_photo():

    uploaded = st.file_uploader(
        "Upload New Profile Photo",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        st.image(
            uploaded,
            width=250
        )

        if st.button(
            "Save Photo",
            use_container_width=True
        ):

            os.makedirs(
                "images/updateImg",
                exist_ok=True
            )

            filename = (
                f"{username}_"
                f"{uploaded.name}"
            )

            filepath = os.path.join(
                "images/updateImg",
                filename
            )

            with open(
                filepath,
                "wb"
            ) as f:

                f.write(
                    uploaded.getbuffer()
                )

            coll.update_one(
                {
                    "Name": username
                },
                {
                    "$set": {
                        "Photo":
                        f"updateImg/{filename}"
                    }
                }
            )

            st.success(
                "Photo Updated Successfully"
            )

            time.sleep(1)

            st.rerun()

# ================= CHANGE PASSWORD =================

@st.dialog("Change Password")
def change_password():

    old_pass = st.text_input(
        "Current Password",
        type="password"
    )

    new_pass = st.text_input(
        "New Password",
        type="password"
    )

    confirm_pass = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Update Password",
        use_container_width=True
    ):

        user_data = coll.find_one(
            {
                "Name": username
            }
        )

        if not old_pass:

            st.warning(
                "Enter Current Password"
            )

        elif user_data["Pass"] != old_pass:

            st.error(
                "Current Password Incorrect"
            )

        elif len(new_pass) < 6:

            st.warning(
                "Password must contain at least 6 characters"
            )

        elif new_pass != confirm_pass:

            st.error(
                "Passwords do not match"
            )

        else:

            coll.update_one(
                {
                    "Name": username
                },
                {
                    "$set": {
                        "Pass": new_pass
                    }
                }
            )

            st.success(
                "Password Updated Successfully"
            )

# ================= PROFILE INFO =================

def show_profile():

    st.subheader(
        "👤 Profile Information"
    )

    if user:

        st.write(
            f"Username : {user['Name']}"
        )

        if "DOB" in user:

            st.write(
                f"DOB : {user['DOB']}"
            )

        photo = user.get(
            "Photo",
            ""
        )

        image_path = (
            f"images/{photo}"
        )

        if (
            photo
            and
            os.path.exists(
                image_path
            )
        ):

            st.image(
                image_path,
                width=250
            )

        else:

            st.info(
                "No Profile Photo"
            )

# ================= SIDEBAR =================

with st.sidebar:

    st.title(
        "Margdarshak AI"
    )

    st.success(
        f"Welcome {username}"
    )

    # ---------- Profile Image ----------

    if user:

        photo = user.get(
            "Photo",
            ""
        )

        image_path = (
            f"images/{photo}"
        )

        if (
            photo
            and
            os.path.exists(
                image_path
            )
        ):

            st.image(
                image_path,
                width=220
            )

        else:

            st.warning(
                "Profile Image Missing"
            )

    st.divider()

    # ---------- Stream ----------

    st.info(
        f"""
Current Stream:

{st.session_state['recommended_stream']}
"""
    )

    st.divider()

    # ---------- Buttons ----------

    if st.button(
        "👤 View Profile",
        use_container_width=True
    ):

        show_profile()

    if st.button(
        "🖼️ Update Photo",
        use_container_width=True
    ):

        update_photo()

    if st.button(
        "🔒 Change Password",
        use_container_width=True
    ):

        change_password()

    st.divider()

    if st.button(
        "🚪 Sign Out",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "MargdarshakAi.py" )
# ================= OPENROUTER AI =================

def ask_ai(question, stream):

    api_key = st.secrets[
        "OPENROUTER_API_KEY"
    ]

    headers = {
        "Authorization":
        f"Bearer {api_key}",

        "Content-Type":
        "application/json"
    }

    payload = {

        "model":
        "openrouter/free",

        "messages": [

            {
                "role": "system",

                "content": f"""
You are Margdarshak AI.

Student Recommended Stream:
{stream}

You are an expert career counselor.

Your job is to help students with:

• Stream Selection
• Career Guidance
• JEE
• NEET
• UPSC
• Government Jobs
• Commerce Careers
• Arts Careers
• College Selection
• Skill Development
• Future Planning

Rules:

1. Give personalized advice.
2. Consider the recommended stream.
3. Suggest careers.
4. Suggest skills.
5. Suggest exams.
6. Keep answers practical.
7. Use bullet points.
8. Keep answers student friendly.
"""
            },

            {
                "role": "user",

                "content": f"""
Recommended Stream:
{stream}

Student Question:
{question}
"""
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    data = response.json()

    if "choices" not in data:

        return (
            "AI service unavailable.\n\n"
            + str(data)
        )

    return data["choices"][0]["message"]["content"]

# ================= CHAT HEADER =================

st.divider()

st.header(
    "🤖 Margdarshak AI Counselor"
)

st.info(
    f"""
Current Recommended Stream:

{st.session_state['recommended_stream']}
"""
)

# ================= CHAT MEMORY =================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ================= CLEAR CHAT =================

col1, col2 = st.columns([3,1])

with col2:

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

# ================= DISPLAY CHAT =================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )

# ================= CHAT INPUT =================

prompt = st.chat_input(
    "Ask Margdarshak AI..."
)

# ================= USER MESSAGE =================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            prompt
        )

    try:

        with st.spinner(
            "Thinking..."
        ):

            answer = ask_ai(
                prompt,
                st.session_state[
                    "recommended_stream"
                ]
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Keep last 20 messages only

        if len(
            st.session_state.messages
        ) > 20:

            st.session_state.messages = (
                st.session_state.messages[-20:]
            )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )

    except Exception as e:

        with st.chat_message(
            "assistant"
        ):

            st.error(
                f"AI Error: {str(e)}"
            )

# ================= QUICK QUESTIONS =================

st.divider()

st.subheader(
    "🚀 Quick Questions"
)

q1, q2 = st.columns(2)

with q1:

    st.markdown("""
- How can I prepare for my future?
- What careers suit my stream?
- Which skills should I learn?
- How do I prepare for competitive exams?
""")

with q2:

    st.markdown("""
- Best colleges for my stream?
- How to become a Data Scientist?
- Government job opportunities?
- Future scope of my stream?
""")
        
