import requests
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

conn = MongoClient(st.secrets["MONGO_URI"])
db = conn["User"]
coll = db["Info"]
# ================= LOGIN CHECK =================

if "User" not in st.session_state:
    st.warning("Please Sign In First")
    time.sleep(1)
    st.switch_page("MargdarshakAi.py")
username = st.session_state["User"]

# ================= SESSION STATE =================

if "recommended_stream" not in st.session_state:
    st.session_state["recommended_stream"] = "Not Predicted Yet"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ================= BACKGROUND =================

def add_bg(image_file):
    if not os.path.exists(image_file):
        return
    with open(image_file,"rb") as image:
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

add_bg(
    "background_img/Bg1.png"
)

# ================= LOAD USER =================

user = coll.find_one({"Name": username})

# ================= HEADER =================

st.title("Margdarshak AI Dashboard")
st.markdown(
    """
    <div style='
    background:rgba(25,25,25,0.8);
    padding:20px;
    border-radius:15px;
    '>

    <h3>
    Discover Your Ideal Career Path
    </h3>

    <p>
    Enter your goals,
    interests and academic performance.

    Margdarshak AI will recommend
    the most suitable stream.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
# ================= TEXT MODEL =================

@st.cache_resource
def load_text_model():

    stream_data = pd.read_csv("Stream1.csv" )
    text_X = stream_data["word"]
    text_y = stream_data["stream"]
    vectorizer = CountVectorizer()
    text_matrix = vectorizer.fit_transform(text_X)
    text_model = MultinomialNB()
    text_model.fit(text_matrix,text_y)

    return (vectorizer,text_model)
vectorizer, text_model = (load_text_model())

# ================= PREFERENCE MODEL =================

@st.cache_resource
def load_pref_model():

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

    return pref_model

pref_model = (
    load_pref_model()
)

# ================= MARKS MODEL =================

@st.cache_resource
def load_marks_model():

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

    return marks_model

marks_model = (
    load_marks_model()
)

# ================= CAREER MAP =================

career_map = {

    "Science": [

        "Software Engineer",
        "Doctor",
        "Data Scientist",
        "Research Scientist",
        "AI Engineer",
        "NDA Officer"

    ],

    "Commerce": [

        "CA",
        "CS",
        "Investment Banker",
        "MBA",
        "Business Analyst"

    ],

    "Arts": [

        "Lawyer",
        "Journalist",
        "UPSC Officer",
        "Psychologist",
        "Designer"

    ]
}
# ================= PREDICTION FORM =================

with st.form(
    "prediction_form"
):

    # ================= GOAL SECTION =================

    st.header(
        "Career Goal Analysis"
    )

    goal_input = st.text_area(
        "Describe your interests, dreams and future goals",
        height=150
    )

    # ================= INTEREST SECTION =================

    st.header(
        "Interest Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        maths_interest = st.slider("Maths Interest",0,10,5 )
        science_interest = st.slider("Science Interest",0,10,5)
        business_interest = st.slider("Business Interest",0,10,5)
    with col2:
        creativity = st.slider("Creativity", 0, 10,5 )
        stress_level = st.slider("Stress Handling Level", 0,10, 5)

    # ================= MARKS SECTION =================

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

    # ================= SUBMIT BUTTON =================

    predict_btn = (
        st.form_submit_button(
            "🚀 Predict My Stream",
            use_container_width=True
        )
    )

# ================= PREDICTION LOGIC =================

if predict_btn:

    if (
        maths == 0
        or science == 0
        or social == 0
        or english == 0
    ):

        st.warning(
            "Please fill all marks."
        )

    else:

        results = []

        # ===== GOAL PREDICTION =====

        if goal_input.strip():

            goal_vector = (
                vectorizer.transform(
                    [goal_input]
                )
            )

            goal_prediction = (
                text_model.predict(
                    goal_vector
                )[0]
            )

            results.append(
                goal_prediction
            )

        # ===== PREFERENCE PREDICTION =====

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

        pref_prediction = (
            pref_model.predict(
                pref_input
            )[0]
        )

        results.append(
            pref_prediction
        )

        # ===== MARKS PREDICTION =====

        marks_prediction = (
            marks_model.predict(
                [[
                    maths,
                    science,
                    social,
                    english
                ]]
            )[0]
        )

        results.append(
            marks_prediction
        )

        # ===== FINAL RESULT =====

        final_stream = (
            Counter(results)
            .most_common(1)[0][0]
        )

        st.session_state[
            "recommended_stream"
        ] = final_stream

        st.success(
            f"Recommended Stream: {final_stream}"
        )

        st.balloons()

        # ===== BREAKDOWN =====

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

        # ===== CAREER OPTIONS =====

        if final_stream in career_map:

            st.subheader(
                "Career Options"
            )

            for career in career_map[
                final_stream
            ]:

                st.write(
                    "•",
                    career
                )
# ================= AI COUNSELLOR =================

def ask_ai(
    question,
    stream
):

    try:

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

You are a professional career counselor.

Your responsibilities:

1. Career Guidance
2. Career Roadmap
3. Future Scope
4. Skill Recommendations
5. Exam Suggestions
6. College Guidance

Rules:

• Keep answers simple
• Be practical
• Use bullet points
• Focus on student's stream
• Keep answers student friendly
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
            timeout=60
        )

        data = response.json()

        if "choices" not in data:

            return (
                "AI service unavailable.\n\n"
                + str(data)
            )

        return data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    except Exception as e:

        return (
            f"Error: {str(e)}"
        )

# ================= CHAT SESSION =================

if "messages" not in st.session_state:

    st.session_state[
        "messages"
    ] = []

# ================= QUICK PROMPTS =================

quick_questions = [

    "What careers suit my stream?",

    "How should I prepare for my future?",

    "Which skills should I learn?",

    "Best entrance exams for me?",

    "Government jobs after my stream?",

    "Future scope of my stream?"
]

# ================= AI STATUS =================

st.divider()

st.success(
    f"""AI Counselor Ready
"""
      )
# ================= UPDATE PHOTO =================

@st.dialog("🖼️ Update Photo")
def update_photo():

    uploaded = st.file_uploader(
        "Upload New Photo",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if uploaded:

        st.image(
            uploaded,
            width=250
        )

        if st.button(
            "Save Photo"
        ):

            os.makedirs(
                "images/updateImg",
                exist_ok=True
            )

            file_path = os.path.join(
                "images/updateImg",
                uploaded.name
            )

            with open(
                file_path,
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
                        f"updateImg/{uploaded.name}"
                    }
                }
            )

            st.success(
                "Photo Updated Successfully"
            )

            time.sleep(1)

            st.rerun()

# ================= CHANGE PASSWORD =================

@st.dialog("🔒 Change Password")
def change_password():

    old_pass = st.text_input(
        "Old Password",
        type="password"
    )

    new_pass = st.text_input(
        "New Password",
        type="password"
    )

    if st.button(
        "Update Password"
    ):

        user_data = coll.find_one(
            {
                "Name": username
            }
        )

        if (
            user_data["Pass"]
            == old_pass
        ):

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
                "Password Updated"
            )

        else:

            st.error(
                "Incorrect Old Password"
            )

# ================= SIDEBAR =================

with st.sidebar:

    st.subheader(
        f"Welcome {username}"
    )

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

    st.info(
        f"""
Recommended Stream

{st.session_state['recommended_stream']}
"""
    )

    st.divider()

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
            "MargdarshakAi.py"
          )
# ================= AI CHAT =================

st.divider()

st.header(
    "Margdarshak AI Chat"
)

# ================= CHAT CONTROLS =================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state[
            "messages"
        ] = []

        st.rerun()


# ================= CHAT HISTORY =================

for msg in st.session_state[
    "messages"
]:

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

    st.session_state[
        "messages"
    ].append(
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

    with st.spinner(
        "Thinking..."
    ):

        answer = ask_ai(
            prompt,
            st.session_state[
                "recommended_stream"
            ]
        )

    st.session_state[
        "messages"
    ].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Keep only latest 30 messages

    if len(
        st.session_state[
            "messages"
        ]
    ) > 30:

        st.session_state[
            "messages"
        ] = (
            st.session_state[
                "messages"
            ][-30:]
        )

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )

# ================= QUICK QUESTIONS =================

st.divider()

st.subheader(
    "Suggested Questions"
)

q1, q2 = st.columns(2)

with q1:

    st.markdown(
        """
- What careers suit my stream?
- How should I prepare for my future?
- Which skills should I learn?
- Best entrance exams for me?
"""
    )

with q2:

    st.markdown(
        """
- Government jobs after my stream?
- Future scope of my stream?
- Best colleges for my stream?
- Career roadmap for my stream?
"""
    )

# ================= FOOTER =================

st.divider()

